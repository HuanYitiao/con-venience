#include <Arduino.h>
#include "music.h"
#include "songs.h"
#include "button.h"

#define BTN1 32
#define BTN2 33

btn_state_t BTN1State;
btn_state_t BTN2State;

void setup() {
  Serial.begin(115200);

  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);

  Serial.println("Ready.");
}

void loop() {
  btn_event_t BTN1Event = btn_read(BTN1, &BTN1State);
  switch (BTN1Event)
  {
    case BTN_CLICK:
      Serial.println("BTN1 click");
      break;

    case BTN_LONG_PRESS:
    Serial.println("BTN1 long press");
    break;
  
    default:
      break;
  }

  btn_event_t BTN2Event = btn_read(BTN2, &BTN2State);
  switch (BTN2Event)
  {
    case BTN_CLICK:
      Serial.println("BTN2 click");
      break;

    case BTN_LONG_PRESS:
    Serial.println("BTN2 long press");
    break;
  
    default:
      break;
  }

}