import serial  # 引用pySerial模組

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "F_Z2p7hyMRIP6HRd_HVlHmrYbf7erFQmUFWxJAaywjDk-0VxF-jp0Oavm8-rpEQROm898giDNV0IYyNUBjaoaw=="
org = "AUO"
bucket = "MonitorSystem"
dataname = ["num","Mean_X","Mean_Y","Mean_Z","Std_X","Std_Y","Std_Z","RMS_X","RMS_Y","RMS_Z","Kurtosis_X","Kurtosis_Y","Kurtosis_Z","fundamental_freq_X","fundamental_freq_Y","fundamental_freq_Z","tp_X","tp_Y","tp_Z"]
COM_PORT = 'COM4'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
#Mean_[0],Mean_[1],Mean_[2],Std_[0],Std_[1],Std_[2],RMS_[0],RMS_[1],RMS_[2],Kurtosis_,fundamental_freq[0],fundamental_freq[1],fundamental_freq[2],tp_[0],tp_[1],tp_[2]
try:
    
    while True:
        while ser.in_waiting:          # 若收到序列資料…
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            print('接收到的原始資料：', data_raw)
            print('接收到的資料：', data)
            new = data.split()
            with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                for i in range(19):
                    #data_db = "mem,host=host1 " + dataname[i] + "=" + new[i]
                    data_db = "mem,host="+new[0]+" " + dataname[i] + "=" + new[i]
                    #data_db = "mem,host=" + new[0] + " " + dataname[i] + "=" + " " + new[i]
                    write_api.write(bucket, org, data_db)


except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')


