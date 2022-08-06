#
import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.0.145", 1883, 60)
for i in range(3):
    client.publish('test1', payload=i, qos=0, retain=False)
    print(f"send {i} to a/b")
    time.sleep(1)

client.loop_forever()