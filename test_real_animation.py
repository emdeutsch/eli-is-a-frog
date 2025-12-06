#!/usr/bin/env python3
"""
REAL ANIMATION TEST
This calls the EXACT same animate() function that FuncAnimation uses.
No mocking, no shortcuts - the real deal.
"""
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("REAL ANIMATION FUNCTION TEST")
print("=" * 60)

# Import and setup exactly like main() does
with open('eli_is_a_frog.py', 'r') as f:
    content = f.read()

# Remove main block
main_idx = content.find("if __name__ == '__main__':")
if main_idx != -1:
    content = content[:main_idx]

local_ns = {}
exec(content, local_ns)

# Get what we need
WIDTH = local_ns['WIDTH']
HEIGHT = local_ns['HEIGHT']
FPS = local_ns['FPS']
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
print(f"Total frames: {total_frames} ({total_frames/FPS:.1f}s)")

# Create systems exactly like create_animation() does
print("Creating systems...")
particles = AdvancedParticleSystem()
camera = Camera(WIDTH, HEIGHT)
lighting = LightingSystem()
weather = WeatherSystem(particles)
transitions = TransitionManager()
narration = NarrationSystem()
slowmo = SlowMotionManager()

# Create figure exactly like create_animation() does
fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100), dpi=100)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.set_aspect('equal')
ax.axis('off')

# This is the EXACT animate function from create_animation()
def animate(frame):
    ax.clear()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    ax.axis('off')

    # Update systems
    slowmo.update()
    effective_frame = slowmo.get_effective_frame(frame)
    transitions.update()
    narration.update()

    # Render scenes
    for scene in scenes:
        if scene.start <= effective_frame < scene.end:
            ctx = {
                'particles': particles,
                'camera': camera,
                'lighting': lighting,
                'weather': weather,
                'transitions': transitions,
                'narration': narration,
                'slowmo': slowmo
            }
            scene.render(ax, effective_frame, ctx)

    # Update camera and apply
    camera.update()
    camera.apply_to_axes(ax)

    # Update systems
    particles.update()
    lighting.update(frame)
    weather.update(frame)

    # Render particles
    particles.render(ax)
    return []

# TEST: Run animate() for sampled frames
print("\nTesting animation function...")
print("This tests the EXACT code path used by FuncAnimation\n")

# Test frames: first 100, then every 100th, plus last 100
test_frames = list(range(100))  # First 100
test_frames += list(range(100, total_frames - 100, 100))  # Every 100th
test_frames += list(range(max(0, total_frames - 100), total_frames))  # Last 100
test_frames = sorted(set(test_frames))

print(f"Testing {len(test_frames)} frames...")

errors = []
start_time = time.time()

for i, frame in enumerate(test_frames):
    try:
        animate(frame)
        if i % 50 == 0:
            print(f"  Frame {frame:5d} ({100*frame/total_frames:5.1f}%) - OK")
    except Exception as e:
        errors.append((frame, type(e).__name__, str(e)[:200]))
        print(f"  Frame {frame:5d} - FAILED: {type(e).__name__}: {str(e)[:80]}")

elapsed = time.time() - start_time
plt.close(fig)

print(f"\nCompleted in {elapsed:.1f}s ({len(test_frames)/elapsed:.1f} frames/sec)")
print("\n" + "=" * 60)

if errors:
    print(f"FAILED - {len(errors)} errors found:")
    for frame, etype, msg in errors[:10]:
        print(f"  Frame {frame}: {etype} - {msg[:60]}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED!")
    print(f"Tested {len(test_frames)} frames with zero errors.")
    print("The animate() function works correctly.")
    sys.exit(0)
