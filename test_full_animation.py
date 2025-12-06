#!/usr/bin/env python3
"""Full animation integration test - tests build_scenes and rendering sequence"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum, auto

print("=" * 70)
print("FULL ANIMATION INTEGRATION TEST")
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

print("\n[1/5] Building scenes...")
scenes = build_scenes()
print(f"      Built {len(scenes)} scenes")

# Calculate total frames
total_frames = max(s.end for s in scenes)
print(f"      Total frames: {total_frames}")
print(f"      Estimated runtime: {total_frames / 60:.1f} seconds ({total_frames / 60 / 60:.1f} minutes)")

print("\n[2/5] Creating render context...")
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

print("\n[3/5] Validating scene coverage (no frame gaps)...")
# Build a coverage map
coverage = [False] * total_frames
for scene in scenes:
    for f in range(scene.start, scene.end):
        if f < total_frames:
            coverage[f] = True

gaps = []
in_gap = False
gap_start = 0
for i, covered in enumerate(coverage):
    if not covered and not in_gap:
        in_gap = True
        gap_start = i
    elif covered and in_gap:
        gaps.append((gap_start, i - 1))
        in_gap = False
if in_gap:
    gaps.append((gap_start, total_frames - 1))

if gaps:
    print(f"      WARNING: Found {len(gaps)} gaps in scene coverage!")
    for start, end in gaps[:5]:
        print(f"        Gap: frames {start}-{end}")
else:
    print("      No gaps - all frames covered!")

print("\n[4/5] Test rendering sample frames across animation...")
# Test frames at key points
sample_points = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
test_frames = [int(p * total_frames) for p in sample_points]
test_frames = [min(f, total_frames - 1) for f in test_frames]

errors = []
for idx, frame in enumerate(test_frames):
    try:
        fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100))
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.set_aspect('equal')
        ax.axis('off')

        # Find and render active scenes for this frame
        np.random.seed(frame)
        for scene in scenes:
            if scene.start <= frame < scene.end:
                scene.render(ax, frame, ctx)

        # Update systems
        particles.update()
        particles.render(ax)
        camera.update()
        weather.update(frame)  # Pass frame number
        transitions.update()
        narration.update()
        slowmo.update()

        plt.close(fig)
        print(f"      Frame {frame:5d} ({sample_points[idx]*100:5.1f}%): OK")

    except Exception as e:
        errors.append((frame, str(e)))
        print(f"      Frame {frame:5d} ({sample_points[idx]*100:5.1f}%): FAILED - {e}")
        import traceback
        traceback.print_exc()

print("\n[5/5] Test rapid sequential rendering (stress test)...")
stress_errors = []
for i in range(0, min(total_frames, 600), 10):  # Test every 10th frame up to 600
    try:
        fig, ax = plt.subplots(figsize=(4, 2.25))  # Smaller for speed
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.axis('off')

        np.random.seed(i)
        for scene in scenes:
            if scene.start <= i < scene.end:
                scene.render(ax, i, ctx)

        particles.update()
        plt.close(fig)

    except Exception as e:
        stress_errors.append((i, str(e)))

if stress_errors:
    print(f"      {len(stress_errors)} errors in stress test:")
    for frame, err in stress_errors[:5]:
        print(f"        Frame {frame}: {err}")
else:
    print(f"      Stress test passed (tested {min(total_frames, 600)//10} frames)")

print("\n" + "=" * 70)
if errors or stress_errors or gaps:
    print("INTEGRATION TEST: SOME ISSUES FOUND")
    if gaps:
        print(f"  - {len(gaps)} scene coverage gaps")
    if errors:
        print(f"  - {len(errors)} sample frame errors")
    if stress_errors:
        print(f"  - {len(stress_errors)} stress test errors")
else:
    print("FULL ANIMATION INTEGRATION TEST: ALL PASSED!")
print("=" * 70)
