#!/usr/bin/env python3
"""
Custom FT232RL board <-> ESP32 (UART2 RX=19 / TX=21) reliability + throughput benchmark.

Funnels checksum-verified data through:  custom board TX -> ESP32 RX(19)
                                         custom board RX <- ESP32 TX(21)
Requires ZERO byte errors. Reports effective throughput and error rate.
"""
import serial, time, random, hashlib, sys

PORT = '/dev/ttyUSB0'
BAUD = 115200
BLOCK = 512            # bytes per write
ROUNDS = 2000          # blocks -> ~1 MB total
TIMEOUT = 5.0

random.seed(42)
rng = random.Random(42)

def main():
    print(f"Custom FT232RL <-> ESP32 echo benchmark @ {BAUD} baud", flush=True)
    print(f"Pin map: custom TX -> GPIO19, custom RX <- GPIO21", flush=True)
    print(f"Total payload: {BLOCK*ROUNDS/1e6:.1f} MB  ({ROUNDS} x {BLOCK}B blocks)\n", flush=True)

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(0.5)
    ser.reset_input_buffer()

    ok = 0
    mismatch = 0
    data_bytes = 0
    t_start = time.time()
    send_start = None
    for i in range(ROUNDS):
        payload = rng.randbytes(BLOCK)
        digest = hashlib.sha256(payload).hexdigest()[:12]
        ser.reset_input_buffer()
        ser.write(payload)
        if send_start is None:
            send_start = time.time()  # start timing once pipe is primed
        got = b''
        t0 = time.time()
        while len(got) < BLOCK and time.time() - t0 < TIMEOUT:
            chunk = ser.read(BLOCK - len(got))
            if not chunk:
                break
            got += chunk
        if len(got) != BLOCK:
            print(f"  TIMEOUT #{i}: got {len(got)}/{BLOCK} bytes", flush=True)
            mismatch += 1
            continue
        data_bytes += BLOCK
        if hashlib.sha256(got).hexdigest()[:12] == digest:
            ok += 1
        else:
            mismatch += 1
            print(f"  CHECKSUM MISMATCH #{i}", flush=True)
        if (i + 1) % 250 == 0:
            elapsed = time.time() - t_start
            rate = (BLOCK * (i + 1)) / max(elapsed, 1e-6)
            print(f"  {i+1}/{ROUNDS} blocks | {rate/1000:.0f} kB/s live", flush=True)

    elapsed = time.time() - t_start
    good_bytes = ok * BLOCK
    overall_rate = good_bytes / elapsed

    print("\n=== RESULTS ===", flush=True)
    print(f"Blocks verified correct : {ok}/{ROUNDS}", flush=True)
    print(f"Errors                  : {mismatch}", flush=True)
    print(f"Bytes verified          : {good_bytes/1e6:.2f} MB", flush=True)
    print(f"Elapsed                 : {elapsed:.2f} s", flush=True)
    print(f"Effective throughput    : {overall_rate/1000:.1f} kB/s", flush=True)
    print(f"Error rate              : {mismatch/ROUNDS:.6%}", flush=True)
    verdict = "PASS" if ok == ROUNDS else "FAIL"
    print(f"VERDICT                 : {verdict}", flush=True)
    ser.close()
    sys.exit(0 if verdict == "PASS" else 1)

if __name__ == "__main__":
    main()
