from pathlib import Path
import os
import subprocess

source = Path('/work/src/fight/fight.lu')
original = source.read_bytes()
needle = '        if sim.boss_index(s) < 0 && s.action != sim.FALL {\n'
insert = '''        if kind == sim.ELK && seed == 15 {
            let index = sim.boss_index(s)
            if index < 0 {
                eprint("elk15 field{cols} attempt{attempt} won tick{s.tick} health{s.health}")
                fs.create_dir_all("target/elk15-after-frames") else |_| { eprint("diagnostic mkdir failed") }
                for tier in [0, 1] {
                    var g = grid.new(s.rows, s.cols)
                    art.render(s, tier, mut g)
                    headless.write_frame("target/elk15-after-frames", "field{cols}-attempt{attempt}-won-tier{tier}", g) else |_| { eprint("diagnostic frame failed") }
                }
            }
            if index >= 0 {
                let f = copy s.foes[index]
                let (tx, ty) = approach_point(s, index)
                fs.create_dir_all("target/elk15-after-frames") else |_| { eprint("diagnostic mkdir failed") }
                for tier in [0, 1] {
                    var g = grid.new(s.rows, s.cols)
                    art.render(s, tier, mut g)
                    headless.write_frame("target/elk15-after-frames", "field{cols}-attempt{attempt}-tier{tier}", g) else |_| { eprint("diagnostic frame failed") }
                }
                eprint("elk15 field{cols} attempt{attempt} n{n} tick{s.tick} cub{s.x},{s.y} health{s.health} stamina{s.stamina} action{s.action} heading{s.heading} held{sim.held_direction(s)} blocked{s.blocked} boss{f.x},{f.y} hp{f.health} phase{f.phase} since{f.since} gap{sim.body_gap(s, index)} goal{tx},{ty} goal_blocked{sim.blocked(s, sim.floor_div(tx, sim.FP), sim.floor_div(ty, sim.FP))}")
            }
        }
'''
assert original.decode().count(needle) == 1
try:
    instrumented = original.decode().replace(needle, insert + needle)
    instrumented = instrumented.replace('use controls\n', 'use controls\nuse art\nuse grid\nuse headless\nuse std.fs\n', 1)
    start_marker = '            walker.press(mut s, mut r, keys)\n            count_hit(s, before, mut out)'
    start_probe = '''            walker.press(mut s, mut r, keys)
            if kind == sim.ELK && seed == 15 && cols == 80 && attempt == 1 && s.started == s.tick && (s.action == sim.BITE || s.action == sim.LUNGE || s.action == sim.DODGE) {
                let f = copy s.foes[i]
                let bearing = sim.heading_to(s.x, s.y, f.x, f.y)
                eprint("elk15 action tick{s.tick} kind{s.action} paw{s.paw} cub{s.x},{s.y} heading{s.heading} aim{s.attack_heading} bearing{bearing} gap{sim.body_gap(s, i)} health{s.health} boss_hp{f.health} phase{f.phase}")
                fs.create_dir_all("target/elk15-after-action-frames") else |_| { eprint("diagnostic mkdir failed") }
                for tier in [0, 1] {
                    var g = grid.new(s.rows, s.cols)
                    art.render(s, tier, mut g)
                    headless.write_frame("target/elk15-after-action-frames", "tick{s.tick}-tier{tier}", g) else |_| { eprint("diagnostic frame failed") }
                }
            }
            count_hit(s, before, mut out)'''
    assert instrumented.count(start_marker) == 1
    instrumented = instrumented.replace(start_marker, start_probe)
    source.write_text(instrumented)
    env = dict(os.environ, WOLF_STD='/work/.wolf-bin/std')
    subprocess.run(['/work/.wolf-bin/wolf', 'build', '--deny-warnings', 'src/cub.lu', '-o', 'target/cb04b-elk-fixed-diagnostic'], env=env, check=True)
finally:
    source.write_bytes(original)
with Path('/work/target/cb04b-elk-fixed-diagnostic-census.txt').open('w') as out, Path('/work/target/cb04b-elk-fixed-diagnostic.log').open('w') as err:
    result = subprocess.run(['/work/target/cb04b-elk-fixed-diagnostic', '--boss-census'], stdout=out, stderr=err)
print(Path('/work/target/cb04b-elk-fixed-diagnostic.log').read_text())
print('DIAGNOSTIC_CENSUS_EXIT', result.returncode)
assert source.read_bytes() == original
