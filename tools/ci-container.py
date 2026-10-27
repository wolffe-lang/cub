#!/usr/bin/env python3
"""Stage the pinned engine image for CI's exact-key cache; never publish it."""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent


def image_name(root):
    recipe = root / '.lair/ci/Containerfile'
    return 'localhost/pack-ci:' + hashlib.sha256(recipe.read_bytes()).hexdigest()[:16]


def inspect(engine, image):
    return subprocess.run([engine, 'image', 'inspect', image],
                          capture_output=True).returncode == 0


def prepare(root, engine):
    image = image_name(root)
    archive = root / 'target/ci-container/image.tar'
    if archive.is_file():
        source = 'cache'
        subprocess.run([engine, 'load', '--input', str(archive)], check=True)
    else:
        source = 'local'
        if not inspect(engine, image):
            source = 'build'
            recipe = root / '.lair/ci/Containerfile'
            subprocess.run([engine, 'build', '--memory', '12g', '-t', image,
                            '-f', str(recipe), str(recipe.parent)], check=True)
        if not inspect(engine, image):
            raise RuntimeError('prepared image lacks the exact Containerfile tag: ' + image)
        archive.parent.mkdir(parents=True, exist_ok=True)
        partial = archive.with_suffix('.partial')
        try:
            subprocess.run([engine, 'save', '--output', str(partial), image], check=True)
            partial.replace(archive)
        finally:
            partial.unlink(missing_ok=True)
    if not inspect(engine, image):
        raise RuntimeError('cached image lacks the exact Containerfile tag: ' + image)
    print(f'ci-container source={source} image={image} archive_bytes={archive.stat().st_size}', flush=True)


def run_tests(root, engine, command):
    if not command:
        raise RuntimeError('missing test command')
    if not inspect(engine, image_name(root)):
        raise RuntimeError('image must be provisioned before the test timer starts')
    env = dict(os.environ, LAIR_ENGINE=engine)
    subprocess.run([str(root / '.lair/tools/in-container'), *command],
                   cwd=root, env=env, check=True)


def timed(name, operation):
    start = time.monotonic()
    stamp = lambda: datetime.now(timezone.utc).isoformat()
    print(f'ci-stage {name} START utc={stamp()}', flush=True)
    status = 0
    try:
        operation()
    except BaseException as error:
        status = error.returncode if isinstance(error, subprocess.CalledProcessError) else 1
        raise
    finally:
        print(f'ci-stage {name} END utc={stamp()} elapsed_seconds={time.monotonic()-start:.3f} status={status}', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', default=os.environ.get('LAIR_ENGINE', 'docker'))
    parser.add_argument('action', choices=('prepare', 'run'))
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.action == 'prepare':
        timed('container-provision', lambda: prepare(ROOT, args.engine))
    else:
        command = args.command[1:] if args.command[:1] == ['--'] else args.command
        timed('linux-tests', lambda: run_tests(ROOT, args.engine, command))


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
