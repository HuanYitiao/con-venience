#include <Arduino.h>
#include "storage.h"

Contact self;
Contact loaded;
Contact contact;
Contact contacts[10];

void setup() {
  Serial.begin(115200);
  delay(1000);

  if (!storageInit()) {
    Serial.println("storage init failed");
    return;
  }
  Serial.println("storage init ok");

  strlcpy(self.username, "wolfram_test", USERNAME_LEN);
  strlcpy(self.url, "t.me/wolfram_test", URL_LEN);
  memset(self.avatar, 0xAA, AVATAR_LEN);

  if (storageSaveSelf(self)) Serial.println("save self ok");
  else Serial.println("save self failed");

  memset(&loaded, 0, sizeof(loaded));
  if (storageLoadSelf(loaded)) {
    Serial.print("username: ");
    Serial.println(loaded.username);
    Serial.print("url: ");
    Serial.println(loaded.url);
    Serial.print("avatar[0]: 0x");
    Serial.println(loaded.avatar[0], HEX);
  } else {
    Serial.println("load self failed");
  }

  strlcpy(contact.username, "friend_furry", USERNAME_LEN);
  strlcpy(contact.url, "instagram.com/friend_furry", URL_LEN);
  memset(contact.avatar, 0xBB, AVATAR_LEN);

  if (storageSaveContact(contact)) Serial.println("save contact ok");
  else Serial.println("save contact failed");

  int count = storageLoadContacts(contacts, 10);
  Serial.print("contact count: ");
  Serial.println(count);
  for (int i = 0; i < count; i++) {
    Serial.print("contact[");
    Serial.print(i);
    Serial.print("]: ");
    Serial.print(contacts[i].username);
    Serial.print(" | ");
    Serial.println(contacts[i].url);
  }
}

void loop() {}