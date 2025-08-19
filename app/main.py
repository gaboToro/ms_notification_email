from fastapi import FastAPI, BackgroundTasks, status
import asyncio

from app.consumer import start_consumer
from app.services import EmailService
from app.schemas import EmailSchema

# Create the FastAPI application
app = FastAPI(title="Email Notifications Microservice")

# Global instance of the email service
email_service = EmailService()

# This function runs when the application starts
@app.on_event("startup")
async def startup_event():
    # Event triggered when the application starts. Starts the broker consumer in the background.
    print("INFO: Starting microservice...")
    # Run the consumer in the background so it does not block the API
    asyncio.create_task(start_consumer())


# Simple endpoint to check if the microservice is running
@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    # Health check endpoint for the microservice.
    return {"status": "ok", "service": "notifications-email"}

# Endpoint to send an email via HTTP
@app.post("/send-email", status_code=status.HTTP_202_ACCEPTED)
async def send_email_api(email_data: EmailSchema, background_tasks: BackgroundTasks):
    # Add the email sending task to run in the background
    background_tasks.add_task(email_service.send_email, email_data)
    return {"message": "Email request accepted, processing in background."}
