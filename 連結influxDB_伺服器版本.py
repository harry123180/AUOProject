from datetime import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "VLJI0v-iKBTAmclC9KWPYEwN4swa6mITR-LJK1uw3c1_LDzwgroQ-eliFQcq1-YJc6G1FdL_ULa-z2U1aKe5mw=="
org = "K1082"
bucket = "test"
while(True):
    with InfluxDBClient(url="http://125.229.142.15:9453", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        data = "mem test=-23.43234543 "
        write_api.write(bucket, org, data)
        point = Point("wifi_status") \
            .tag("SSID", "SHCT") \
            .field("rssi", 23) \
            .time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, data)
        print("send")
        time.sleep(1)

