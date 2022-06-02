from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import paho.mqtt.client as mqtt

# You can generate an API token from the "API Tokens Tab" in the UI
token = "99Bzuifog7FWRvvuAHbiMEy4xwtDmYEt-y9oyfiyqj-ubAB8KA5k2GMgZP1ACPJPZuoWYTvgCdoHg5dG2HqyXQ=="
org = "harry"
bucket = "MonitorSystem"
# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
def on_message(client, userdata, msg):
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        print("[{}]: {}".format(msg.topic, str(msg.payload)))
        try:
            load = str(float(msg.payload))
            data = "mem,host=host1 "+msg.topic+"=" + load
            print(data)
            write_api.write(bucket, org, data)
        except:
            pass
    pass
# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定建立連線回呼函數
client.on_connect = on_connect
#摳被函數
#client.message_callback_add('sensor/X', on_message_X)
#client.message_callback_add('sensor/Y', on_message_Y)
#client.message_callback_add('sensor/Z', on_message_Z)
# 設定接收訊息回呼函數
client.on_message = on_message

# 設定登入帳號密碼（若無則可省略）
client.username_pw_set("test","vcAnn8GZ")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("lwcjacky.myds.me", 1883)
client.subscribe("sensor/#")
# 進入無窮處理迴圈

client.loop_forever()







