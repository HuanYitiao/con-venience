# con-venience

[![Build Firmware](https://github.com/HuanYitiao/con-venience/actions/workflows/build.yml/badge.svg)](https://github.com/HuanYitiao/con-venience/actions/workflows/build.yml)
![Platform](https://img.shields.io/badge/platform-ESP32--S3-blue)
![Framework](https://img.shields.io/badge/framework-Arduino%20%7C%20PlatformIO-orange)
![License](https://img.shields.io/badge/license-MIT-green)

> *Ubi amici, ibi opes.* — Plautus
> Where there are friends, there is wealth.

---

Ever hit it off with another fursuiter, only to realize — you can't unlock your phone through mesh eyes, can't type with paws on, and definitely don't want to break the magic by de-suiting just to swap contacts?

**con-venience** has one answer: touch wrists.

---

## What it does

**con-venience** is a wearable social device built for furry conventions. Watch-sized. Lives on your forearm. Handles everything your phone can't while you're suited up.

| Scenario | What happens |
|---|---|
| 🐾 Two fursuiters meet | Wrists touch → ACOM protocol exchanges Telegram handles automatically |
| 📱 Attendee wants to add you | They scan the QR code on your display → straight to your profile |

---

## ACOM — the signature interaction

**ACOM (Asymmetric Contact Over Metal)** is the heart of the project.

Two exposed metal contact pads. Opposite-polarity magnets for alignment. When two devices touch, they handshake and exchange usernames — no Bluetooth pairing screen, no menus, no "can you unlock my phone real quick."

This is why the device exists.

**Under the hood:** single-wire half-duplex UART via 74HC126 tri-state buffer, 9600 baud, magic byte handshake + randomized backoff collision avoidance.

---

## Hardware

| Component | Choice | Why |
|---|---|---|
| MCU | ESP32-C6-devkit | BLE + native USB + enough GPIO |
| Display | 2.9" screen, 256×128px | Special style profiles |
| Audio | MP3 module | Game Boy–style feedback tones, light and simple |
| Battery | 3× AA Eneloop NiMH | 18h+ target — covers a full convention day |
| Contact comm | Metal pads + 74HC126 | The physical layer of ACOM |

**Form factor:** wrist-worn, watch profile. Designed around one hard constraint: gloved paws can't do precise button presses. One large pairing button. Everything else happens automatically.

---

## Firmware architecture

```
firmware/platformIO/con-venience/
├── src/
│   └── main.cpp          # thin glue layer, state machine entry point
├── lib/
│   ├── fsm/              # finite state machine (Idle / Pairing / Contact card / Menu)
│   ├── storage/          # LittleFS + JSON contact storage
│   ├── input/            # button handling
│   └── acom/             # contact communication protocol (in progress)
└── platformio.ini
```

Modular by design. Each subsystem is its own library under `lib/`. `main.cpp` connects things; it doesn't contain logic.

---

## Project status

```
[x] Hardware architecture finalized
[x] Storage module (lib/storage) — complete and tested
[x] State machine (lib/fsm) — complete and tested
[x] Button input (lib/input) — complete
[x] CI (GitHub Actions) — Arduino + PlatformIO dual build
[~] ACOM protocol — single-wire comms validated, library integration in progress
[~] Display module — u8g2 confirmed, UI implementation in progress
[ ] PCB v1 — target: October, small convention demo
[ ] Community hardware kit — target: February
```

`[~]` = validated, pending integration

---

## Getting started

**Requirements:**
- VS Code + PlatformIO extension
- That's it.

```bash
git clone https://github.com/HuanYitiao/con-venience
cd con-venience/firmware/platformIO/con-venience
# Open in VS Code — PlatformIO handles the toolchain automatically
```

No embedded experience required. PlatformIO sets everything up. If you can read Arduino or Python, you can read this codebase.

---

## Contributing

The furry community has a lot of programmers. This project is built for them.

**Good first contributions:**
- New display pages (extra QR codes, custom layouts)
- Documentation and translations
- Convention schedule / alert features

**Hardware contributions:**
- PCB design review
- Alternative form factors

Not sure where to start? Open an issue and say hi.

---

## Roadmap

- **Now:** Breadboard prototype, ACOM validation, core UI
- **October:** PCB v1, small convention demo
- **February:** Community hardware kit launch
- **Future:** Full fursuit companion platform

---

## Vision

con-venience is designed to grow into a full fursuit companion — covering the entire convention day, not just contact exchange. Panel schedule alerts so you never miss an event while suited. Body temperature and humidity monitoring to keep you safe. Integrations with convention apps, social platforms, and whatever the community decides to build next.

The hardware is a platform. What runs on it is up to everyone.

> *Semel in anno licet insanire.* — Seneca
> Once a year, it is permitted to go a little mad.

---

## Why open source?

Because the people who would use this are also the people who can improve it. Selling hardware kits funds development; keeping the firmware open means the community can extend it. A **con-venience** on your arm should feel like *your* device.

---

## License

MIT — do whatever you want, just keep the attribution.

---

*Built for the furry community. Designed in Sweden.*
