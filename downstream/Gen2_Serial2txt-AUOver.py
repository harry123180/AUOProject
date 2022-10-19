import serial  # 引用pySerial模組
from datetime import datetime



dataname = ["num","Mean_X","Mean_Y","Mean_Z","Std_X","Std_Y","Std_Z","RMS_X","RMS_Y","RMS_Z","Kurtosis_X","Kurtosis_Y","Kurtosis_Z","fundamental_freq_X","fundamental_freq_Y","fundamental_freq_Z","tp_X","tp_Y","tp_Z"]
COM_PORT = '/dev/ttyUSB0'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
#Mean_[0],Mean_[1],Mean_[2],Std_[0],Std_[1],Std_[2],RMS_[0],RMS_[1],RMS_[2],Kurtosis_,fundamental_freq[0],fundamental_freq[1],fundamental_freq[2],tp_[0],tp_[1],tp_[2]
now = datetime.now()
MD_time = now.strftime("%M_%d")
H_time = now.strftime("%H")
path = MD_time+"_"+H_time+".txt"
sample=0 #一個檔案等於一個樣本
try:
    f = open(path, 'w')
except:
    pass
try:
    while True:
        now = datetime.now()

        MD_time = now.strftime("%Y-%m-%d,%H:%M")#年-月-日,時:分
        M_time = now.strftime("%M")#分鐘
        if(int(M_time) ==0):
            while(1):
                try:#時間到 把檔案關掉
                    f.close()
                    break
                except:#如果關不掉在當前的檔案寫入關不掉的錯誤訊息
                    f.write("error file can't close")
                    pass#持續迴圈直到關掉
            sample+=1 #樣本數遞增
            path = str(sample)+"-" + MD_time+".txt"#新檔名
            try:
                f = open(path, 'w')
                #當新檔案開啟時，先寫入數據名稱在第一行
                f.write("timestamp")#時間戳記 配合Edge Impulse File Format使用
                for i in range(len(dataname)):
                    f.write(dataname[i])
                f.write("\n")
            except:
                #如果開啟失敗就pass
                pass
        while ser.in_waiting:          # 若收到序列資料…
            now = datetime.now()
            nowTime = now.strftime("%M:%S")
            data_raw = ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            #print('接收到的原始資料：', data_raw)
            print('接收到的資料：', data)
            f.write(nowTime + " " +data)

except KeyboardInterrupt:
    ser.close()    # 清除序列通訊物件
    print('再見！')


