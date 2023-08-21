# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 12:11:25 2023

@author: Admin
"""
import random
import code1
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
class Database():
    def __init__(self,tokens,url,org,bucket):
        self.tokens=tokens
        self.url=url
        self.org=org
        self.bucket=bucket
        self.client= InfluxDBClient(url=self.url, token=self.tokens, org=self.org) 
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        
    def getData(self,dataname,time_range,node):
        query = """from(bucket: "%s")
        |> range(start: %ss)
        |> filter(fn: (r) => r["_measurement"] == "%s") """%(self.bucket,time_range,node)
        tables = self.client.query_api().query(query, org=self.org)
        for table in tables:
            for record in table.records:
                print( record['_value'],"值")
    def pushData(self,dataname,datanode,datavalue):
        point = Point("mem") \
        .tag("host", datanode) \
        .field(dataname, datavalue)\
        .time(datetime.utcnow(), WritePrecision.NS)
        print(point)
        self.write_api.write(self.bucket, self.org, point)
        print("寫入成功")
    def pushRandom_Data(self,dataname,datanode,upper,lower):
        random_float = random.uniform(lower, upper)
        rounded_float = round(random_float, 2)
        self.pushData(dataname, datanode, rounded_float)
        print("成功")
    def pushAnomalyRate(self):
        self.pushData("Anomaly rate", "host1", code1.fun([1,1,1,1,1,1,1]))
        