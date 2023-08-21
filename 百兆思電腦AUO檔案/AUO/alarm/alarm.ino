int pinA = 2;//外部按鈕
int pinB = 12;//控制Relay
bool alram = false;

String receivedData = "";  // 儲存接收到的數字字串

void setup() {
  Serial.begin(9600);  // 設定串列通訊速率為 9600 bps
  pinMode(pinA, INPUT_PULLUP);  // 將13號腳設定為輸入模式並使用內部上拉電阻
  pinMode(pinB,OUTPUT);
  digitalWrite(pinB,LOW);//開啟警示
}

void loop() {
  int buttonState = digitalRead(pinA);  // 讀取13號腳的狀態
   Serial.println(buttonState);
  if (buttonState == LOW or alram ) {
    digitalWrite(pinB,HIGH);//開啟警示
    Serial.println("ON");
    
  }
  if (buttonState == HIGH  and !alram) {
    digitalWrite(pinB,LOW);//關閉警示
    Serial.println("off");
  }
  if (Serial.available() > 0) {  // 檢查是否有資料可供讀取
    char incomingByte = Serial.read();  // 讀取一個字節的資料
    
    if (incomingByte == '\n') {  // 如果收到換行符號
      int number = receivedData.toInt();  // 將接收到的數字字串轉換為整數
      
      if (number > 15) {
        alram=true;
      } else {
        alram=false;
      }
      
      receivedData = "";  // 清空接收緩衝區
    } else if (incomingByte >= '0' && incomingByte <= '9') {
      receivedData += incomingByte;  // 將數字字符添加到接收緩衝區
    }
  }
}
