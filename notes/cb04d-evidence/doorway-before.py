#!/usr/bin/env python3
"""Reconstruct 5f5b05a's centre-radius trigger on doorproof's first-contact rows.

No map/hash replication: all portal locations are whole cells, so translation
cancels in the original near() predicate. The nine graph edges have eighteen
faces; ten are path faces and eight shortcut faces were never walked triggers.
The two silhouettes and four quarters are silhouette.footprint at the baseline.
This is a geometric baseline census, not a recording of the old live loop.
"""
checks = misses = 0
for seed in range(50):
    for field in (80, 200):
        for face in range(18):
            for sy in range(-1, 2):
                for sx in range(-3, 4):
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = sx - dx, sy - dy
                            if -3 <= nx <= 3 and -1 <= ny <= 1:
                                continue
                            for w, h in ((8, 16), (12, 24)):
                                for facing in range(4):
                                    tw, th = (w, h) if facing % 2 == 0 else (h, w)
                                    cols, rows = (tw + 1) // 2, (th + 3) // 4
                                    x0, y0 = -((cols - 1) // 2), -((rows - 1) // 2)
                                    x1, y1 = x0 + cols - 1, y0 + rows - 1
                                    bx = x1 if dx > 0 else x0 if dx < 0 else 0
                                    by = y1 if dy > 0 else y0 if dy < 0 else 0
                                    x = (sx - bx) * 256 + 128
                                    y = (sy - by) * 256 + 128
                                    entered = face < 10 and x * x + y * y <= 256 * 256
                                    checks += 1
                                    misses += not entered
print(f'baseline 5f5b05a geometric first-contact rows {checks} misses {misses}')
assert checks == 806400 and misses == checks
