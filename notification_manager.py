import os
from twilio.rest import Client


#initialize global variables
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_NUM = os.getenv('TWILIO_NUM')
PERSONAL_NUM = os.getenv('PERSONAL_NUM')


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def send_sms(self, message):
        '''Send sms message via twilio API.'''
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_NUM,
            to=PERSONAL_NUM,
        )
        print(message.sid)