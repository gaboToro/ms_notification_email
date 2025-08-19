import asyncio
import json
from aio_pika import connect_robust, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

async def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    # rabbitmq_url = "amqp://guest:guest@localhost/"

    print("INFO: Connecting to RabbitMQ...")
    connection = await connect_robust(rabbitmq_url)

    async with connection:
        channel = await connection.channel()

        # Message simulating an event from another microservice
        test_payload = {
            "event_type": "order_created",
            "data": {
                "to_email": "test@gmail.com",
                "subject": "Your order has been created",
                "body": "<h1>Hello!</h1><p>Thank you for your purchase.</p>",
                "payload": {
                    "order_id": "12345",
                    "customer_name": "User #1"
                }
            }
        }

        message_body = json.dumps(test_payload).encode()

        # Publish the message to the queue that your microservice listens to
        print("INFO: Publishing test message...")

        # Create a Message object before publishing
        message_to_publish = Message(body=message_body)

        await channel.default_exchange.publish(
            message=message_to_publish,  # Now passing a Message object
            routing_key="notifications-email-queue"
        )
        print("INFO: Message published successfully.")

if __name__ == "__main__":
    asyncio.run(main())
