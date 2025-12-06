#!/usr/bin/env python3
"""
EXTREME THOROUGHNESS TEST
Tests EVERY SINGLE FRAME in the animation
"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum, auto
import time

print("=" * 70)
print("TESTING EVERY SINGLE FRAME - NUCLEAR OPTION")
print("=" * 70)

# Read and exec file without running main()
with open('eli_is_a_frog.py', 'r') as f:
    content = f.read()

main_idx = content.find("if __name__ == '__main__':")
if main_idx != -1:
    content = content[:main_idx]

local_ns = {}
exec(content, local_ns)

# Pull needed items
WIDTH = local_ns['WIDTH']
HEIGHT = local_ns['HEIGHT']
build_scenes = local_ns['build_scenes']
AdvancedParticleSystem = local_ns['AdvancedParticleSystem']
Camera = local_ns['Camera']
LightingSystem = local_ns['LightingSystem']
WeatherSystem = local_ns['WeatherSystem']
TransitionManager = local_ns['TransitionManager']
NarrationSystem = local_ns['NarrationSystem']
SlowMotionManager = local_ns['SlowMotionManager']

print("\nBuilding scenes...")
scenes = build_scenes()
total_frames = max(s.end for s in scenes)
print(f"Total frames to test: {total_frames}")

# Create render context
particles = AdvancedParticleSystem()
camera = Camera(WIDTH, HEIGHT)
lighting = LightingSystem()
weather = WeatherSystem(particles)
transitions = TransitionManager()
narration = NarrationSystem()
slowmo = SlowMotionManager()

ctx = {
    'particles': particles,
    'camera': camera,
    'lighting': lighting,
    'weather': weather,
    'transitions': transitions,
    'narration': narration,
    'slowmo': slowmo
}

print(f"\nTesting all {total_frames} frames...")
print("Progress: ", end="", flush=True)

errors = []
start_time = time.time()

# Test EVERY FRAME
for frame in range(total_frames):
    try:
        # Progress indicator every 1000 frames
        if frame % 1000 == 0:
            print(f"{frame//1000}k ", end="", flush=True)

        fig, ax = plt.subplots(figsize=(4, 2.25))  # Smaller for speed
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.axis('off')

        np.random.seed(frame)  # Reproducible

        # Find and render active scenes
        for scene in scenes:
            if scene.start <= frame < scene.end:
                scene.render(ax, frame, ctx)

        # Update all systems as they would be in the real animation
        particles.update()
        camera.update()
        weather.update(frame)
        transitions.update()
        narration.update()
        slowmo.update()

        plt.close(fig)

    except Exception as e:
        errors.append((frame, str(e), type(e).__name__))
        plt.close('all')  # Clean up on error

elapsed = time.time() - start_time
print(f"\nDone! Tested {total_frames} frames in {elapsed:.1f}s ({total_frames/elapsed:.1f} fps)")

print("\n" + "=" * 70)
if errors:
    print(f"FOUND {len(errors)} ERRORS:")
    # Group errors by type
    error_types = {}
    for frame, msg, etype in errors:
        if etype not in error_types:
            error_types[etype] = []
        error_types[etype].append((frame, msg))

    for etype, error_list in error_types.items():
        print(f"\n{etype} ({len(error_list)} occurrences):")
        # Show first 5 of each type
        for frame, msg in error_list[:5]:
            print(f"  Frame {frame}: {msg[:80]}")
        if len(error_list) > 5:
            print(f"  ... and {len(error_list) - 5} more")
else:
    print("ALL FRAMES PASSED!")
print("=" * 70)

# Exit with error code if any failures
sys.exit(1 if errors else 0)
