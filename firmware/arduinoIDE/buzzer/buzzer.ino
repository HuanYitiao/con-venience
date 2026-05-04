#define BUZZER_PIN 23

void setup() {
  // Star Wars Main Theme
  tone(BUZZER_PIN, 440, 500); delay(550);  // A
  tone(BUZZER_PIN, 440, 500); delay(550);  // A
  tone(BUZZER_PIN, 440, 500); delay(550);  // A
  tone(BUZZER_PIN, 349, 375); delay(425);  // F
  tone(BUZZER_PIN, 523, 125); delay(175);  // C
  tone(BUZZER_PIN, 440, 500); delay(550);  // A
  tone(BUZZER_PIN, 349, 375); delay(425);  // F
  tone(BUZZER_PIN, 523, 125); delay(175);  // C
  tone(BUZZER_PIN, 440, 1000); delay(1050); // A
}

void loop() {}