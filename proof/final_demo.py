#!/usr/bin/env python3
"""
HACK CLUB FINAL DEMO - custom FT232RL board.

Phase A (board-only self-loopback, ESP disconnected):
  500 x 512B pseudo-random, back-to-back. MUST be 0 errors.

Phase B (board <-> ESP32 integration, ESP reconnected, paced):
  200 x 64B frames + 300 single bytes. MUST be 0 errors.
"""
import serial, time, random, sys

PORT = '/dev/ttyUSB0'
BAUD = 115200
rng = random.Random(2024)

def wait(msg):
    if sys.stdin.isatty():
        input(msg)
    else:
        time.sleep(2)

def phaseA():
    print("=== PHASE A: PURE BOARD SELF-LOOPBACK ===", flush=True)
    print("   (SPACE SPACE -> make sure board TX is jumpered to RX,", flush=True)
    print("    ESP32 DISCONNECTED, then press <Enter>)", flush=True)
    wait("")
    ser = serial.Serial(PORT, BAUD, timeout=1); time.sleep(0.4); ser.reset_input_buffer()
    BLOCK, ROUNDS = 512, 500
    ok = fail = flips = 0; t0 = time.time()
    for i in range(ROUNDS):
        p = rng.randbytes(BLOCK); ser.reset_input_buffer(); ser.write(p)
        got = b''; tt = time.time()
        while len(got) < BLOCK and time.time()-tt < 5:
            c = ser.read(BLOCK-len(got))
            if not c: break
            got += c
        if got == p: ok += 1
        else:
            fail += 1; flips += sum(1 for a,b in zip(p,got) if a!=b)
    ser.close()
    print(f"   {ok}/{ROUNDS} PASS, {fail} FAIL, {flips} bad bytes, {time.time()-t0:.1f}s", flush=True)
    if ok != ROUNDS:
        print("   PHASE A FAILED"); sys.exit(1)
    print("   PHASE A OK\n", flush=True)

def phaseB():
    print("=== PHASE B: BOARD <-> ESP32 INTEGRATION ===", flush=True)
    print("   (SPACE SPACE -> un-jumper board TX/RX and reconnect the two", flush=True)
    print("    wires TX->ESP GPIO19 and RX->ESP GPIO21, then press <Enter>)", flush=True)
    wait("")
    ser = serial.Serial(PORT, BAUD, timeout=1); time.sleep(0.4); ser.reset_input_buffer()
    t0 = time.time()
    # 64B frames, 5ms gap
    n_ok = 0
    for i in range(200):
        p = rng.randbytes(64); ser.write(p); ser.flush()
        got = ser.read(64)
        if got == p: n_ok += 1
        time.sleep(0.005)
    # 300 single bytes
    n_s = 0
    for i in range(300):
        b = rng.randbytes(1); ser.write(b); ser.flush()
        if ser.read(1) == b: n_s += 1
    ser.close()
    print(f"   64B frames: {n_ok}/200   single bytes: {n_s}/300   ({time.time()-t0:.1f}s)", flush=True)
    if n_ok==200 and n_s==300:
        print("   PHASE B OK\n")
    else:
        print("   PHASE B FAILED - if frame errors appear, it's the hookup wire (see PROOF.md)")
        sys.exit(1)

if __name__ == "__main__":
    print("CUSTOM FT232RL BOARD - HACK CLUB DEMO  (board_selfloopback + esp integration)\n")
    phaseA()
    phaseB()
    print("FINAL VERDICT: ALL GREEN - board proven functional, and integration is clean for paced traffic.")