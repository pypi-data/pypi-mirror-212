import asyncio
# from src.tcare_sbvalidator import sb_validator
from src.tcare_sbvalidator.sms_handler import Sms

from dotenv import dotenv_values
config = dotenv_values(".env")

NAMESPACE = config['NAMESPACE']
TOPIC = config['TOPIC']

# msg = sb_validator.create_sms("jnsdj24", "123", "456", "Well hey!")
# print(sb_validator.sms(msg).data)

async def main():
    handler = Sms()

    json = handler.build_json(
        id="123",
        recipient="+15713024423",
        sender="+18722782273",
        content="Hey!"
    )

    await handler.publish_message(NAMESPACE, TOPIC, json)

asyncio.run(main())