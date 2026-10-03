# v1.1 Build + Testing Proof

Build/test date: September 21, 2026. This is the v1.1 revision (no ULN2003s, second
fuse, 13 LEDs, full reroute from the September 1 redesign).

## Build

- PCBs assembled, powered up, nothing released the magic smoke.
- Fuse footprint bridged with tweezers (same as v1.0 - never bothered fitting
  the PPTC, just shorted it). On camera: `video/VID_20260921_184839.mp4`.
- All LEDs lit and stayed lit.

## Testing

- Re-ran the proof kit from v1.0 (self-loopback, paced ESP32 traffic,
  sustained-load stress).
- The two v1.0 issues are gone in this revision:
  - auto-reset stage no longer latches (was a bodge wire on v1.0)
  - VCCIO rail follows the switch properly, no bodge wire needed (was 3.3V
    even in 5V mode on v1.0)
- Test script running on camera: `video/VID_20260921_190001.mp4`.
- Full self-loopback passes clean.

## Media

| File | What it shows |
|------|---------------|
| `video/VID_20260921_184839.mp4` | bridging the fuse with tweezers, LEDs lighting up |
| `video/VID_20260921_190001.mp4` | test script running / self-loopback passing |
| `image/IMG_20260921_185508_130.jpg` | built v1.1 board |
| `image/IMG_20260921_185721_778.jpg` | built v1.1 board |

See `proof/V1/PROOF.md` for the original v1.0 electrical soundness proof.