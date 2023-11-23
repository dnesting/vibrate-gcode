# vibrate-gcode

This repo contains code and sample G-code for using a 3D print bed as a vibration table.

## Provided G-code files

```
vibrate-20-10s-0.1-2.0mm.gcode
vibrate-20-60s-0.1-2.0mm.gcode
vibrate-20-300s-0.1-2.0mm.gcode
vibrate-20-900s-0.1-2.0mm.gcode
```

These vibrate the 3D printer table.
The times (10s, 60s, 300s, 900s) are calibrated for my Prusa MK3s+.

## Generating your own files

```
make vibrate-{steps}-{seconds}s-{min_amplitude}-{max_amplitude}mm.gcode
make vibrate-30-10s-0.1-2.0mm.gcode
```

The files generated by `generate.py` produce Y-axis movements with amplitudes between `min_amplitude` and `max_amplitude`.

- `steps`: the number of movement steps per period
- `seconds`: used to compute the number of periods to generate in the G-code
- `min_amplitude`: the shortest movements in the period
- `max_amplitude`: the longest movements in the period

If you don't want the amplitude to vary (you just want a constant vibration at the same amplitude),
`min_amplitude` and `max_amplitude` can just be set to the same value and `steps` can be any non-zero number (eg. 1).

## `generate.py`

```
usage: generate.py [-h] [-t N] [-c N] [-s SECONDS] [-x MM] [-n MM] [-o FILE]
                   [--steps_per_sec N]

Generate gcode for vibrating

options:
  -h, --help            show this help message and exit
  -t N, --steps N       Vibration steps per period
  -c N, --cycles N      Number of periods (0 = use --secs)
  -s SECONDS, --secs SECONDS
                        Number of seconds (0 = use --cycles)
  -x MM, --max MM       Maximum amplitude
  -n MM, --min MM       Minimum amplitude
  -o FILE, --output FILE
                        Output file
  --steps_per_sec N     Steps per second to compute --cycles from --secs
```

Note that the default `--steps_per_sec` value was empirically determined and may be wildly off for your printer.

## Future directions

The vibrations just involve short G-code movements, essentially as fast as the printer is capable of moving.
Eg.:

```
G1 Y2.00
G1 Y-2.00
G1 Y1.17
G1 Y-1.17
G1 Y0.86
G1 Y-0.86
```

There are opportunities here for:

- More intelligently setting the acceleration to give consistent results across any type of printer
- Allowing `generate.py` to think natively in terms of hertz. It would be nice, for instance to be able to generate G-code for a 100Hz vibration with a 1mm max amplitude, and have it automatically figure out the best amplitude and acceleration value to get to 100Hz.
- True sine wave motion rather than just linear movements back and forth.

I don't intend to hack on this much further, but if anyone wants to contribute changes, feel free.
