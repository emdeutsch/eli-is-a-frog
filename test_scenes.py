#!/usr/bin/env python3
"""Comprehensive scene rendering test for eli_is_a_frog.py"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum, auto

print("=" * 60)
print("COMPREHENSIVE SCENE RENDERING TEST")
print("=" * 60)

# Read and exec file without running main()
with open('eli_is_a_frog.py', 'r') as f:
    content = f.read()

# Find and remove main block
main_idx = content.find("if __name__ == '__main__':")
if main_idx != -1:
    content = content[:main_idx]

# Create globals dict for exec
local_ns = {}
exec(content, local_ns)

# Pull needed classes into local scope
WIDTH = local_ns['WIDTH']
HEIGHT = local_ns['HEIGHT']
ParticleSystem = local_ns['AdvancedParticleSystem']  # Note: named AdvancedParticleSystem
Camera = local_ns['Camera']
LightingSystem = local_ns['LightingSystem']
WeatherSystem = local_ns['WeatherSystem']
TransitionManager = local_ns['TransitionManager']
NarrationSystem = local_ns['NarrationSystem']
SlowMotionManager = local_ns['SlowMotionManager']

TitleScene = local_ns['TitleScene']
ChapterScene = local_ns['ChapterScene']
StoryScene = local_ns['StoryScene']
TransformScene = local_ns['TransformScene']
BattleScene = local_ns['BattleScene']
FlashbackScene = local_ns['FlashbackScene']
ProphecyScene = local_ns['ProphecyScene']
TrainingMontageScene = local_ns['TrainingMontageScene']
SacrificeScene = local_ns['SacrificeScene']
ArmyBattleScene = local_ns['ArmyBattleScene']
CoronationScene = local_ns['CoronationScene']
CreditsScene = local_ns['CreditsScene']

# Create systems in order (some depend on others)
particles = ParticleSystem()
camera = Camera(WIDTH, HEIGHT)
lighting = LightingSystem()
weather = WeatherSystem(particles)  # Needs particles
transitions = TransitionManager()
narration = NarrationSystem()
slowmo = SlowMotionManager()

# Create the context
ctx = {
    'particles': particles,
    'camera': camera,
    'lighting': lighting,
    'weather': weather,
    'transitions': transitions,
    'narration': narration,
    'slowmo': slowmo
}

# Test all scene types
scene_tests = [
    ("TitleScene", lambda: TitleScene(0, 300)),
    ("ChapterScene", lambda: ChapterScene(0, 180, 1, "TEST")),
    ("StoryScene-pond", lambda: StoryScene(0, 300, 'pond', "Test")),
    ("StoryScene-forest", lambda: StoryScene(0, 300, 'forest', "Test")),
    ("StoryScene-mountain", lambda: StoryScene(0, 300, 'mountain', "Test")),
    ("StoryScene-village", lambda: StoryScene(0, 300, 'village', "Test")),
    ("StoryScene-castle", lambda: StoryScene(0, 300, 'castle', "Test")),
    ("StoryScene-dark_swamp", lambda: StoryScene(0, 300, 'dark_swamp', "Test")),
    ("TransformScene", lambda: TransformScene(0, 300)),
    ("BattleScene-serpent", lambda: BattleScene(0, 300, 'serpent')),
    ("BattleScene-heron", lambda: BattleScene(0, 300, 'heron')),
    ("BattleScene-dark_one", lambda: BattleScene(0, 300, 'dark_one')),
    ("FlashbackScene-happy", lambda: FlashbackScene(0, 300, 'happy')),
    ("FlashbackScene-sad", lambda: FlashbackScene(0, 300, 'sad')),
    ("FlashbackScene-origin", lambda: FlashbackScene(0, 300, 'origin')),
    ("ProphecyScene", lambda: ProphecyScene(0, 300)),
    ("TrainingMontageScene", lambda: TrainingMontageScene(0, 600)),
    ("SacrificeScene-sacrifice", lambda: SacrificeScene(0, 300, True)),
    ("SacrificeScene-resurrection", lambda: SacrificeScene(0, 300, False)),
    ("ArmyBattleScene", lambda: ArmyBattleScene(0, 300)),
    ("CoronationScene", lambda: CoronationScene(0, 300)),
    ("CreditsScene", lambda: CreditsScene(0, 500)),
]

all_passed = True
failed_tests = []

for scene_name, scene_factory in scene_tests:
    try:
        scene = scene_factory()
        # Test at multiple frames
        test_frames = [0, scene.duration // 4, scene.duration // 2,
                       3 * scene.duration // 4, scene.duration - 1]

        for test_frame in test_frames:
            fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100))
            ax.set_xlim(0, WIDTH)
            ax.set_ylim(0, HEIGHT)
            ax.set_aspect('equal')

            np.random.seed(42)
            scene.render(ax, test_frame, ctx)
            plt.close(fig)

        print(f"✓ {scene_name}: PASSED")

    except Exception as e:
        all_passed = False
        failed_tests.append((scene_name, str(e), test_frame))
        print(f"✗ {scene_name}: FAILED at frame {test_frame} - {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 60)
if all_passed:
    print("ALL SCENE TESTS PASSED!")
else:
    print(f"FAILED TESTS: {len(failed_tests)}")
    for name, error, frame in failed_tests:
        print(f"  - {name} at frame {frame}: {error}")
print("=" * 60)
