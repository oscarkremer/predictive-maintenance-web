import os
from flask import url_for
from server import db
from server.models import Company, User


if __name__=='__main__':
    db.drop_all()
    db.create_all()
    for filename in os.listdir('data/client'):
        if filename != '0':
            os.system('sudo rm -rvf data/client/{}'.format(filename))
    company = Company(name='Garten Automation', address='Av. Herbert Hadler, 1367', 
        city='Pelotas', country='Brasil', telephone='+55 (53) 3028-9001')
    db.session.add(company)
    db.session.commit()
