from pydantic import BaseModel, EmailStr
from typing import Dict, Any

class EmailSchema(BaseModel):
    # Data structure for an email message.
    to_email: EmailStr       # Whi will receive the email
    subject: str             # Email subject
    body: str                # Email body content
    payload: Dict[str, Any] = {}  # Optional extra information

class NotificationEvent(BaseModel):
    # Structure for a notification event from the broker. Allows handling different types of events.
    event_type: str          # Type of the event (e.g., "email_sent")
    data: EmailSchema        # The email data associated with the event