# FTDIboard

FTDIboard is a compact, feature-rich USB-to-UART development interface designed for reliable serial communication, firmware flashing, and debugging of microcontroller-based systems.

It is built around the FT232RL USB-to-serial bridge and focuses on usability, robustness, and clear hardware feedback through extensive status LEDs and protection circuitry.

---

## 📌 Key Features

- FT232RL USB-to-UART bridge
- Switchable 3.3V / 5V logic levels
- ESP-style auto reset support (DTR-based)
- USB ESD protection (USBLC6)
- Resettable fuse (PPTC) for overcurrent protection
- Multiple status LEDs for power and UART activity
- Compact 75 × 50 mm PCB
- 4-layer PCB design for improved routing and stability
- M3 mounting holes in all four corners for enclosure or fixture mounting
- Standard 2.54mm headers for breadboard and prototyping compatibility
- USB-powered operation

---

## 🧠 Overview

FTDIboard is designed as a practical development tool for embedded systems work. It provides a stable and flexible USB-to-serial interface for:

- Microcontroller flashing (ESP32, AVR, STM32, etc.)
- Serial debugging and logging
- UART communication between devices
- Prototyping embedded systems

The board prioritizes reliability, protection, and usability over unnecessary complexity.

---

## ⚙️ Electrical Features

- USB-to-UART: FT232RL
- Logic voltage: switchable 3.3V / 5V
- Auto-reset: DTR-based ESP-style reset circuit
- Protection:
  - USBLC6 ESD protection diode
  - PPTC resettable fuse for current limiting
- Status indicators:
  - Power LED
  - TX/RX activity LEDs
  - Additional debug/status LEDs

---

## 📐 PCB Design

- Dimensions: 75 mm × 50 mm
- Layer stack: 4-layer PCB
- Mounting: 4 × M3 mounting holes (corner-mounted)
- Routing:
  - USB differential pair routed with matched length
  - Clean separation of power and signal layers
- Fabrication-ready design included in `/pcb`

---

## 📁 Repository Structure
/pcb → KiCad PCB design files (.kicad_sch, .kicad_pcb, .kicad_pro)
/cad → 3D models and STEP exports
/firmware → Optional test or utility firmware
BOM.csv → Bill of Materials
README.md → Project documentation

---

## 📦 Bill of Materials

See `BOM.csv` for full component list.

Main components include:
- FT232RL USB-to-UART IC
- USB connector (USB-C or Micro USB depending on revision)
- USBLC6 ESD protection device
- PPTC resettable fuse
- Voltage regulator / switching circuit for 3.3V and 5V rails
- LEDs for status indication
- Pin headers (2.54mm)
- M3 mounting hardware compatibility

---

## 🔌 Usage

1. Connect FTDIboard via USB
2. Install required drivers if needed:
   - FTDI VCP drivers
3. Select correct serial port in your development environment
4. Use with tools such as:
   - Arduino IDE Serial Monitor
   - PlatformIO
   - PuTTY / minicom / screen

---

## 🧪 Applications

- Microcontroller programming
- Serial debugging
- UART bridging between systems
- Embedded system prototyping
- Hardware bring-up and testing

---

## 🧊 Mechanical Design

- 75 × 50 mm PCB footprint
- 4 × M3 mounting holes in corner layout for secure installation
- Designed for mounting in enclosures, test rigs, or lab setups

---

## 🌙 Design Notes

The board includes a custom silkscreen design element (lunar motif) on the PCB as a visual signature, combining functional engineering with identifiable aesthetic design.

---

## 📸 Images

Add the following images for submission:

```md
![PCB Render](images/pcb.png)
![3D Render](images/render.png)
![Assembled Board](images/photo.jpg)