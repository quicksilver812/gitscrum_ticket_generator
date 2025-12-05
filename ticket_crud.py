from database.database import SessionLocal
from models.models import Ticket
from datetime import timedelta

session = SessionLocal()

def create_ticket(bug):
    """Save bug into tickets table"""
    ticket = Ticket(
        ticket_id=0,  # Generate unique ticket ID
        user_email=bug.user_email,    # Changed from bug.user
        bug_title=bug.title,          # Changed from bug.title
        bug_summary=bug.summary,      # Changed from bug.summary
        bug_priority=bug.priority     # Changed from bug.priority
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    session.close()
    return ticket

def update_uuid(new_uuid):
    ticket = session.query(Ticket).filter(Ticket.ticket_id == 0).first()
    ticket.ticket_id = new_uuid
    session.commit()
    session.close()
    print("UUID updated in db.")

def get_all_tickets():
    """Retrieve all tickets"""
    tickets = session.query(Ticket).all()
    session.close()
    return tickets

def get_all_pending_tickets():
    tickets = session.query(Ticket).filter(Ticket.status == False).all()
    session.close()
    return tickets

def get_ticket_by_id(ticket_id: str):
    """Retrieve tickets filtered by priority"""
    ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    session.close()
    return ticket

def change_ticket_status(ticket_id):
    ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    ticket.status = True
    session.commit()
    session.close()

def add_duration(ticket_id, duration):
    ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    ticket.duration = ticket.duration + duration
    session.commit()
    session.close()

def retrieve_duration(ticket_id):
    ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    session.close()
    ageing = timedelta(hours = ticket.duration)
    days = ageing.days
    hours = ticket.duration - (days*24)
    return days, hours