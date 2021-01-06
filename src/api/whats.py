from app import db
from app.models import *
from twilio.rest import Client
from config import BaseConfig

def twillio_message():
    try:
        client = Client()
        from_whatsapp_number='whatsapp:+14155238886'
        outlier = Anomaly.query.filter(Anomaly.behavior=='Outlier').count()
        freq = Anomaly.query.filter(Anomaly.behavior=='Frequency').count()
        deep = Anomaly.query.filter(Anomaly.behavior=='DeepAnT').count()
        total = outlier + freq + deep
        acceleration = Anomaly.query.filter(Anomaly.variable=='Acceleration').count()
        rotation = Anomaly.query.filter(Anomaly.variable=='Rotation').count()
        temperature = Anomaly.query.filter(Anomaly.variable=='Temperature').count()
        message = 'Hello, I\'am your intelligent maintenance assistant and I have a daily report for you. \n Today a total of {} anomalies have been detected, {} of them arised from acceleration readings, {} from rotation and {} from temperature.'.format(total, acceleration, rotation, temperature)
        for user in users:
            to_whatsapp_number='whatsapp:{}{}'.format(user.telephone[:5], user.telephone[6:])
            client.messages.create(body=message,
                from_=from_whatsapp_number,
                            to=to_whatsapp_number)
    except Exception as e:
        print('excecao twillio - {}'.format(e))

if __name__ == '__main__':
    twilli_message()
    