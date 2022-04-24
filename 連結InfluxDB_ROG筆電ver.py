from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "1W7iej02NfAdH6xYrU1gjIvgavP7XI0enWeyUUYDRbO4OWI1ETXYCVVdbjBmfM3bYEIf8A-cpZ757FKnKyNhCA=="
org = "harry"
bucket = "b1"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = "mem,host=host1 test=23.43234543 "
    write_api.write(bucket, org, data)
    data = "mem,host=host1 test1=23.43234543 "
    write_api.write(bucket, org, data)

