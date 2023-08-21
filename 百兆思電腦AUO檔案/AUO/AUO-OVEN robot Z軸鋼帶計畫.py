import Database as DB
import time 
tokens = "eQ5UWiaZGFzzHpNgLpMPuaqTR0UM3lPxjGYc3ykeT-t0vIIv_7c4ye_QzwUC3CWhCadcARmm8-c_SzAgbcGzwA=="
url = "http://localhost:8086"
org = "AUO"
bucket = "OVEN"
a = DB.Database(tokens, url, org, bucket)
while(True):
    a.pushAnomalyRate()
    time.sleep(60)