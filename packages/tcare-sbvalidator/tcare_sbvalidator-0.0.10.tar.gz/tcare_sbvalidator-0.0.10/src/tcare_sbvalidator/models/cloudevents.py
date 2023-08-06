from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# TCARE Cloud Events
class Options(BaseModel):
    expedite: bool

class TcareCloudEvent(BaseModel):
    specversion: str
    type: str
    id: str
    time: datetime
    datacontenttype: str
    options: Optional[Options] = None

# SMS
class SmsData(BaseModel):
    type: str
    content: str
    recipient: str
    sender: str

class SmsServiceBusMessage(TcareCloudEvent):
    data: SmsData