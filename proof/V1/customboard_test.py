import serial, time, random

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(0.5)
ser.reset_input_buffer()
print("Custom board (ttyUSB0) -> ESP32 UART2 RX=19/TX=21 echo test", flush=True)

ok = 0
total = 0
for i in range(20):
    payload = bytes(random.randint(33,126) for _ in range(16))
    ser.reset_input_buffer()
    ser.write(payload)
    got = b''
    t0 = time.time()
    while len(got) < len(payload) and time.time()-t0 < 2.0:
        chunk = ser.read(len(payload)-len(got))
        if not chunk: break
        got += chunk
    total += 1
    if got == payload:
        ok += 1
    else:
        print(f"MISMATCH #{i}: sent {payload!r} got {got!r}", flush=True)
    time.sleep(0.05)

print(f"\nRESULT: {ok}/{total} echoed correctly via custom board", flush=True)
ser.close()
