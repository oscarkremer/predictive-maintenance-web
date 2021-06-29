import requests
import random

def main(url):
    acX = 9.8+0.5*random.random()
    down_acX = acX-0.2-0.1*random.random()
    up_acX = acX+0.2+0.1*random.random()
    acY = 0.5*random.random()
    down_acY = acY-0.2-0.1*random.random()
    up_acY = acY+0.2+0.1*random.random()
    acZ = 0.5*random.random()
    up_acZ = acZ+0.2+0.1*random.random()
    down_acZ = acZ-0.2-0.1*random.random()
    gyX = 0.5*random.random()
    up_gyX = gyX+0.2+0.1*random.random()
    down_gyX = gyX-0.2-0.1*random.random()
    gyY = 0.5*random.random()
    up_gyY = gyY+0.2+0.1*random.random()
    down_gyY = gyY-0.2-0.1*random.random()
    gyZ = 9.8+0.5*random.random()
    down_gyZ = acX+0.2+0.1*random.random()
    up_gyZ = acX+0.2+0.1*random.random()
    temperature = 14+0.5*random.random()
    up_temperature = temperature+0.5+0.1*random.random()
    down_temperature = temperature-0.5+0.1*random.random()
 
    data = {'AcX': acX, 'DownAcX': down_acX,'UpAcX': up_acX,
        'AcY': acY,'DownAcY': down_acY,'UpAcY': up_acY,
        'AcZ': acZ, 'DownAcZ': down_acZ, 'UpAcZ': up_acZ, 
        'GyX': gyX, 'DownGyX': down_gyX, 'UpGyX': up_gyX,
        'GyY': gyY, 'DownGyY': down_gyY, 'UpGyY': up_gyY,
        'GyZ': gyZ, 'DownGyZ': down_gyZ,'UpGyZ': up_gyZ,
        'Tmp': temperature, 'DownTmp': down_temperature,'UpTmp': up_temperature}
    response = requests.post(url, data = data)


if __name__=='__main__':
    try:
        main('http://0.0.0.0:5000/request-data')
    except Exception as e:
        print(e)