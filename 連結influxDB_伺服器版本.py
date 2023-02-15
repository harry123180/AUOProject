from datetime import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
# You can generate an API token from the "API Tokens Tab" in the UI
token = "VLJI0v-iKBTAmclC9KWPYEwN4swa6mITR-LJK1uw3c1_LDzwgroQ-eliFQcq1-YJc6G1FdL_ULa-z2U1aKe5mw=="
org = "K1082"
bucket = "test"
frq=[]
for i in range(128):
    frq.append("bin"+str(i))
while(True):
    with InfluxDBClient(url="http://125.229.142.15:9453", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        data = "mem test=-23.43234543 "
        write_api.write(bucket, org, data)
        sequence = []
        sequence = ["mem,host=host1 "+frq[0]+"="+str(random.uniform(10.5, 75.5))]
        for i in range(10):
            sequence.append("mem,host=host1 "+frq[i+1]+"="+str(random.uniform(10.5, 75.5)))
        print(type(sequence))
        write_api.write(bucket, org, sequence)

        #for i in range(128):
            #sequence.append("mem,host=host1 "+frq[i]+"="+str(random.randint(0,10)))
        #data = "mem test2=-23.43234543"
        #for i in range(100):
           # data+=","+str(random.randint(0, 10))
        print(sequence)
        #write_api.write(bucket, org, data)
        #write_api.write(bucket, org, sequence)

        print("send")
        time.sleep(1)

