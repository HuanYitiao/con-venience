# con-venience

[![Build Firmware](https://github.com/HuanYitiao/con-venience/actions/workflows/build.yml/badge.svg)](https://github.com/HuanYitiao/con-venience/actions/workflows/build.yml)

> *Ubi amici, ibi opes.* — Plautus
> Where there are friends, there is wealth.

> *Ever hit it off with another fursuiter, only to realize — you can't unlock your phone through mesh eyes, can't type with paws on, and definitely don't want to break the magic by de-suiting just to swap contacts?*
>
> **con-venience** solves that. Two wrists touch. Done.

<!-- TODO: insert demo video here -->
<!-- TODO: insert hero image / hand-drawn sketch here -->

---

## What it does

**con-venience** is an open-source wearable social device for fursuit conventions. It lives on your forearm like a watch and handles contact exchange so you never have to reach for your phone.

| Scenario | How it works |
|---|---|
| 🐾 Fursuiter meets fursuiter | Press devices together → Telegram handles exchange automatically via **ACOM** (physical contact protocol) |
| 📱 Attendee meets fursuiter | Scan QR code on display → opens Telegram/YouTube instantly |
| 🎉 Group meetup | BLE pairing window opens for bulk contact exchange |
| 😴 Standing by | E-ink display shows your QR code / handles with near-zero power draw |

### ACOM — the signature interaction

ACOM (Asymmetric Contact Over Metal) is a single-wire half-duplex UART protocol over two exposed metal contact pads, guided by side magnets with opposite polarity. When two devices touch, they handshake and exchange usernames — no pairing, no menus, no fumbling.

This is the interaction that makes **con-venience** worth wearing.

---

## Hardware

| Component | Choice | Why |
|---|---|---|
| MCU | ESP32-S3-Zero (TBD)| BLE + native USB + enough GPIO |
| Display | 2.9" Waveshare e-ink, 296×128px | Sunlight readable, ~0mW standby |
| Audio | Passive piezo buzzer (PWM) | Game Boy–style feedback tones |
| Power | CR2450 coin cell (TBD)| 18h+ convention day on a single cell |

**Form factor:** wrist-worn, forearm mount, watch-like profile. Designed around the constraint that gloved paws can't do precise button presses — a single short press cycles display pages; a long press triggers pairing mode.

---

## Project status

```
[x] Hardware architecture finalized
[x] Component selection complete
[x] Buzzer / melody playback — integrated
[~] e-ink display — tested standalone, not yet merged into main firmware
[~] BLE — tested standalone, not yet merged into main firmware
[~] Button input — tested standalone, not yet merged into main firmware
[ ] ACOM — waiting on hardware materials
[ ] u8g2 UI implementation (QR page, contacts list, pairing animation)
[ ] PCB v1 — target: small convention demo, October
[ ] Community hardware kit release — target: February
```

`[~]` = tested, pending integration

---

## Getting started
---

## Architecture

```
con-venience/
├── firmware/
│   └── platformIO/con-venience/   # Main firmware (Arduino framework via PlatformIO)
│       ├── src/
│       │   ├── main.cpp           # Entry point, page state machine
│       └── platformio.ini
├── hardware/                      # Schematics, PCB files (KiCad)
├── tools/                         # Helper scripts for contributors
│   └── image-convert/             # Convert images to e-ink compatible format
├── ui/                            # UI layout references (Figma exports, mockups)
└── docs/                          # Documentation
```

If you've never touched embedded before, the PlatformIO project opens straight in VS Code — no manual toolchain setup.

---

## Contributing

The furry community has a lot of programmers. This project is designed for them.

**Good first contributions:**
- New display pages (additional QR codes, custom layouts)
- BLE companion app features
- Documentation and translations

**Hardware contributions:**
- PCB design review
- Alternative form factors

If you want to contribute but aren't sure where to start, open an issue and say hi.

---

## Roadmap

- **Now:** Breadboard prototype, ACOM validation, core UI
- **October:** PCB v1, small convention demo
- **February:** Community hardware kit launch
- **Future:** Fursuit companion

---

## Vision
**con-venience** is designed to grow into a full fursuit companion — a wearable assistant for the entire convention day, not just contact exchange. With community involvement, future versions could include panel schedule alerts so you never miss an event while suited, body temperature and humidity monitoring to help you stay safe inside a fursuit, and integrations with convention apps, social platforms, and whatever the community decides to build next.

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