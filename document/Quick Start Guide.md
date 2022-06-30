# Quick Start Guide

## 首先將這份.zip檔案送去PCB廠家製作[檔案連結](https://github.com/harry123180/AUOProject/blob/cd63b463207a05c479944efaf1438e0ff1443a89/MCU-Sensor-dev-v16_2022-06-02)
* ### 此專案開發是送[ICBOX艾斯霸](https://icbox.com.tw/)公司進行洗板
>檔案名稱: MCU-Sensor-dev-v16_2022-06-02  
>製程:     FR-4 黑底白字 1.6MM板厚 有鉛噴錫 1OZ銅箔  
>數量:    10pcs  
>報價:    NT$800 含稅
* ### MCU 開發IDE [Arduino IDE 1.8.16](https://www.arduino.cc/en/software)

* ### MCU 型號 :ESP32-WROOM-32 [購買連結](https://shopee.tw/ESP32S%E5%96%AE%E7%89%87%E6%A9%9F30pin%EF%BC%8EDEVKIT-V1%E9%96%8B%E7%99%BC%E6%9D%BFWiFi%E8%97%8D%E7%89%99ioT%E7%89%A9%E8%81%AF%E7%B6%B2%E9%9B%99%E6%A0%B8%E5%BF%83-i.73692085.4859808779)

* ### 使用Arudino IDE開啟[這個資料夾](https://github.com/harry123180/AUOProject/blob/cd63b463207a05c479944efaf1438e0ff1443a89/upstream/ESP_Program/3Axis_FFT_FXLN8371Q_Serial_MakeSure)將程式燒入

* ### 參照這篇在主機上安裝[InfluxDB](https://docs.influxdata.com/influxdb/v2.2/install/?t=Windows)
* ### 使用Python腳本來連結MCU傳入的data至InfluxDB 範例語法如下
``` 
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

```
* ### 參照這篇在主機上安裝[Grafana](document/Install Grafana windows.md)
### Flux語法在Grafana上
* Example  

```
  from(bucket: "testDB")
  |> range(start: -5h, stop: -1s)
  |> filter(fn: (r) => r["_measurement"] == "mem" and r["_field"] == "ch2")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield()  
  ``` 