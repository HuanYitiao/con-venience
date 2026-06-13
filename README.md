# con-venience

[![Build Firmware](https://github.com/HuanYitiao/con-venience-firmware/actions/workflows/build.yml/badge.svg)](https://github.com/HuanYitiao/con-venience-firmware/actions/workflows/build.yml)
![Platform](https://img.shields.io/badge/platform-ESP32--C6-blue)
![Framework](https://img.shields.io/badge/framework-Arduino%20%7C%20PlatformIO-orange)
![License](https://img.shields.io/badge/license-MIT-green)

> *Ubi amici, ibi opes.* — Plautus
> Where there are friends, there is wealth.

---

Ever hit it off with another fursuiter, only to realize — you can't unlock your phone through mesh eyes, can't type with paws on, and definitely don't want to break the magic by de-suiting just to swap contacts?

**con-venience** is a wearable social device for fursuiters. Watch-sized. One large button. 18-hour battery. Handles everything your phone can't while you're suited up.

---

## What it does

| Scenario | What happens |
|---|---|
| 🐾 Two fursuiters meet | Touch → Exchanges profiles automatically |
| 📱 Attendee wants to add you | They scan the QR code on your display → straight to your link |

No menus. No unlocking. No breaking character.

---

## ACOM — the signature interaction

**ACOM (Asymmetric Contact Over Metal)** is the heart of the project.

Two exposed metal contact pads on each device, aligned by opposite-polarity magnets. When two devices touch, they exchange contact information automatically — no Bluetooth pairing screen, no app, no "can you unlock my phone real quick."

**Under the hood — two layers:**

**Layer 1 — Physical contact (OOB channel):** The metal pads connect through a 74HC126 tri-state buffer, forming a single-wire half-duplex channel. The two devices exchange only their BLE MAC addresses over this channel. MAC comparison decides roles: the lower MAC becomes BLE Peripheral, the higher becomes Central.

**Layer 2 — BLE profile exchange:** With roles assigned and MACs known, the Central scans for the Peripheral directly (no broadcast needed), opens a GATT connection, and both devices exchange their full profiles — Telegram handle, avatar, and URLs. The contact appears as a name card on-screen. Connection closes. Done.

The physical touch is the pairing. The ritual is the protocol.

---

## Hardware

| Component | Choice | Notes |
|---|---|---|
| MCU | ESP32-C6-DevKitC-1 | BLE 5 + Wi-Fi 6 + native USB |
| Display (dev) | 2.42" SSD1309 OLED, 128×64 | SPI, u8g2 |
| Display (production target) | ST75256, 256×128, 4-bit grayscale | u8g2 throughout — constructor swap only |
| Storage | MicroSD via SPI | `/self_profile/`, `/friends_profiles/`, `/musics/` |
| Audio | VS1053B MP3 module | Game Boy–style feedback tones — post-MVP |
| Battery | 3× AA Eneloop NiMH | 18h+ target — covers a full convention day |
| Contact comm | Metal pads + 74HC126 | Physical layer of ACOM |
| LED | WS2812B | Status indicator |

**Form factor:** wrist-worn, watch profile. One large button for gloved-paw use. Directional buttons for unsuited configuration.

---

## Firmware architecture

```
firmware/platformIO/con-venience/
├── src/
│   └── main.cpp          # thin glue layer — get input → update FSM → render display
├── lib/
│   ├── fsm/              # finite state machine (Idle / Pairing / Contact card / Menu)
│   ├── storage/          # SD card + JSON contact storage, on-demand loading
│   ├── input/            # button handling (large button + directional)
│   ├── display/          # u8g2 UI — in progress
│   └── acom/             # ACOM protocol: OOB MAC exchange + BLE GATT profile transfer
└── platformio.ini
```

C-style throughout: structs, enums, plain functions with module-prefix naming. No classes. `main.cpp` connects things; it doesn't contain logic.

---

## Project status

```
[x] Hardware architecture finalized
[x] Storage module (lib/storage) — SD card, on-demand contact loading
[x] State machine (lib/fsm) — complete and tested
[x] Button input (lib/input) — complete
[x] CI (GitHub Actions) — Arduino + PlatformIO dual build
[x] BLE server — verified on ESP32-C6 via nRF Connect
[~] pioarduino + NimBLE-Arduino migration — validated, main project migration in progress
[~] ACOM protocol — state machine + physical layer designed, library integration in progress
[~] Display module (lib/display/) — u8g2 on pioarduino/NimBLE stack, UI implementation in progress
[ ] PCB v1 — target: small convention demo
[ ] Community hardware kit — target: post-PCB-v1
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

These are targets, not deadlines.

- **Now:** pioarduino migration, ACOM library integration, core UI
- **PCB v1 (target: 2025 Q4):** first physical board, small convention demo
- **Community kit (target: 2026 Q1):** hardware kit launch for builders
- **Future:** full fursuit companion platform

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

Firmware: MIT — do whatever you want, just keep the attribution.
Hardware: CERN-OHL-S

---

*Built for the furry community. Designed in Sweden.*
