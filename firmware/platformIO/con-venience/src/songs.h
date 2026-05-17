#pragma once
#include "music.h"

Note bootMusic[] = {
    {NOTE_D5, 4},
    {NOTE_D5, 4},
    {NOTE_D5, 4},
    {NOTE_D5, 4},
    {NOTE_D5, 4},
    {NOTE_E5, 4},
    {NOTE_D5, 2},
    {NOTE_D5, 4},
    {NOTE_G5, 4},
    {NOTE_FS5, 4},
    {NOTE_E5, 4},
    {NOTE_D5, 4},
    {NOTE_E5, 4},
    {NOTE_D5, 2}
};

Music boot = {240, bootMusic, sizeof(bootMusic)/sizeof(bootMusic[0])};