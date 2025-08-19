# Description: Contains the logic to send emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

from app.schemas import EmailSchema

# Load environment variables from a .env file
load_dotenv()

class EmailService:
    # Service to send emails. Uses environment variables to configure the SMTP server.
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")         # SMTP server address
        self.smtp_port = os.getenv("SMTP_PORT")             # SMTP server port
        self.smtp_user = os.getenv("SMTP_USER")             # SMTP login username
        self.smtp_password = os.getenv("SMTP_PASSWORD")     # SMTP login password
        self.sender_email = os.getenv("SENDER_EMAIL")       # Sender's email address

    async def send_email(self, email_data: EmailSchema):
        # Check if all SMTP configurations are present
        if not all([self.smtp_server, self.smtp_user, self.smtp_password, self.sender_email]):
            print("ERROR: SMTP configuration incomplete. Email will not be sent.")
            return
        print(f"INFO: Trying to send email to {email_data.to_email}...")

        # Create a multipart email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = email_data.subject   # Email title
        msg["From"] = self.sender_email       # Sender
        msg["To"] = email_data.to_email       # Recipient

        # Assume the email body is HTML
        part1 = MIMEText(email_data.body, "html")
        msg.attach(part1)  # Attach the body to the message

        try:
            # Connect to the SMTP server using the .env variable port
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()                                                           # Start TLS encryption
                server.login(self.smtp_user, self.smtp_password)                            # Login to SMTP
                server.sendmail(self.sender_email, email_data.to_email, msg.as_string())    # Send email
            print(f"INFO: Email successfully sent to {email_data.to_email}")
        except Exception as e:
            print(f"ERROR: Failed to send email to {email_data.to_email}. Error: {e}")