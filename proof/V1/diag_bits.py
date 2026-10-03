#!/usr/bin/env python3
"""Detailed byte/bit-level analysis of corruption on the custom board TX path."""
import serial, time, random

BOARD = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
MON   = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
time.sleep(0.5)
rng = random.Random(99)
BLOCK = 512

def analyze(payload, got):
    n = min(len(payload), len(got))
    first_bad = None
    bad_bytes = 0
    for i in range(n):
        if payload[i] != got[i]:
            if first_bad is None: first_bad = i
            bad_bytes += 1
    return first_bad, bad_bytes, n

for trial in range(6):
    payload = rng.randbytes(BLOCK)
    BOARD.reset_input_buffer(); MON.reset_input_buffer()
    BOARD.write(payload)
    got = b''; mirror = b''
    t0 = time.time()
    while (len(got)<BLOCK or len(mirror)<BLOCK) and time.time()-t0<5:
        if len(got)<BLOCK:
            c=BOARD.read(BLOCK-len(got))
            if c: got+=c
        if len(mirror)<BLOCK:
            c=MON.read(BLOCK-len(mirror))
            if c: mirror+=c
    if got == payload:
        print(f"trial {trial}: CLEAN (512/512 ok)")
        continue
    fn, bad, tot = analyze(payload, got)
    fm, badm, totm = analyze(payload, mirror)
    print(f"trial {trial}: board echo BAD: first_bad_byte={fn} bad={bad}/{tot} "
          f"esp_mirror first_bad_byte={fm} bad={badm}/{totm}")
    # bit-level analysis at the first diverging byte (if same length)
    i = fn if fn is not None else 0
    if i < len(payload) and i < len(got):
        a, b = payload[i], got[i]
        diffbits = f"{a^b:08b}"
        print(f"     byte[{i}]: sent=0x{a:02x} got=0x{b:02x} xor={diffbits}")
    # check if after first divergence the stream shifted (compare payload[i+1:] vs got[i:])
    if fm is not None and fm < min(len(payload), len(mirror)):
        a, b = payload[fm], mirror[fm]
        print(f"     mirror byte[{fm}]: sent=0x{a:02x} got=0x{b:02x} xor={a^b:08b}")

BOARD.close(); MON.close()
