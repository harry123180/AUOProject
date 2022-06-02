import paho.mqtt.client as mqtt

# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    #client.subscribe("sensor/X")

# 接收訊息（接收到 PUBLISH）的回呼函數
def on_message(client, userdata, msg):
    #print("[{}]: {}".format(msg.topic, str(msg.payload)))
    print(type(msg.topic),msg.topic[0],len(msg.topic))
    pass
def on_message_X(mosq, obj, msg):
    #print("[{}]: {}".format(msg.topic, str(msg.payload)))
    pass
def on_message_Y(mosq, obj, msg):
    #print("[{}]: {}".format(msg.topic, str(msg.payload)))
    pass
def on_message_Z(mosq, obj, msg):
    #print("[{}]: {}".format(msg.topic, str(msg.payload)))
    pass
# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定建立連線回呼函數
client.on_connect = on_connect
#摳被函數
client.message_callback_add('sensor/X', on_message_X)
client.message_callback_add('sensor/Y', on_message_Y)
client.message_callback_add('sensor/Z', on_message_Z)
# 設定接收訊息回呼函數
client.on_message = on_message

# 設定登入帳號密碼（若無則可省略）
client.username_pw_set("test","vcAnn8GZ")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("lwcjacky.myds.me", 1883)
client.subscribe("sensor/#")
# 進入無窮處理迴圈

client.loop_forever()
