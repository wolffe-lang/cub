#!/usr/bin/env python3
"""Summarise --motion-census, retaining area/terrain/heading/gait/tier strata."""
import argparse
import collections
import math
from pathlib import Path


def summarise(path):
    strata = collections.defaultdict(list)
    rows = 0
    travel = []
    for line in Path(path).read_text().splitlines():
        if line.startswith("pace "):
            fields = dict(item.split("=", 1) for item in line.split()[1:])
            row = {key: int(value) for key, value in fields.items()}
            assert row["blocked"] == 0, line
            key = tuple(row[k] for k in ("area", "tier", "terrain", "heading", "gait"))
            strata[key].append(math.hypot(row["dx"], row["dy"]) * 30 / 256)
            rows += 1
        elif line.startswith("travel "):
            travel.append(line)
    assert rows > 0, "no pace rows"
    print("area,tier,terrain,heading,gait,samples,min_cps,max_cps,mean_cps")
    for key, speeds in sorted(strata.items()):
        print(",".join(map(str, key)), len(speeds),
              f"{min(speeds):.9f}", f"{max(speeds):.9f}",
              f"{sum(speeds) / len(speeds):.9f}", sep=",")
    print(f"rows={rows} strata={len(strata)}")
    for line in travel:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("census")
    summarise(parser.parse_args().census)
