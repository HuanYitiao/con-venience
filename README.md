# con-venience

[![Build Firmware](https://github.com/HuanYitiao/con-venience-firmware/actions/workflows/build.yml/badge.svg)](https://github.com/HuanYitiao/con-venience-firmware/actions/workflows/build.yml)
![Platform](https://img.shields.io/badge/platform-ESP32--C6-blue)
![Framework](https://img.shields.io/badge/framework-Arduino%20%7C%20PlatformIO-orange)
![License](https://img.shields.io/badge/license-MIT-green)

> *Ubi amici, ibi opes.* — Plautus

> Where there are friends, there is wealth.

---

Ever hit it off with another fursuiter, only to realize you can't unlock your phone through mesh eyes, can't type with paws on, and definitely don't want to break the magic by de-suiting just to swap contacts?

**con-venience** is a wearable social device for fursuiters. Watch-sized. One large button. 18-hour battery on cells you can buy at any store. It handles everything your phone can't while you're suited up.

---

## What it does

| Scenario | What happens |
|---|---|
| 🐾 Two fursuiters meet | Touch devices → profiles exchange automatically |
| 📱 An attendee wants to add you | They scan the QR on your display → straight to your link |

No menus. No unlocking. No breaking magic.

---

## ACOM — the signature interaction

**ACOM (Asymmetric Contact Over Metal)** is the heart of the project.

Two exposed metal pads on each device, aligned by opposite-polarity magnets so they can only meet the right way round. When two devices touch, they swap contact info on their own, no Bluetooth pairing screen, no app, no "can you unlock my phone real quick."

**Under the hood — two layers:**

**Layer 1 — Physical contact (out-of-band channel).**
The touching pads form a single-wire, half-duplex bus: open-drain lines sharing a pull-up resistor (wired-AND), running a lightweight UART at 4800 baud. Over this channel the two devices exchange only their BLE MAC addresses. A simple comparison then assigns roles, the lower MAC becomes the BLE **Peripheral**, the higher becomes the **Central**. That asymmetry is where the name comes from.

**Layer 2 — BLE profile exchange.**
With roles fixed and both MACs already known, the Central connects straight to the Peripheral — no advertising, no scanning the room. It opens a GATT connection and drives the whole exchange by **reading** the profile characteristics directly (a client-driven READ architecture, far more reliable than push/notify for bulk transfer). Full profiles move both ways: Telegram handle, avatar, URLs. The new contact appears as a name card on screen, the link closes, done.

The physical touch *is* the pairing. The ritual is the protocol.

---

## Hardware

| Component | Choice | Notes |
|---|---|---|
| MCU | ESP32-C6 | BLE 5 + Wi-Fi 6 + native USB. DevKitC-1 for dev; custom PCB in progress |
| Display | ST75256 256×128 grayscale LCD (JLX256128G-921/931) | SPI. Custom pixel driver; u8g2 used for font rasterization only.|
| Storage | MicroSD via SPI | Single source of truth — `/self_profile/`, `/friends_profiles/` |
| Audio | MAX98357A I2S DAC/amp | Feedback tones on contact and boot |
| RTC | PCF85063A | Timestamps contacts; time synced from the browser during setup |
| GPIO expander | MCP23008 (I2C) | Extra inputs/outputs off a two-wire bus |
| Battery | 3× AA alkaline (disposable) | 18h+ target — see below |
| Battery monitor | ADC voltage divider | Low-voltage threshold alert only |
| Contact comm | Metal pads + single-wire open-drain UART | Physical layer of ACOM |

**Why disposable AA?** A convention isn't a place to babysit a charger. Alkaline AAs are sold everywhere, need no charging, keep for years on a shelf, and pass through airport carry-on without a second look. The trade-off is a sagging discharge curve and Peukert losses under load, so power budget lives in backlight management and BLE timing, not in a fancy fuel gauge (those are LiPo-shaped and read nonsense off alkaline anyway). A plain voltage-divider "battery low" alert is all the metering it needs.

**Form factor:** wrist-worn, watch profile. One large button sized for a gloved paw. Directional buttons for out-of-suit configuration only.

---

## Software stack

Built on **PlatformIO** with the **pioarduino** platform (Arduino framework, FreeRTOS underneath).

- **BLE:** NimBLE-Arduino (GATT, client-driven READ)
- **Display:** custom ST75256 driver + u8g2 (fonts only)
- **Data:** ArduinoJson + the SD library, SD-as-sole-source-of-truth
- **QR:** ricmoo/QRCode

`main.cpp` is a thin glue layer — read input → advance the state machine → render. Cross-cutting logic stays out of the individual modules. Plain C style throughout: structs, enums, module-prefixed functions, `pins.h` as the one source of truth for every pin.

---

## Provisioning — no buttons required

Configuration happens out of suit, and still without fiddling:

1. Enter **Settings** → the device starts a SoftAP and shows a Wi-Fi QR full-screen.
2. Your phone scans it and joins; a second QR points to `http://192.168.4.1/`.
3. That page (a self-contained profile generator served from the SD card) lets you fill in your card and pick an avatar.
4. Submit → `profile.json` + `avatar.bin` are POSTed straight to `/self_profile/`, and the browser's local time is written to the RTC in the same request.

Everything is driven by network events — no button presses. Changes take effect on the next reboot.

---

## Repository layout

```
con-venience/                      # main repo — hardware, docs
└── firmware/                      # git submodule → con-venience-firmware
    ├── src/
    │   └── main.cpp               # thin glue: events → FSM → render
    ├── lib/
    │   ├── acom/                  # ACOM layer 1 — single-wire OOB MAC exchange
    │   ├── audio/                 # MAX98357A I2S tones
    │   ├── ble/                   # ACOM layer 2 — NimBLE GATT profile transfer
    │   ├── button/                # large button + directional
    │   ├── display/               # custom ST75256 driver + u8g2 fonts
    │   ├── fsm/                   # Idle / Pairing / Contact card / Menu
    │   ├── led/                   # status indicator
    │   ├── packing/               # profile serialize / deserialize
    │   ├── pins/                  # pins.h — single source of truth for the pin map
    │   ├── storage/               # SD card + JSON, on-demand loading
    │   └── wifi_config/           # SoftAP provisioning + web profile generator
    └── platformio.ini
```
---

## Project status

```
[x] Hardware stack — core architecture finalized
[x] Storage module — SD card, on-demand contact loading
[x] State machine (FSM) — complete
[x] Button input — complete
[x] Display driver (ST75256) — custom driver, complete
[x] ACOM — physical MAC exchange + BLE profile transfer
[x] BLE exchange — client-driven READ architecture
[x] Settings / Wi-Fi provisioning — SoftAP + QR + web profile generator
[x] End-to-end pairing — touch → exchange → save → contact card, working
[~] RTC (PCF85063A) — final firmware integration in progress
[ ] Power rails — LDO vs buck-boost decision with EE, before layout
[ ] Custom PCB — after power architecture sign-off
[ ] Community hardware kit — post-PCB
```

`[~]` = validated, integration pending. The firmware is feature-complete apart from the RTC; the open work is now mostly on the hardware side.

---

## Roadmap

Targets, not deadlines.

- **Now:** finish RTC integration; settle the regulator topology with the EE collaborator; prep the PCB brief.
- **Awoostria (late July 2026):** first public debut — a short clip of two devices trading cards, wrist to wrist.
- **PCB v1:** first physical board once the power architecture is signed off.
- **Community kit:** DIY kit + assembled units, aimed at builders (Tindie planned).
- **Future:** Whatever the community decides to grow it into.

---

## Contributing

The furry community has a lot of programmers. This project is built for them.

**Good first contributions**
- New display pages (extra QR codes, custom layouts)
- Documentation and translations
- Convention schedule / alert features

**Hardware contributions**
- PCB and power-rail review
- Alternative form factors

Not sure where to start? Open an issue and say hi.

---

## Vision

con-venience is meant to grow into a full fursuit companion — the whole convention day, not just contact exchange. Panel alerts so you never miss an event while suited. Temperature and humidity monitoring to keep you safe in-suit. Hooks into convention apps and whatever comes next.

The hardware is a platform. What runs on it is up to everyone.

> *Semel in anno licet insanire.* — Seneca

> Once a year, it is permitted to go a little mad.

---

## Why open source?

Because the people who'd wear this are the people who can improve it. Selling kits funds development; keeping the firmware open means the community can extend it. A **con-venience** on your arm should feel like *your* device.

---

## License

Firmware: **MIT** — do what you like, just keep the attribution.
Hardware: **CERN-OHL-S**

---

*Built for the furry community. Designed in Sweden.*