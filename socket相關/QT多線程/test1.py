from datetime import datetime
import random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client import write_api
from influxdb_client.client.write_api import SYNCHRONOUS
import time
# You can generate an API token from the "API Tokens Tab" in the UI
token = "6d8_CxREXOK_5Nv09YyHYI6yvgpWsy6ETrNGmbPL-n-vGjoWs2cMxMG9TK-CM7TuHXW6yFUwVsQVIaD4_HuQQg=="
org = "harry"
bucket = "ESP"
while (True):
    i = 0
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:

        write_api = client.write_api(write_options=SYNCHRONOUS)
        i+=1
        data = "mem,host=host1 used_percent="+str(random.randint(-1001,1000))
        write_api.write(bucket, org, data)
        time.sleep(0.01)
        print(str(i))
client.close()