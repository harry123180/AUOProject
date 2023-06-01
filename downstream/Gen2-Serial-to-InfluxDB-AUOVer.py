import serial  # 引用pySerial模組

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


# You can generate an API token from the "API Tokens Tab" in the UI
token = "690WrHMhfk0DqySA1v86ze5iMo7DzWRItI7jTmh_EicUEAomd8Rz6t8XvR62_miOt7xzYURpF1qCnDCgA3SoyA=="
org = "K1082"
bucket = "MonitorSystem"

dataname = ["num","Mean_X","Mean_Y","Mean_Z","Std_X","Std_Y","Std_Z","RMS_X","RMS_Y","RMS_Z","Kurtosis_X","Kurtosis_Y","Kurtosis_Z","fundamental_freq_X","fundamental_freq_Y","fundamental_freq_Z","tp_X","tp_Y","tp_Z"]
dataname = ["num","StrainA","StrainA","Mean_Z","Std_X","Std_Y","Std_Z","RMS_X","RMS_Y","RMS_Z","Kurtosis_X","Kurtosis_Y","Kurtosis_Z","fundamental_freq_X","fundamental_freq_Y","fundamental_freq_Z","tp_X","tp_Y","tp_Z"]
COM_PORT = '/dev/ttyUSB0'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
#Mean_[0],Mean_[1],Mean_[2],Std_[0],Std_[1],Std_[2],RMS_[0],RMS_[1],RMS_[2],Kurtosis_,fundamental_freq[0],fundamental_freq[1],fundamental_freq[2],tp_[0],tp_[1],tp_[2]

try:
    while True:
        now = datetime.now()
        while ser.in_waiting:          # 若收到序列資料…
            now = datetime.now()
            nowTime = now.strftime("%Y_%m_%d %H:%M:%S")
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            #print('接收到的原始資料：', data_raw)
            #print('接收到的資料：', data)
            try:
                new = data.split()
                with InfluxDBClient(url="https://influxdb.lwcjacky.com/", token=token, org=org) as client:
                    write_api = client.write_api(write_options=SYNCHRONOUS)
                    print(new)
                    for i in range(19):
                        if(new[0]!='4'):
                            # data_db = "mem,host=host1 " + dataname[i] + "=" + new[i]
                            # data_db = "mem,host=" + new[0] + " " + dataname[i] + "=" + " " + new[i]
                            data_db = "mem,host=" + new[0] + " " + dataname[i] + "=" + new[i]
                        else:
                            data_db = "mem,host=" + new[0] + " " + dataname2[i] + "=" + new[i]
                        try:
                            write_api.write(bucket, org, data_db)

                        except:
                            print("write fail")
                            pass
            except:
                print("connect fail")

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')

