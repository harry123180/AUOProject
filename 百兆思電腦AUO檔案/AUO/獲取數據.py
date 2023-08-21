
#import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "eQ5UWiaZGFzzHpNgLpMPuaqTR0UM3lPxjGYc3ykeT-t0vIIv_7c4ye_QzwUC3CWhCadcARmm8-c_SzAgbcGzwA=="
org = "AUO"
bucket = "OVEN"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    query = """from(bucket: "OVEN") |> range(start: -10s)|> filter(fn: (r) => r["_measurement"] == "mem") """
    print(type(query))
    tables = client.query_api().query(query, org=org)
    for table in tables:
        for record in table.records:
            print(record['_value'])
            print(record)
            print(type(record))
client.close()

