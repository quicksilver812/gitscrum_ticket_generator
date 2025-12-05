import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

async def send_ticket_email(to_email: str, ticket_id: str):
    subject = f"Your Support Ticket #{ticket_id}"
    body = f"""Hello,

We have received your issue and are working on it. 

Your support ticket ID is: {ticket_id}

We will get back to you as soon as possible.

Thank you for contacting us!

Best regards,
Support Team"""
    
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    
    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT", "587")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True
    )
    print(f"Email sent successfully to {to_email}")

async def send_employee_email(to_email: str, ticket_id: str, task_name: str):
    subject = f"Task Assignment Notification"
    body = f"""Hello,

You have been assigned a new task. Please review the task details and start working on it at your earliest convenience.

Task ID: {ticket_id}
Task Title: {task_name}

Kindly update the progress regularly
Best regards,
Support Team"""
    
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    
    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT", "587")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True
    )
    print(f"Email sent successfully to {to_email}")

async def send_followup_email(to_email: str, ticket_id: str, task_name: str, days, hours):
    subject = f"Reminder: Please Fix the Issue with {task_name}"
    body = f"""Hello,

This is a reminder to fix the issue below.

Task ID: {ticket_id}
Task Title: {task_name}

Pending since {days} days {hours} hours.

Please look into this at the earliest and update once the issue has been resolved.

Thank you for your prompt attention to this matter.

Best regards,
Support Team"""
    
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    
    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT", "587")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True
    )
    print(f"Followup email for '{task_name}' sent successfully to {to_email}")