from fastapi import FastAPI
from database.database import engine, Base
import asyncio
from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from email_files.pull_mails import fetch_unread_emails
from email_files.process_mails import classify_and_parse_email, close_provider
from crud.ticket_crud import change_ticket_status, create_ticket, get_all_pending_tickets, update_uuid, add_duration, retrieve_duration
from gitscrum_files.git_scrum import create_task_on_gitscrum, get_task_status
from email_files.send_mails import send_followup_email, send_ticket_email, send_employee_email


app = FastAPI(title="Email Issue Tracker")

employee_email =  os.getenv("EMPLOYEE_EMAIL")
check_duration = int(os.getenv("CHECK_DURATION"))

Base.metadata.create_all(bind=engine)

def check_if_completed():
    tickets = get_all_pending_tickets()
    for t in tickets:
        status = get_task_status(t.ticket_id)
        if status == "Complete":
            change_ticket_status(t.ticket_id)
            print(f"{t.ticket_id} marked complete.")
        else:
            # add 4 hours to the task
            add_duration(t.ticket_id, check_duration)
            # retrieve the duration exactly
            days, hours = retrieve_duration(t.ticket_id)
            # get days and hours
            # pass to followup email function
            asyncio.run(send_followup_email(employee_email, t.ticket_id, t.bug_title, days, hours))

def check_emails_job():
    print("📩 Checking new emails...")
    emails = fetch_unread_emails()
    
    if not emails:
        print("No new emails found.")
        return
    
    for email in emails:
        print(f"📧 Processing email from {email['from']}: {email['subject']}")

        try:
            # Call async AI classification
            bug = asyncio.run(classify_and_parse_email(email['subject'], email['body'], email['from']))

            if bug:
                print("✅ Bug detected!")

                ticket = create_ticket(bug)
                print(f"   💾 Ticket saved to DB - ID: {ticket.ticket_id}")
                print(f"   Title: {ticket.bug_title}")
                print(f"   Priority: {ticket.bug_priority}")
                
                # 2️⃣ Create task on GitScrum
                task_id = create_task_on_gitscrum(
                    title=f"{ticket.bug_title} ({ticket.bug_priority})",
                    description=ticket.bug_summary,
                )
                if task_id:
                    print(f"   📋 GitScrum task created - Task ID: {task_id['data']['uuid']}")
                    # Update ticket with GitScrum task ID (optional)
                    # You can add code here to update the ticket.git_scrum_task_id field
                else:
                    print(f"   ⚠️ Failed to create GitScrum task")

                # Save to database
                gen_uuid = task_id['data']['uuid']
                update_uuid(gen_uuid)
                
                # 3️⃣ Send confirmation email to customer
                asyncio.run(send_ticket_email(ticket.user_email, gen_uuid))
                asyncio.run(send_employee_email(employee_email, gen_uuid, ticket.bug_title))
                print(f"   📧 Confirmation email sent to {ticket.user_email} and {employee_email}")
                
                print(f"✅ Complete! Ticket #{gen_uuid} processed successfully.\n")
            else:
                print("❌ Not a bug - email ignored.\n")
                
        except Exception as e:
            print(f"❌ Error processing email: {e}")
            import traceback
            traceback.print_exc()
            print()

# Schedule the job every 2 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(check_emails_job, "interval", minutes=1, next_run_time=datetime.now())
scheduler.add_job(check_if_completed, "interval", hours = check_duration)
scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Shutting down...")
    scheduler.shutdown()
    await close_provider()

@app.get("/")
async def root():
    return {"message": "Email Issue Tracker Backend is running"}