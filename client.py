from notifier import mqttsub
import time
import pickle
import sys
import json
#import RPi.GPIO as GPIO
from multiprocessing import Queue
from math import *
import os

def distance(lon1, lat1, lon2, lat2):
    """
    calcula la distancia entre 2 puntos en la tierra a partir de las coordenadas de
    latitud y longitud
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. 
    return c * r

config_dir = '/home/juanluna/Desktop/SIRENA/'

#Reading config file
f = open(config_dir+'config.json','r')
params = json.load(f)
f.close()

time.sleep(10)
lat = params['location']['lat']
lon = params['location']['lon']
msgbuffer = Queue(50)

#client = TCPClient('190.187.237.140', 5007, 'PISI001')
#client1 = mqttsub('190.187.237.140',5007,'PISI006','saspe/sirene/main',msgbuffer)
#client2 = mqttsub('190.187.237.140',5007,'PISI007','saspe/sirene/test',msgbuffer)

id = params['network']['ip']
port = params['network']['port']
client_id = params['mqtt']['client_id']
topics = params['mqtt']['topics']
topic = params['mqtt']['topic1']
topic_test = params['mqtt']['topic2']
user = params['mqtt']['user']
pwd = params['mqtt']['pwd']
tcp_buff = params['mqtt']['tcpbuff']
audio_file = params["alarm"]["file"]
audio_vol = params["alarm"]["volume"]

topic_mant="home/sirena/mant/"+client_id
vol=int((audio_vol*32768)/100)#Setting up the volume


#client1 = mqttsub(id,port,client_id,topic,msgbuffer)
#client2 = mqttsub(id,port,client_id,topic_test,msgbuffer)
client1 = mqttsub(id,port,client_id,topic,user,pwd,msgbuffer)
client2 = mqttsub(id,port,client_id,topic_test,user,pwd,msgbuffer)
#client2 = mqttsub(id,port,'PISI007','home/sirena/test',msgbuffer)

while True:
   data = msgbuffer.get()

   dist = distance(data['longitud'],data['latitud'],lon,lat)
   if data['impacto']*1.2 >= dist:
      print('Sending alarm to megaphone')
      #playsound('/home/pi/Desktop/SIRENA/'+audio_alarm)
      os.system("mpg123 -f -"+str(vol)+" "+audio_file)
   else:
      pass
   
   '''elif data['remote'] == "OFF":
      audio_file = data['file']
      audio_vol = data['vol']
      vol=int((audio_vol*32768)/100)#Setting up the volume
   elif data['remote'] == "ON":
      os.system("python3 ~/SSH/remote_tunnel.py > /dev/null 2>&1 & disown")'''