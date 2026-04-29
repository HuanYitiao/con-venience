# con-venience

> An open-source wearable social device for fursuit interaction — inspired by Digimon virtual pets.

**con-venience** (convention + convenience) is a wearable device designed for fursuit wearers who can't easily use a phone at furry conventions. It lets you exchange social contacts through NFC, a custom near-field wired protocol (ACOM), and BLE — no human hands required.

---

## The Problem

At furry conventions, fursuiters can't easily use their phones with paws. Exchanging social links requires taking off paws, fumbling with a screen, or asking someone else to type for you. **con-venience** solves this with a wearable device that handles contact exchange automatically — tap, connect, or bump.

---

## How It Works

| Scenario | Method |
|---|---|
| Regular attendee wants to follow you | NFC tap with phone → opens Telegram directly |
| Two fursuiters want to exchange contacts | ACOM — magnetic contact pads snap together, data exchanges automatically |
| Group of fursuiters want to add each other | Long-press button → BLE 5-minute discovery window |

---

## Features (v1)

- **E-ink display** — shows QR codes for multiple social platforms, short-press button to cycle pages
- **NFC** — phone tap opens your Telegram link instantly (PN532, Tag mode)
- **ACOM** — custom single-wire half-duplex protocol over magnetic contact pads; two identical devices snap together and exchange data automatically
- **BLE** — long-press triggers a 5-minute discovery window; find nearby con-venience devices, confirm to add, window refreshes on each new contact
- **Local storage** — NVS stores config, LittleFS stores page content; survives power loss
- **BLE phone config** — update your Telegram handle and social links wirelessly via Web Bluetooth
- **BLE sync** — push today's encounter log to your phone after the convention
- **E-ink backlight** — white LEDs for dark venues, toggle with long-press
- **Passive buzzer** — audio feedback on ACOM connect, NFC tap, and BLE add

---

## Hardware

| Component | Part | Notes |
|---|---|---|
| MCU | ESP32-S3-Zero | Dual-core 240MHz, BLE 5.0, 24 GPIO, USB-C |
| E-ink display | 2.9" 296×128px B/W SPI | Waveshare; always-on, sunlight readable |
| NFC | PN532 module | Tag mode (v1); Reader/Card Emulation planned (v2) |
| ACOM interface | 2× PCB edge contact pads + side magnets | Signal on top, GND on bottom; magnets align polarity |
| Power | 3× AA NiMH (e.g. Eneloop) | 4.5V → 3.3V via AMS1117; ~2500mAh, no shipping restrictions |
| Button | 12mm+ tactile switch | Short press: page flip; Long press: BLE window / backlight |
| Buzzer | Passive piezo 12×5.5mm | PWM-driven, different tones for each event |
| Backlight | 4× white 3mm LED | E-ink illumination for dark venues |
| USB-C | Standard connector | Firmware update, dev power |

**PCB:** Digimon-inspired rounded enclosure, AA battery compartment on back, ACOM contacts on bottom edge.

---

## ACOM Protocol

ACOM (short for a-com, the device's physical contact interface) is a custom single-wire half-duplex UART protocol.

- Two contact pads: **Signal** (top) and **GND** (bottom)
- Side magnets with opposing polarity auto-align two identical devices
- When devices connect face-to-face, Signal connects to Signal and GND to GND — correct for shared single-wire bus
- Collision arbitration uses **randomised exponential backoff** (0–255ms, doubling on retry)
- Payload: device ID, Telegram handle, social links — all stored in NVS

---

## Device ID

Each device generates a random **4-character uppercase ID** (e.g. `MIST`) on first boot. Collision probability is low for convention-scale use. A community registry is planned for global uniqueness.

---

## Firmware

Built with **PlatformIO + VS Code**, Arduino framework.

Two tracks are planned:

| Track | Framework | Audience |
|---|---|---|
| `firmware/arduino` | Arduino (PlatformIO) | Community contributors |
| `firmware/espidf` | ESP-IDF | Production / power optimisation |

Storage: NVS for user config, LittleFS for page content and QR images.

---

## Roadmap

**v1 — Breadboard prototype (target: July 2025)**
- [ ] E-ink display with multi-page QR layout
- [ ] NFC Tag mode (phone tap → Telegram)
- [ ] ACOM wired contact exchange
- [ ] BLE discovery window with confirmation
- [ ] BLE phone config and encounter sync
- [ ] Local NVS/LittleFS storage

**v1 PCB (target: October 2025)**
- [ ] Digimon-inspired enclosure
- [ ] ACOM magnetic contact pads
- [ ] E-ink backlight LEDs
- [ ] AA battery compartment

**v2 (community-driven)**
- [ ] PN532 Card Emulation for device-to-device NFC
- [ ] Community plugin page system
- [ ] Global device ID registry (possible Barq collaboration)

---

## Getting Started

*Coming soon — hardware arrives May 2025.*

---

## Contributing

This project is designed for community extension. Once the first hardware batch ships, contribution guides will cover:

- Writing new display page modules
- Adding sensor support via the I2C/SPI expansion headers
- Porting to other ESP32 variants

---

## Inspiration

- **Digimon / Tamagotchi** — physical contact interaction between devices
- **EF28 Badge** (Eurofurence) — open-source ESP32 convention badge
- **Badger 2040** (Pimoroni) — e-ink convention badge

---

## License

- Firmware: [MIT License](LICENSE)
- Hardware design files: [CERN-OHL-S-2.0](LICENSE-HARDWARE)

© 2025 HuanYitiao
