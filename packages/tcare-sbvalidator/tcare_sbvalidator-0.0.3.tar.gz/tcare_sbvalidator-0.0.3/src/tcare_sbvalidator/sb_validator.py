import json
from pydantic import BaseModel

# SMS
class SmsServiceBusMessage(BaseModel):
    recipient_number: str
    message: str
    message_type: str

def sms(message):
    parsed_json = json.loads(message)
    return SmsServiceBusMessage(**parsed_json)