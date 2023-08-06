import json
from datetime import datetime
from .models.cloudevents import SmsServiceBusMessage

def sms(message):
    parsed_json = json.loads(message)
    return SmsServiceBusMessage(**parsed_json)

def create_sms(id, recipient, sender, content, options=None):
    try:
        return json.dumps({
            "specversion": "1.0.0",
            "type": "servicebusevent",
            "id": id,
            "time": datetime.now(),
            "datacontenttype": "application/json",
            "data": {
                "type": "sms",
                "content": content,
                "recipient": recipient,
                "sender": sender
            },
            "options": options,
        }, default=str)
    except Exception as e:
        print(e)