from datetime import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from EdgeComputing import RMS,Mean,Standard_Deviation,Kurtosis,FFT,ROP
# You can generate an API token from the "API Tokens Tab" in the UI
token = "1W7iej02NfAdH6xYrU1gjIvgavP7XI0enWeyUUYDRbO4OWI1ETXYCVVdbjBmfM3bYEIf8A-cpZ757FKnKyNhCA=="
org = "harry"
bucket = "MonitorSystem"
from matplotlib import pyplot as plt
import  numpy as np
file1 = open('G:\\AUOProject\\all20000.txt', 'r')
samping_rate = 20000
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Loading full Data set'
Samping_Rate = 20000#採樣頻率
start_sec = 0
final_sec = 611
point = (final_sec-start_sec)*200
t=  np.linspace(start_sec, final_sec,point)
Hz = np.linspace(0, Samping_Rate,point)
#t=  np.linspace(0, 2,201)
count = 0
dataname = ["num","Mean_X","Mean_Y","Mean_Z",
            "Std_X","Std_Y","Std_Z",
            "RMS_X","RMS_Y","RMS_Z",
            "Kurtosis_X","Kurtosis_Y","Kurtosis_Z",
            "fundamental_freq_X","fundamental_freq_Y","fundamental_freq_Z",
            "tp_X","tp_Y","tp_Z"]
# Strips the newline character
k=1
Sig_1=[]
Sig_2=[]
Sig_3=[]
for line in Lines:
    count += 1
    a = line.strip()
    Sig_1.append(float(a.split()[1]))
    Sig_2.append(float(a.split()[2]))
    Sig_3.append(float(a.split()[3]))
    if(count >=start_sec*Samping_Rate and count <= final_sec*Samping_Rate and count %1024 ==0):
        with InfluxDBClient(url="http://192.168.1.49:8086", token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            #print( "mem,host=host1 ch1=" + str(RMS(Sig_1[0: 1023])))

            amp1,herze = FFT(Sig_1,Samping_Rate)
            amp2, herze = FFT(Sig_2, Samping_Rate)
            amp3, herze = FFT(Sig_3, Samping_Rate)
            a1,b1,c1,d1  =ROP(amp1)
            a2, b2, c2, d2 = ROP(amp2)
            a3, b3, c3, d3 = ROP(amp3)

            data = "mem,host=" + "1" + " " + "Mean_X" + "=" + str(Mean(Sig_1))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Mean_Y" + "=" + str(Mean(Sig_2))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Mean_Z" + "=" + str(Mean(Sig_3))
            write_api.write(bucket, org, data)
            #**************************************************************#
            data = "mem,host=" + "1" + " " + "Std_X" + "=" + str(Standard_Deviation(Sig_1))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Std_Y" + "=" + str(Standard_Deviation(Sig_2))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Std_Z" + "=" + str(Standard_Deviation(Sig_3))
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "RMS_X" + "=" + str(RMS(Sig_1))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "RMS_Y" + "=" + str(RMS(Sig_2))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "RMS_Z" + "=" + str(RMS(Sig_3))
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "Kurtosis_X" + "=" + str(Kurtosis(Sig_1))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Kurtosis_Y" + "=" + str(Kurtosis(Sig_2))
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "Kurtosis_Z" + "=" + str(Kurtosis(Sig_3))
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "low_frequency_X" + "=" + str(a1)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "low_frequency_Y" + "=" + str(a2)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "low_frequency_Z" + "=" +str( a3)
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "mid_low_frequency_X" + "=" +str( b1)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "mid_low_frequency_Y" + "=" + str(b2)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "mid_low_frequency_Z" + "=" +str( b3)
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "mid_frequency_X" + "=" + str(c1)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "mid_frequency_Y" + "=" +str( c2)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "mid_frequency_Z" + "=" +str( c3)
            write_api.write(bucket, org, data)
            # **************************************************************#
            data = "mem,host=" + "1" + " " + "high_frequency_X" + "=" + str(d1)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "high_frequency_Y" + "=" + str(d2)
            write_api.write(bucket, org, data)
            data = "mem,host=" + "1" + " " + "high_frequency_Z" + "=" + str(d3)
            write_api.write(bucket, org, data)
            # **************************************************************#

            """
            data = "mem,host=host1 ch1=" + str(RMS(Sig_1[0: 1023]))
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch2=" + str(RMS(Sig_2[0: 1023]))
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch3=" + str(RMS(Sig_3[0: 1023]))

            write_api.write(bucket, org, data)
            """
            #print("Data Write Count:", count, "data = ", a.split()[1] * k)
            Sig_1 = []
            Sig_2 = []
            Sig_3 = []
        time.sleep(0.05)



    """
    if(count >=start_sec*Samping_Rate and count <= final_sec*Samping_Rate and count %1024 ==0):
        with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            print(count)
            print(str(Mean(a.split()[count:count+1024])))
            data = "mem,host=host1 ch1="+str(Mean(a.split()[count:count+1024]))
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch2="+str(Mean(a.split()[count:count+1024]))
            write_api.write(bucket, org, data)
            data = "mem,host=host1 ch3="+str(Mean(a.split()[count:count+1024]))
            write_api.write(bucket, org, data)
            print("Data Write Count:",count,"data = ",a.split()[1]*k)
        time.sleep(0.05)
"""

