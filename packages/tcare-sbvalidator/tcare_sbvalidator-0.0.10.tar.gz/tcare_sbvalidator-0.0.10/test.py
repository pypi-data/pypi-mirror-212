import asyncio
# from src.tcare_sbvalidator import sb_validator
from src.tcare_sbvalidator.sms_handler import Sms

from dotenv import dotenv_values
config = dotenv_values(".env")

NAMESPACE = config['NAMESPACE']
CONNECTION_STRING = config['CONNECTION_STRING']
TOPIC = config['TOPIC']

async def main():
    handler = Sms(connection_string=CONNECTION_STRING)

    json = handler.build_json(
        id="123",
        recipient="+15713024423",
        sender="+18722782273",
        content="Helloo!"
    )

    await handler.publish_message(NAMESPACE, TOPIC, json)

asyncio.run(main())