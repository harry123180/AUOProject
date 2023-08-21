from datetime import datetime
#import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "eQ5UWiaZGFzzHpNgLpMPuaqTR0UM3lPxjGYc3ykeT-t0vIIv_7c4ye_QzwUC3CWhCadcARmm8-c_SzAgbcGzwA=="
org = "AUO"
bucket = "OVEN"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("mem") \
    .tag("host", "host1") \
    .field("used_percent", 23.43234543) \
    .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point)
client.close()

