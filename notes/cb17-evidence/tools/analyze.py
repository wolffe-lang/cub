#!/usr/bin/env python3
"""cb17 scratch: PCM measurements for a part render (stereo S16_LE, 48 kHz).

    analyze.py A.pcm [B.pcm ...]

Prints seconds, peak, RMS dBFS overall, the loudest second's RMS, the last
tick's peak (score-check's seam bar is 256) and the first tick's peak.
"""
import math
import struct
import sys

TICK = 1600 * 4


def samples(b):
    n = len(b) // 2
    return struct.unpack("<%dh" % n, b)


def peak(b):
    s = samples(b)
    return max(max(s), -min(s)) if s else 0


def rms(b):
    s = samples(b)
    if not s:
        return 0.0
    return math.sqrt(sum(x * x for x in s) / len(s))


def db(x):
    return 20 * math.log10(x / 32768) if x > 0 else -999.0


def main():
    for path in sys.argv[1:]:
        b = open(path, "rb").read()
        secs = len(b) / 192000
        per = [rms(b[i:i + 192000]) for i in range(0, len(b), 192000)]
        loud = max(per) if per else 0
        quiet = min(per) if per else 0
        print("%-28s %5.1fs peak %5d rms %6.1f dBFS loudest-s %6.1f quietest-s %6.1f last-tick %4d first-tick %4d" % (
            path.split("/")[-1], secs, peak(b), db(rms(b)), db(loud), db(quiet), peak(b[-TICK:]), peak(b[:TICK])))


if __name__ == "__main__":
    main()
