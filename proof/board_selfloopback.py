#!/usr/bin/env python3
"""
Pure custom FT232RL board self-loopback stress(test).

Jumper the board TX <-> RX (NO ESP32 in the path). Sends 512-byte blocks,
identical to the size that failed through the ESP32. If this passes clean,
the board itself is fine and the earlier fault was in the wires to the ESP.
If it fails, the board's TX/RX driver has a real signal-integrity problem.
"""
import serial, time, random, sys

PORT = '/dev/ttyUSB0'
BAUD = 115200
BLOCK = 512
ROUNDS = 500
rng = random.Random(2024)

print(f"PURE BOARD SELF-LOOPBACK @ {BAUD}  ({ROUNDS} x {BLOCK}B = {ROUNDS*BLOCK/1e6:.1f} MB)", flush=True)
print("Jumper must be between board TX and RX, ESP32 DISCONNECTED.\n", flush=True)

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(0.5)
ser.reset_input_buffer()

ok = 0; fail = 0; flips = 0
t0 = time.time()
for i in range(ROUNDS):
    payload = rng.randbytes(BLOCK)
    ser.reset_input_buffer()
    ser.write(payload)
    got = b''
    tt = time.time()
    while len(got) < BLOCK and time.time()-tt < 5:
        c = ser.read(BLOCK-len(got))
        if not c: break
        got += c
    if got == payload:
        ok += 1
    else:
        fail += 1
        nbad = sum(1 for a,b in zip(payload,got) if a!=b)
        flips += nbad
        if fail <= 10 or nbad > 3:
            print(f"  FAIL #{i}: {nbad} bad bytes in block", flush=True)
elapsed = time.time()-t0
rate = (ok+fail)*BLOCK/elapsed
print(f"\n=== SELF-LOOPBACK RESULT ===", flush=True)
print(f"passed : {ok}/{ROUNDS}", flush=True)
print(f"failed : {fail}", flush=True)
print(f"bad bytes total: {flips}", flush=True)
print(f"elapsed: {elapsed:.1f}s  throughput: {rate/1000:.1f} kB/s", flush=True)
verdict = "PASS - BOARD TX/RX DRIVER INTEGRITY OK" if ok==ROUNDS else "FAIL - BOARD HAS MARGINAL TX/RX DRIVER"
print(f"VERDICT: {verdict}", flush=True)
ser.close()
sys.exit(0 if ok==ROUNDS else 1)
