#include <Arduino.h>
#include "music.h"
#include "songs.h"

void setup() {
  playRandomMusic(musics, sizeof(musics)/sizeof(musics[0]));
}

void loop() {

}