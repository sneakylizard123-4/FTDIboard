#!/usr/bin/env python3
"""
Isolate TX vs RX failure on the custom board.

We write a long block into ttyUSB0 (custom board). The ESP32:
  - echoes back on UART2 (custom board RX window, read at ttyUSB0)
  - mirrors what it RECEIVED to Serial/UART0 (read at ttyUSB1)

If ttyUSB0 is corrupt but ttyUSB1 mirror is clean  -> failure on ESP->board RX path
If ttyUSB1 mirror is corrupt (board sent bad data) -> failure on board->ESP TX path
"""
import serial, time, random

BOARD = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
MON   = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
time.sleep(0.5)
BOARD.reset_input_buffer()
MON.reset_input_buffer()

rng = random.Random(11)
BLOCK = 512
trials = 40
passed = 0
for i in range(trials):
    payload = rng.randbytes(BLOCK)
    BOARD.reset_input_buffer()
    MON.reset_input_buffer()
    BOARD.write(payload)

    # read board echo
    writing=True
    # collect monitor (ESP mirror) while board echo arrives
    got = b''; mirror = b''
    t0 = time.time()
    while (len(got) < BLOCK or len(mirror) < BLOCK) and time.time()-t0 < 5:
        if len(got) < BLOCK:
            c = BOARD.read(BLOCK-len(got))
            if c: got += c
        if len(mirror) < BLOCK:
            c = MON.read(BLOCK-len(mirror))
            if c: mirror += c

    board_ok = (got == payload)
    mirror_ok = (mirror == payload)
    if board_ok and mirror_ok: passed += 1
    print(f"#{i:3d} board_echo={'OK ' if board_ok else 'BAD'}  esp_mirror={'OK ' if mirror_ok else 'BAD'}"
          f"  (got {len(got):3d}B mirror {len(mirror):3d}B)")
    time.sleep(0.02)

print(f"\nTrials fully clean: {passed}/{trials}")
BOARD.close(); MON.close()
