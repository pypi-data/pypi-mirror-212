import json, asyncio
from datetime import datetime
from .models.cloudevents import SmsServiceBusMessage
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

class Sms:

    def __init__(self, connection_string=None):
        self.connection_string = connection_string

    def validate_json(self, message):
        parsed_json = json.loads(message)
        return SmsServiceBusMessage(**parsed_json)

    def build_json(self, id, recipient, sender, content, options=None):
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

    async def publish_message(self, namespace, topic, message_json, cred=DefaultAzureCredential()):
        if self.connection_string:
            client = ServiceBusClient.from_connection_string(self.connection_string)
        else:
            client = ServiceBusClient(namespace, cred)
        async with client:
            async with client.get_topic_sender(topic) as sender:
                msg = ServiceBusMessage(message_json)
                await sender.send_messages(msg)
                print(f"message sent with content: {message_json}")
