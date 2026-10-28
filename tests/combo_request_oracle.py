"""Independent empty-arena bite oracle: consumed input, never observed actions.

Only Space events occur in this witness. Stat1 starts at70 stamina, costs
12/14/18, and recovers2 at the end of an idle tick. No foes, movement or
other actions are allowed to supply hidden state to this oracle.
"""
from collections import defaultdict


DURATIONS = {1: 11, 2: 13, 3: 17}
COSTS = {1: 12, 2: 14, 3: 18}


def predicted_starts(events, enhanced, through, stamina=70):
    by_tick = defaultdict(list)
    last_tick = 0
    for tick, kind in events:
        assert last_tick <= tick <= through and tick >= 1, (tick, last_tick, through)
        assert kind in ('press', 'repeat', 'release'), kind
        by_tick[tick].append(kind)
        last_tick = tick
    assert 0 <= stamina <= 70
    result = []
    combo = pending = previous = 0
    started = 0
    grace = -1
    last_space = -100

    def start(hit, tick):
        nonlocal stamina, combo, started, pending, previous, grace
        if stamina < COSTS[hit]:
            return False
        stamina -= COSTS[hit]
        combo, started = hit, tick
        pending, previous, grace = 0, 0, -1
        result.append((tick, hit))
        return True

    for tick in range(1, through + 1):
        # Inputs precede action completion, including the inclusive end tick.
        for kind in by_tick[tick]:
            if kind == 'release' or enhanced and kind == 'repeat':
                continue
            fresh = enhanced or tick - last_space > 2
            last_space = tick
            if not fresh:
                continue
            if combo:
                if 1 <= tick - started <= DURATIONS[combo]:
                    pending = min(2, pending + 1)
            else:
                hit = previous % 3 + 1 if previous and tick <= grace else 1
                start(hit, tick)
        if combo and tick - started >= DURATIONS[combo]:
            finished, queued = combo, pending
            combo = pending = previous = 0
            grace = -1
            if queued:
                if start(finished % 3 + 1, tick):
                    pending = queued - 1
            else:
                previous, grace = finished, tick + 6
        if not combo:
            stamina = min(70, stamina + 2)
    return result
