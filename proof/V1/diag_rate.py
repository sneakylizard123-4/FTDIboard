#!/usr/bin/env python3
"""
Diagnostic: is the custom-board stress failure a BOARD (signal integrity)
or FIRMWARE (ESP32 UART2 RX buffer overflow) problem?

Method: sweep sustained offered rate. If errors only appear above a rate
threshold and vanish with pacing, it's an upstream buffering/logic issue
(ESP32 firmware), not a board electrical failure.
"""
import serial, time, random

PORT = '/dev/ttyUSB0'
BAUD = 115200

rng = random.Random(7)

def paced_test(rate_label, block, count, gap):
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(0.5)
    ser.reset_input_buffer()
    ok = 0; fail = 0
    t0 = time.time()
    for i in range(count):
        payload = rng.randbytes(block)
        ser.reset_input_buffer()
        ser.write(payload)
        got = b''
        t1 = time.time()
        while len(got) < block and time.time()-t1 < 5:
            chunk = ser.read(block-len(got))
            if not chunk: break
            got += chunk
        if got == payload: ok += 1
        else: fail += 1
        if gap: time.sleep(gap)  # pace the sustained load
    rate = (ok+fail)*block/max(time.time()-t0,1e-6)
    ser.close()
    print(f"{rate_label:28s} block={block:5d} n={count:5d} gap={gap!s:5}  -> {ok:4d}/{ok+fail:4d} ok  ({rate/1000:.1f} kB/s)")
    return ok, fail

paced_test("blocked+50ms gap",     512, 100, 0.05)
paced_test("blocked+20ms gap",     512, 100, 0.02)
paced_test("blocked+5ms gap",      512, 100, 0.005)
paced_test("blocked no gap",       512, 100, 0.0)
paced_test("small+1ms gap",         64, 100, 0.001)
paced_test("small+100us gap",       64, 100, 0.0001)
paced_test("single byte bursts",     1, 300, 0.005)
