#include <Arduino.h>

#define BTN1 32
#define BTN2 33
#define BUZZER 18

#define LONG_PRESS_MS 300

bool btn1Last = HIGH;
bool btn2Last = HIGH;
unsigned long btn1PressTime = 0;
unsigned long btn2PressTime = 0;

void beep(int freq, int duration) {
  tone(BUZZER, freq, duration);
  delay(duration + 20);
}

void setup() {
  Serial.begin(115200);
  
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);

  Serial.println("Ready.");
  beep(1000, 100);
  beep(1500, 100);
}

void loop() {
  bool btn1Now = digitalRead(BTN1);
  bool btn2Now = digitalRead(BTN2);
  unsigned long now = millis();

  // BTN1
  if (btn1Now == LOW && btn1Last == HIGH) {
    btn1PressTime = now; // 按下，记时
  }
  if (btn1Now == HIGH && btn1Last == LOW) {
    unsigned long held = now - btn1PressTime;
    if (held >= LONG_PRESS_MS) {
      Serial.println("BTN1 long press");
      beep(600, 300);
    } else {
      Serial.println("BTN1 short press");
      beep(800, 100);
    }
  }

  // BTN2
  if (btn2Now == LOW && btn2Last == HIGH) {
    btn2PressTime = now;
  }
  if (btn2Now == HIGH && btn2Last == LOW) {
    unsigned long held = now - btn2PressTime;
    if (held >= LONG_PRESS_MS) {
      Serial.println("BTN2 long press");
      beep(900, 300);
    } else {
      Serial.println("BTN2 short press");
      beep(1200, 100);
    }
  }

  btn1Last = btn1Now;
  btn2Last = btn2Now;

  delay(20);
}