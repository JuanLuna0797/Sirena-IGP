import socket
from multiprocessing import Queue
import pickle
from threading import Thread
import time
from paho.mqtt import client as mqtt_client
import json

#TCP client class, for delivering event info to SASPE server node
class mqttsub:
   #init params
   #def __init__(self,serverip,serverport,clientid,topic,msgbuffer,username="saspe",password="sasperuclient",tcpbuffer=1024):
   def __init__(self,serverip,serverport,clientid,topic,msgbuffer,username,password,tcpbuffer=1024):
      self.broker = serverip
      self.port = serverport
      self.clientid = clientid
      self.username = username
      self.password = password
      self.topic = topic
      self.buffer = tcpbuffer
      self.inbuffer = msgbuffer
      self.thread = Thread(target = self.start)
      self.thread.start()

   def start(self,):
      while True:
         try:
            self.client = self.connect_mqtt()
            break
         except Exception as e:
            print('unable to connect, retrying in 60 sec')
            print(e)
            time.sleep(60)
            continue

      self.client.on_log = self.on_log
      self.subscribe(self.client)
      self.client.loop_forever()  

   def connect_mqtt(self,) -> mqtt_client:
      def on_connect(client, userdata, flags, rc):
         if rc == 0:
            print("Connected to MQTT Broker!")
            self.subscribe(client)
         else:
            print("Failed to connect, return code %d\n", rc)

      client = mqtt_client.Client(self.clientid)
      #client.username_pw_set(self.username, self.password)
      client.on_log = self.on_log
      client.on_connect = on_connect
      client.connect(self.broker, self.port)
      self.subscribe(client)
      return client

   def on_log(self,client,userdata,level,buf):
      print('log: ',buf)

   def subscribe(self,client: mqtt_client):
      def on_message(client,userdata,msg):
         #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
         self.inbuffer.put(json.loads(msg.payload.decode()))

      client.subscribe(self.topic)
      client.on_message = on_message
