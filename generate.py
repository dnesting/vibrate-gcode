
import argparse
import math
import sys

# Empirically determined
_DEFAULT_STEPS_PER_SEC = 50 * 10 / 25.5


def linear_angles(n_steps):
    """Yields angles from 0 to 2*pi, evenly spaced along the X axis."""
    delta_cos = 2.0 / n_steps
    angles = []

    # Calculate half the steps
    half_steps = n_steps // 2

    for step in range(half_steps + 1):
        cos_val = 1 - step * delta_cos
        angle = math.acos(cos_val)
        angles.append(angle)

    # Mirror for even n_steps, excluding the last value of the first half
    # Include the last value for odd n_steps
    end = -1 if n_steps % 2 == 0 else -2
    for angle in reversed(angles[1:end]):
        angles.append(math.pi * 2 - angle)

    return angles


def vibrate_sine_period(n_steps, min_val=0.1, max_val=2.0):
    gcode = []
    for theta in linear_angles(n_steps): 
        amplitude = min_val + (max_val - min_val) * (1-abs(math.sin(theta)))
        if amplitude == 0:
            continue
        gcode.append(f"G1 Y{amplitude:.2f}")
        gcode.append(f"G1 Y{-amplitude:.2f}")
    return gcode


def main():
    parser = argparse.ArgumentParser(description='Generate gcode for vibrating')
    parser.add_argument('-t', '--steps', type=int, default=2, help='Vibration steps per period', metavar='N')
    parser.add_argument('-c', '--cycles', type=int, default=0, help='Number of periods (0 = use --secs)', metavar='N')
    parser.add_argument('-s', '--secs', type=float, default=0, help='Number of seconds (0 = use --cycles)', metavar='SECONDS')
    parser.add_argument('-x', '--max', type=float, default=2.0, help='Maximum amplitude', metavar='MM')
    parser.add_argument('-n', '--min', type=float, default=0.1, help='Minimum amplitude', metavar='MM')
    parser.add_argument('-o', '--output', type=str, default='', help='Output file', metavar='FILE')
    parser.add_argument('--steps_per_sec', type=float, default=_DEFAULT_STEPS_PER_SEC, help='Steps per second to compute --cycles from --secs', metavar='N')
    args = parser.parse_args()

    if args.cycles and args.secs:
        print('Cannot specify both --cycles and --secs')
        sys.exit(1)

    gcode = vibrate_sine_period(args.steps, min_val=args.min, max_val=args.max)

    cycles = args.cycles
    if args.secs:
        avg = (args.min + args.max) / 2
        cycles = int(args.secs * args.steps_per_sec / (args.steps * avg))

    out = sys.stdout
    if args.output:
        out = open(args.output, 'w')

    out.write('G21\n')
    out.write('G91\n')
    out.write(f"M117 {args.min:.2f}-{args.max:.2f}mm/{args.steps} {cycles}x\n")
    out.write('\n')
    for _ in range(cycles):
        for line in gcode:
            out.write(line + '\n')
        out.write('\n')
    out.write('M84\n')

    if args.output:
        out.close()


if __name__ == '__main__':
    main()
