import json
import asyncio
from aio_pika import connect_robust, IncomingMessage
import os
from dotenv import load_dotenv

from app.services import EmailService
from app.schemas import NotificationEvent

# Load environment variables from a .env file
load_dotenv()

# This function handles messages received from the broker
async def on_message(message: IncomingMessage):
    # Handles broker messages. Runs every time a new message arrives in the queue.
    async with message.process():
        try:
            print("INFO: New message received.")
            data = json.loads(message.body.decode())    # Decode the message body and convert from JSON to Python dict
            event = NotificationEvent(**data)           # Create a NotificationEvent object from the data

            print(f"INFO: Processing event of type '{event.event_type}'")

            # Create the email service and send the email from the event data
            email_service = EmailService()
            await email_service.send_email(event.data)

        except Exception as e:
            print(f"ERROR: Failed to process the message. Error: {e}")

# This function starts the consumer that listens to the broker
async def start_consumer():
    # Connects to the message broker and waits for messages.
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    #rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    try:
        # Connect to RabbitMQ
        connection = await connect_robust(rabbitmq_url)
        channel = await connection.channel()

        # Declare a queue to subscribe to
        queue = await channel.declare_queue("notifications-email-queue", durable=True)
        print("INFO: Consumer connected to RabbitMQ and waiting for messages...")

        # Start consuming messages with the on_message handler
        await queue.consume(on_message, no_ack=False)
        await asyncio.Future()                          # Keeps the consumer running forever
    except Exception as e:
        print(f"ERROR: Could not connect to the message broker. Error: {e}")