from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database.database import Base
from pydantic import BaseModel

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    user_email = Column(String, index=True)
    bug_title = Column(String)
    bug_summary = Column(String)
    bug_priority = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Boolean, default = False)
    duration = Column(Integer, default = 0)

class BugIssue(BaseModel):
    title: str
    user_email: str
    summary: str
    priority: str



