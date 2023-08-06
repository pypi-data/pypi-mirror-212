import json
from src.tcare_sbv import sb_validator

msg = {
    "recipient_number": "123456",
    "message": "hello",
    "message_type": "yo"
}

msg2 = json.dumps(msg)

print(sb_validator.sms(msg2))