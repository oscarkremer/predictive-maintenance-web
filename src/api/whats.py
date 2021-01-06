from app import db
from app.models import *
from twilio.rest import Client
from config import BaseConfig

def twilio_message():
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
        message = 'Hello, I\'am your intelligent maintenance assistant and I have a daily report for you. \nToday a total of {} anomalies have been detected, {} of them arised from acceleration readings, {} from rotation, {} from temperature and the remaining ones related with DeepAnT algorithm. In case of rotation and acceleration anomalies I recommend to check your device and all the surroundings, in special the screws used for support, its possible that something is loose. For temperature ones check if there is any heat sources near your equipment, and if your device has any gears or moving parts it may be helpfull to call the maintenance staff and check the lubrication.'.format(total, acceleration if acceleration!= 0 else 'none', rotation if rotation != 0 else 'none', temperature if temperature != 0 else 'none')
        for user in User.query:
            to_whatsapp_number='whatsapp:{}{}'.format(user.telephone[:5], user.telephone[6:])
            client.messages.create(body=message,
                from_=from_whatsapp_number,
                            to=to_whatsapp_number)
    except Exception as e:
        print('excecao twillio - {}'.format(e))

if __name__ == '__main__':
    twilio_message()
    
