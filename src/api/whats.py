from config import BaseConfig
from twilio.rest import Client


if __name__=='__main__':

    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client()

    # this is the Twilio sandbox testing number
    from_whatsapp_number='whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number='whatsapp:+555391095183'

    client.messages.create(body='Ahoy, world!',
                        from_=from_whatsapp_number,
                        to=to_whatsapp_number)
