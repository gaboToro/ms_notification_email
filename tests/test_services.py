import pytest
import smtplib
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv

from app.schemas import EmailSchema
from app.services import EmailService

# Load environment variables for configuration
load_dotenv()

@pytest.fixture
def email_service():
    # Fixture that returns an instance of EmailService.
    return EmailService()

@pytest.fixture
def mock_smtp():
    #Fixture that simulates the SMTP connection and sending emails."""
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_server = MagicMock()
        # When using 'with', the __enter__ method returns the mock server
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        yield mock_server


@pytest.mark.asyncio
async def test_send_email_success(email_service, mock_smtp):
    # Test that send_email executes successfully.
    # Create a sample email object
    email_data = EmailSchema(
        to_email="test@gmail.com",
        subject="Test Subject",
        body="<h1>Test Body</h1>"
    )

    # Call the method we are testing
    await email_service.send_email(email_data)

    mock_smtp.starttls.assert_called_once()             # Verify that TLS encryption was started
    mock_smtp.login.assert_called_once_with(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD")) # Verify that login was called with correct credentials
    mock_smtp.sendmail.assert_called_once()             # Verify that sendmail was called to send the email

@pytest.mark.asyncio
async def test_send_email_failure(email_service, mock_smtp):
    # Simulate an error when trying to send the email
    mock_smtp.sendmail.side_effect = smtplib.SMTPException("Connection error")

    # Create a sample email object
    email_data = EmailSchema(
        to_email="test@gmail.com",
        subject="Test Subject",
        body="<h1>Test Body</h1>"
    )

    await email_service.send_email(email_data)  # Call the method; it should not raise an exception, only print an error
    mock_smtp.sendmail.assert_called_once()     # Verify that sendmail was attempted once