# -*- coding: utf-8 -*-
"""producer_gtfs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10pevN6jK7QXDus9DnDwCQ09M785lZdGW
"""

#!pip install --upgrade gtfs-realtime-bindings
#!pip install gtfs-realtime-bindings==0.0.7
#!pip install confluent_kafka
#!pip install --user protobuf3-to-dict

import time
from google.protobuf.json_format import MessageToJson
from confluent_kafka import Producer
from google.transit import gtfs_realtime_pb2
import json
import ast
#from google.colab import drive
import os
import csv
import sys
import pathlib
from kafka import KafkaProducer
from time import sleep
#pathlib.Path().absolute()
#drive.mount('/content/gdrive')


#arr = os.listdir()
#print(arr)

from google.protobuf.json_format import MessageToJson
#from protobuf_to_dict import protobuf_to_dict
#import urllib.request
from urllib.request import Request, urlopen


feed = gtfs_realtime_pb2.FeedMessage()
header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
request = Request('http://www.rtd-denver.com/google_sync/VehiclePosition.pb', headers=header)
response = urlopen(request).read()
feed.ParseFromString(response)

def first_response():
  data_file = open('/home/ec2-user/jsonoutput.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  with open("/home/ec2-user/sample.json", "w") as outfile:
    count = 0
    for entity in feed.entity:
      tu = entity.trip_update
      vid = tu.vehicle.id
      tid = tu.trip.trip_id
      data = MessageToJson(entity)
      update_json = json.loads(json.dumps(data))
      outfile.write(update_json)
      header = {'id','timestamp','longitude','latitude'}
      if count == 0:
        csv_writer.writerow(header)
      my_dict = ast.literal_eval(update_json)
      count += 1
      my_list = list(my_dict.values())
      id = my_list[0]
      inner_dict = my_list[1]
      #print(inner_dict['trip'])
      #tripId = inner_dict['trip']['tripId']
      #routeId = inner_dict['trip']['routeId']
      timestamp = inner_dict['timestamp']
      print(timestamp)
      latitude = inner_dict['position']['latitude']
      longitude = inner_dict['position']['longitude']
      all_togather = [id,timestamp,longitude,latitude]
      print(all_togather)
      csv_writer.writerow(all_togather)
      #print(my_dict.values())
      outfile.write("\n")

first_response()
time.sleep(40)

feed = gtfs_realtime_pb2.FeedMessage()
header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
request = Request('http://www.rtd-denver.com/google_sync/VehiclePosition.pb', headers=header)
response = urlopen(request).read()
feed.ParseFromString(response)

def first_response_30():
  data_file = open('/home/ec2-user/jsonoutput_30.csv', 'w', newline='')
  csv_writer = csv.writer(data_file)
  with open("/home/ec2-user/sample_30.json", "w") as outfile:
    count = 0
    for entity in feed.entity:
      tu = entity.trip_update
      vid = tu.vehicle.id
      tid = tu.trip.trip_id
      data = MessageToJson(entity)
      update_json = json.loads(json.dumps(data))
      outfile.write(update_json)
      header = {'id','timestamp','longitude','latitude'}
      if count == 0:
        csv_writer.writerow(header)
      my_dict = ast.literal_eval(update_json)
      count += 1
      my_list = list(my_dict.values())
      id = my_list[0]
      inner_dict = my_list[1]
      #print(inner_dict['trip'])
      #tripId = inner_dict['trip']['tripId']
      #routeId = inner_dict['trip']['routeId']
      timestamp = inner_dict['timestamp']
      print(timestamp)
      latitude = inner_dict['position']['latitude']
      longitude = inner_dict['position']['longitude']
      all_togather = [id,timestamp,longitude,latitude]
      print(all_togather)
      csv_writer.writerow(all_togather)
      #print(my_dict.values())
      outfile.write("\n")

first_response_30()

prod = KafkaProducer(bootstrap_servers=['b-1.mskcsv.*****.c4.kafka.eu-north-1.amazonaws.com:9092'])

f = open("/home/ec2-user/sample.csv","r")

for msg in f:
    data=msg
    prod.send('awskafkatopic',json.dumps(data).encode('utf-8'))
    sleep(2)
    print(data)
    #prod.flush()
    #print("Hello world")



prod = KafkaProducer(bootstrap_servers=['b-1.mskcsv.*****.c4.kafka.eu-north-1.amazonaws.com:9092'])

f = open("/home/ec2-user/sample_30.csv","r")

for msg in f:
    data=msg
    prod.send('awskafkatopic30',json.dumps(data).encode('utf-8'))
    sleep(2)
    print(data)
    #prod.flush()
    #print("Hello world")