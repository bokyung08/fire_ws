#include <SoftwareSerial.h>

int a = 10;
int b = 7;

// SoftwareSerial (블루투스)
// RX, TX
SoftwareSerial btSerial(2, 3);

void setup() {
  pinMode(a, OUTPUT);
  pinMode(b, OUTPUT);

  // 기본 OFF 상태
  digitalWrite(a, LOW);
  digitalWrite(b, LOW);

  Serial.begin(9600);     // 라즈베리파이 / PC
  btSerial.begin(9600);  // 블루투스

  Serial.println("System Ready");
  btSerial.println("Bluetooth Ready");
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == '1') {
      // 🔥 블루투스로 화재 감지 알림 전송
      btSerial.println("화재 감지됨");

      // 🔥 펌프 ON (정방향)
      digitalWrite(a, HIGH);
      digitalWrite(b, LOW);

      Serial.println("Pump ON");

      delay(5000);   // 5초 동안 작동

      // 🔥 펌프 OFF
      digitalWrite(a, LOW);
      digitalWrite(b, LOW);

      Serial.println("Pump OFF");
      btSerial.println("소화 완료");
    }
  }
}
