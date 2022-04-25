from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
# You can generate an API token from the "API Tokens Tab" in the UI
token = "99Bzuifog7FWRvvuAHbiMEy4xwtDmYEt-y9oyfiyqj-ubAB8KA5k2GMgZP1ACPJPZuoWYTvgCdoHg5dG2HqyXQ=="
org = "harry"
bucket = "testDB"

import  numpy as np
file1 = open('all10000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Loading full Data set'
Samping_Rate = 10000#採樣頻率
start_sec = 0
final_sec = 611
point = (final_sec-start_sec)*200
t=  np.linspace(start_sec, final_sec,point)
Hz = np.linspace(0, Samping_Rate,point)
#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=1
for line in Lines:
    count += 1
    a = line.strip()
    if(count >=start_sec*Samping_Rate and count <= final_sec*Samping_Rate and count %1000 ==0):
        with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            data = "mem,host=host1 ch1="+a.split()[1]*k
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch2="+a.split()[1]*k
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch3="+a.split()[1]*k
            write_api.write(bucket, org, data)
            print("Data Write Count:",count,"data = ",a.split()[1]*k)
        time.sleep(0.05)





