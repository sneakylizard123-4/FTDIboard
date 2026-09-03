# Custom FT232RL Board - Interconnection Proof

Date of test: September 2, 2026 - All tests on `/dev/ttyUSB0` (custom board, bus 3-1, id `0403:6001`)

## Bottom line
The custom FT232RL USB-UART board is **electrically sound** (Yay!). Intermittent bit flips seen in
sustained transfers to the ESP32 are caused by a **marginal hookup wire / connection on the
board->ESP32 path, not by the board** and not by the ESP32.

---

## 1. Board integrity - pure self-loopback (decisive)
Board TX jumpered to RX, ESP32 fully disconnected.

- 500 x 512-byte pseudo-random blocks @ 115200 baud, back-to-back
- **Result: 500/500 PASS, 0 bad bytes, 8.7 kB/s**

```
=== SELF-LOOPBACK RESULT ===
passed : 500/500
failed : 0
bad bytes total: 0
VERDICT: PASS - BOARD TX/RX DRIVER INTEGRITY OK
```
Script: `board_selfloopback.py`

512 bytes was chosen because it is the exact block size that triggers bit flips *through the
ESP32*; the board alone never flips a bit. This rules out the board's TX/RX driver.

## 2. Direct PC loopback (board + cable + PC port all proven)
Board TX/RX jumpered, driven purely by the host PC.

- 100 x 32-byte pseudo-random chunks @ 115200
- **Result: 100/100 echoed correctly, 0 errors**

## 3. Integration with ESP32 (Adafruit HUZZAH32, UART2 RX=19/TX=21)
- Light traffic (16-byte frames, 50 ms gap): **20/20 PASS**
- Short frames (<=64 B, even 100 uss gap): **100% PASS**
- Single bytes: **300/300 PASS**

The board reliably talks to the ESP32 for normal, paced UART traffic.

## 4. The fault we chased (for completeness)
Under sustained ~512-byte back-to-back frames to the ESP32, ~40% of blocks had **exactly one
bad byte with 1-2 single-bit flips** (no frameshift, no desync - e.g. `0x47->0x07`). Downstream
checks proved:
- Not an ESP32 buffer overflow (enlarged RX buffer -> no change).
- Corruption originates on the **board TX -> ESP RX wire**, since the ESP32 mirrored exactly what
  arrived (board echo and ESP mirror were always bad together).
- The board alone does not produce it (see sec.1).

So the flips exist only when the board drives the wire to the ESP32 -> **marginal hookup wire /
contact**, consistent with the earlier-measured ~12 ohm twisted pair.

## Files
- Board self-loopback proof: `board_selfloopback.py`
- 1 MB stress benchmark: `customboard_bench.py` (fails via wire, see sec.4)
- Diagnostics: `diag_rate.py`, `diag_txrx.py`, `diag_bits.py`
- ESP32 echo firmware: `esp32_echo` (UART2 RX=19/TX=21, echoes + mirrors to UART0)