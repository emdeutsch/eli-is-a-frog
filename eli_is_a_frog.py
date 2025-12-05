#!/usr/bin/env python3
"""
ELI IS A FROG - THE ULTIMATE CINEMATIC EXPERIENCE
Director's Cut Extended Edition - Matplotlib Version

A smooth, cinematic animation featuring Eli the Frog's epic journey.
Includes original soundtrack and particle effects.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.collections import PathCollection
from matplotlib.path import Path
import subprocess
import tempfile
import os
import wave
import struct
import math

# ============================================================================
# CONFIGURATION
# ============================================================================
FPS = 60  # Smooth 60fps
DURATION = 150  # 2.5 minutes (5x longer than original ~30 sec)
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 1920, 1080  # Full HD

# Color palette (frog-themed)
COLORS = {
    'bg_day': '#87CEEB',
    'bg_night': '#1a1a2e',
    'bg_sunset': '#ff6b6b',
    'pond': '#2d5a7b',
    'pond_light': '#4a90a4',
    'lilypad': '#228b22',
    'lilypad_dark': '#1a6b1a',
    'frog_body': '#32CD32',
    'frog_dark': '#228b22',
    'frog_belly': '#90EE90',
    'eye_white': '#FFFFFF',
    'eye_pupil': '#000000',
    'fly': '#333333',
    'sun': '#FFD700',
    'moon': '#F5F5DC',
    'star': '#FFFFFF',
    'text': '#FFFFFF',
    'cattail': '#8B4513',
    'reed': '#556B2F',
}

# ============================================================================
# SOUND GENERATION
# ============================================================================
def generate_soundtrack(duration, sample_rate=44100):
    """Generate a fun frog-themed soundtrack"""
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples)

    # Base ambient water sounds (filtered noise)
    np.random.seed(42)
    water = np.random.randn(samples) * 0.02
    # Low-pass filter simulation
    for i in range(1, len(water)):
        water[i] = water[i-1] * 0.95 + water[i] * 0.05

    # Ribbit sounds at intervals
    ribbit_times = [5, 12, 20, 28, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145]
    ribbit = np.zeros(samples)
    for rt in ribbit_times:
        if rt < duration:
            start = int(rt * sample_rate)
            # Ribbit is a frequency modulated tone
            ribbit_len = int(0.3 * sample_rate)
            ribbit_t = np.linspace(0, 0.3, ribbit_len)
            # Two-tone ribbit
            freq1 = 200 + 100 * np.sin(2 * np.pi * 5 * ribbit_t)
            freq2 = 350 + 150 * np.sin(2 * np.pi * 7 * ribbit_t)
            env = np.exp(-ribbit_t * 8) * (1 - np.exp(-ribbit_t * 50))
            ribbit_sound = (np.sin(2 * np.pi * freq1 * ribbit_t) * 0.3 +
                          np.sin(2 * np.pi * freq2 * ribbit_t) * 0.2) * env
            end = min(start + ribbit_len, samples)
            ribbit[start:end] += ribbit_sound[:end-start]

    # Background music - simple melody
    melody_notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C major scale
    melody = np.zeros(samples)
    note_duration = 0.5
    note_samples = int(note_duration * sample_rate)

    # Create a simple repeating melody pattern
    pattern = [0, 2, 4, 2, 0, 4, 2, 0, 5, 4, 2, 0, 2, 4, 5, 4]
    pattern_duration = len(pattern) * note_duration

    for i in range(int(duration / pattern_duration) + 1):
        for j, note_idx in enumerate(pattern):
            start = int((i * pattern_duration + j * note_duration) * sample_rate)
            if start + note_samples > samples:
                break
            freq = melody_notes[note_idx]
            note_t = np.linspace(0, note_duration, note_samples)
            envelope = np.exp(-note_t * 2) * (1 - np.exp(-note_t * 30))
            note = np.sin(2 * np.pi * freq * note_t) * envelope * 0.08
            # Add some harmonics
            note += np.sin(4 * np.pi * freq * note_t) * envelope * 0.03
            end = min(start + note_samples, samples)
            melody[start:end] += note[:end-start]

    # Splash sounds during action scenes
    splash_times = [25, 50, 75, 100, 125]
    splash = np.zeros(samples)
    for st in splash_times:
        if st < duration:
            start = int(st * sample_rate)
            splash_len = int(0.5 * sample_rate)
            splash_t = np.linspace(0, 0.5, splash_len)
            env = np.exp(-splash_t * 6)
            splash_sound = np.random.randn(splash_len) * env * 0.15
            # Filter
            for k in range(1, len(splash_sound)):
                splash_sound[k] = splash_sound[k-1] * 0.7 + splash_sound[k] * 0.3
            end = min(start + splash_len, samples)
            splash[start:end] += splash_sound[:end-start]

    # Combine all sounds
    audio = water + ribbit + melody + splash

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8

    return audio, sample_rate


def save_wav(filename, audio, sample_rate=44100):
    """Save audio as WAV file"""
    audio_int = np.int16(audio * 32767)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int.tobytes())


# ============================================================================
# PARTICLE SYSTEM
# ============================================================================
class ParticleSystem:
    def __init__(self, max_particles=500):
        self.max_particles = max_particles
        self.positions = np.zeros((max_particles, 2))
        self.velocities = np.zeros((max_particles, 2))
        self.lifetimes = np.zeros(max_particles)
        self.colors = np.zeros((max_particles, 4))
        self.sizes = np.zeros(max_particles)
        self.active = np.zeros(max_particles, dtype=bool)
        self.next_idx = 0

    def emit(self, x, y, count=10, spread=50, speed=2, lifetime=60,
             color=(1, 1, 1, 1), size=20):
        """Emit particles from a point"""
        for _ in range(count):
            if self.next_idx >= self.max_particles:
                self.next_idx = 0
            idx = self.next_idx

            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, spread)
            v = np.random.uniform(0.5, 1.5) * speed

            self.positions[idx] = [x + r * np.cos(angle), y + r * np.sin(angle)]
            self.velocities[idx] = [v * np.cos(angle), v * np.sin(angle)]
            self.lifetimes[idx] = lifetime + np.random.randint(-10, 10)
            self.colors[idx] = color
            self.sizes[idx] = size * np.random.uniform(0.5, 1.5)
            self.active[idx] = True
            self.next_idx += 1

    def update(self):
        """Update all particles"""
        self.positions[self.active] += self.velocities[self.active]
        self.lifetimes[self.active] -= 1
        # Apply gravity
        self.velocities[self.active, 1] -= 0.1
        # Fade out
        mask = self.active & (self.lifetimes > 0)
        fade = self.lifetimes[mask] / 60
        self.colors[mask, 3] = np.clip(fade, 0, 1)
        # Deactivate dead particles
        self.active[self.lifetimes <= 0] = False

    def get_active(self):
        """Get active particle data"""
        mask = self.active
        return (self.positions[mask], self.colors[mask], self.sizes[mask])


# ============================================================================
# FROG CLASS
# ============================================================================
class Frog:
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale
        self.emotion = 'normal'
        self.blink_timer = 0
        self.mouth_open = 0
        self.jump_offset = 0
        self.facing = 1  # 1 = right, -1 = left

    def get_patches(self, ax, frame):
        """Generate all patches for the frog"""
        patches_list = []
        x, y = self.x, self.y + self.jump_offset
        s = self.scale * 50

        # Body (ellipse)
        body = patches.Ellipse((x, y), s * 2, s * 1.5,
                                color=COLORS['frog_body'], zorder=10)
        patches_list.append(body)

        # Belly
        belly = patches.Ellipse((x, y - s * 0.1), s * 1.4, s * 1.0,
                                 color=COLORS['frog_belly'], zorder=11)
        patches_list.append(belly)

        # Eyes
        eye_offset = s * 0.4
        eye_size = s * 0.4
        self.blink_timer = (self.blink_timer + 1) % 120
        blink = self.blink_timer > 115

        for side in [-1, 1]:
            # Eye bulge
            eye_bulge = patches.Circle((x + side * eye_offset, y + s * 0.5),
                                        eye_size * 0.6, color=COLORS['frog_body'], zorder=12)
            patches_list.append(eye_bulge)

            # Eye white
            if not blink:
                eye_white = patches.Circle((x + side * eye_offset, y + s * 0.5),
                                           eye_size * 0.4, color=COLORS['eye_white'], zorder=13)
                patches_list.append(eye_white)

                # Pupil (follows scene)
                pupil_offset_x = np.sin(frame * 0.02) * eye_size * 0.1
                pupil = patches.Circle((x + side * eye_offset + pupil_offset_x, y + s * 0.5),
                                       eye_size * 0.2, color=COLORS['eye_pupil'], zorder=14)
                patches_list.append(pupil)
            else:
                # Closed eye line
                eye_line = patches.Rectangle((x + side * eye_offset - eye_size * 0.3,
                                              y + s * 0.5 - s * 0.02),
                                             eye_size * 0.6, s * 0.04,
                                             color=COLORS['frog_dark'], zorder=13)
                patches_list.append(eye_line)

        # Mouth
        if self.emotion == 'happy' or self.mouth_open > 0:
            mouth = patches.Arc((x, y - s * 0.2), s * 0.8, s * 0.4,
                               angle=0, theta1=200, theta2=340,
                               color=COLORS['frog_dark'], linewidth=3, zorder=15)
        else:
            mouth = patches.Arc((x, y - s * 0.2), s * 0.6, s * 0.2,
                               angle=0, theta1=200, theta2=340,
                               color=COLORS['frog_dark'], linewidth=2, zorder=15)
        patches_list.append(mouth)

        # Legs
        leg_y = y - s * 0.7
        for side in [-1, 1]:
            # Back leg
            leg = patches.Ellipse((x + side * s * 0.6, leg_y),
                                  s * 0.5, s * 0.3, angle=side * 20,
                                  color=COLORS['frog_dark'], zorder=9)
            patches_list.append(leg)

            # Front leg
            front_leg = patches.Ellipse((x + side * s * 0.3, leg_y + s * 0.1),
                                        s * 0.3, s * 0.2, angle=side * -10,
                                        color=COLORS['frog_dark'], zorder=9)
            patches_list.append(front_leg)

        # Add expression-specific elements
        if self.emotion == 'love':
            # Hearts floating up
            for i in range(3):
                heart_y = y + s * (0.8 + (frame * 0.02 + i * 0.5) % 1.5)
                heart_x = x + s * 0.5 + np.sin(frame * 0.05 + i) * s * 0.3
                heart = patches.RegularPolygon((heart_x, heart_y), numVertices=3,
                                               radius=s * 0.15, orientation=np.pi,
                                               color='#FF69B4', zorder=20)
                patches_list.append(heart)

        elif self.emotion == 'singing':
            # Music notes
            for i in range(2):
                note_x = x + s * (0.8 + i * 0.4)
                note_y = y + s * 0.3 + np.sin(frame * 0.1 + i) * s * 0.2
                note = patches.Circle((note_x, note_y), s * 0.08,
                                      color='#FFD700', zorder=20)
                patches_list.append(note)

        return patches_list


# ============================================================================
# SCENE CLASSES
# ============================================================================
class Scene:
    """Base class for all scenes"""
    def __init__(self, start_frame, duration):
        self.start_frame = start_frame
        self.end_frame = start_frame + duration
        self.duration = duration

    def render(self, ax, frame, particles):
        raise NotImplementedError


class TitleScene(Scene):
    """Epic title screen"""
    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame
        progress = local_frame / self.duration

        # Animated gradient background
        ax.set_facecolor('#000022')

        # Stars
        np.random.seed(42)
        n_stars = 100
        star_x = np.random.rand(n_stars) * WIDTH
        star_y = np.random.rand(n_stars) * HEIGHT
        star_alpha = 0.3 + 0.7 * np.abs(np.sin(local_frame * 0.05 + np.random.rand(n_stars) * 10))
        star_alpha = np.clip(star_alpha, 0.1, 1.0)
        ax.scatter(star_x, star_y, c='white', s=star_alpha * 30, alpha=star_alpha, zorder=1)

        # Title text
        title_y = HEIGHT * 0.65 + np.sin(local_frame * 0.03) * 20

        # Glow effect
        for i in range(3):
            ax.text(WIDTH/2, title_y, "ELI IS A FROG",
                   fontsize=80 + i*5, fontweight='bold',
                   ha='center', va='center',
                   color='#32CD32', alpha=0.2 - i*0.05,
                   family='monospace', zorder=10-i)

        ax.text(WIDTH/2, title_y, "ELI IS A FROG",
               fontsize=80, fontweight='bold',
               ha='center', va='center',
               color='#90EE90',
               family='monospace', zorder=11)

        # Subtitle with fade-in
        sub_alpha = min(1, (local_frame - 30) / 30) if local_frame > 30 else 0
        ax.text(WIDTH/2, HEIGHT * 0.45,
               "THE ULTIMATE CINEMATIC EXPERIENCE",
               fontsize=24, ha='center', va='center',
               color='#FFD700', alpha=sub_alpha,
               family='monospace', zorder=11)

        ax.text(WIDTH/2, HEIGHT * 0.38,
               "Director's Cut Extended Edition",
               fontsize=18, ha='center', va='center',
               color='#87CEEB', alpha=sub_alpha * 0.8,
               family='monospace', zorder=11)

        # Dancing frogs at bottom
        if local_frame > 60:
            for i in range(5):
                frog_x = WIDTH * (0.2 + i * 0.15)
                bounce = np.sin(local_frame * 0.15 + i * 0.8) * 20
                frog = Frog(frog_x, HEIGHT * 0.2 + bounce, scale=0.6)
                frog.emotion = 'happy'
                for p in frog.get_patches(ax, local_frame):
                    ax.add_patch(p)

        # Particles for sparkle effect
        if local_frame % 10 == 0:
            particles.emit(WIDTH/2 + np.random.randn() * 200,
                          HEIGHT * 0.65, count=5, spread=100,
                          color=(1, 0.84, 0, 0.8), lifetime=40)


class PondScene(Scene):
    """Main pond environment scene"""
    def __init__(self, start_frame, duration, time_of_day='day'):
        super().__init__(start_frame, duration)
        self.time_of_day = time_of_day
        self.frog = Frog(WIDTH * 0.5, HEIGHT * 0.4, scale=1.2)
        self.flies = [(np.random.rand() * WIDTH * 0.8 + WIDTH * 0.1,
                      np.random.rand() * HEIGHT * 0.3 + HEIGHT * 0.5)
                     for _ in range(8)]
        self.fly_phases = np.random.rand(8) * 2 * np.pi

    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame

        # Sky gradient based on time of day
        if self.time_of_day == 'day':
            ax.set_facecolor('#87CEEB')
            # Sun
            sun = patches.Circle((WIDTH * 0.85, HEIGHT * 0.85), 60,
                                color='#FFD700', zorder=1)
            ax.add_patch(sun)
            # Sun rays
            for i in range(8):
                angle = i * np.pi / 4 + local_frame * 0.01
                ray_x = WIDTH * 0.85 + np.cos(angle) * 90
                ray_y = HEIGHT * 0.85 + np.sin(angle) * 90
                ax.plot([WIDTH * 0.85, ray_x], [HEIGHT * 0.85, ray_y],
                       color='#FFD700', linewidth=4, alpha=0.6, zorder=0)

        elif self.time_of_day == 'night':
            ax.set_facecolor('#1a1a2e')
            # Moon
            moon = patches.Circle((WIDTH * 0.85, HEIGHT * 0.85), 50,
                                 color='#F5F5DC', zorder=1)
            ax.add_patch(moon)
            # Stars
            np.random.seed(123)
            for _ in range(50):
                sx, sy = np.random.rand() * WIDTH, HEIGHT * 0.5 + np.random.rand() * HEIGHT * 0.5
                twinkle = 0.3 + 0.7 * abs(np.sin(local_frame * 0.1 + np.random.rand() * 10))
                twinkle = max(0.1, min(1.0, twinkle))
                ax.scatter([sx], [sy], c='white', s=twinkle * 20, alpha=twinkle)

        elif self.time_of_day == 'sunset':
            ax.set_facecolor('#ff6b6b')
            # Gradient effect with rectangles
            for i in range(10):
                h = HEIGHT * (0.5 + i * 0.05)
                alpha = max(0.1, 0.3 - i * 0.02)
                rect = patches.Rectangle((0, h), WIDTH, HEIGHT * 0.05,
                                         color='#FF8C00', alpha=alpha, zorder=0)
                ax.add_patch(rect)

        # Pond water
        pond = patches.Rectangle((0, 0), WIDTH, HEIGHT * 0.35,
                                 color=COLORS['pond'], zorder=2)
        ax.add_patch(pond)

        # Water ripples
        for i in range(5):
            wave_y = HEIGHT * 0.35 - i * 15
            phase = local_frame * 0.05 + i * 0.5
            wave_x = np.linspace(0, WIDTH, 100)
            wave_heights = wave_y + np.sin(wave_x * 0.02 + phase) * 5
            ax.fill_between(wave_x, wave_heights, wave_y - 10,
                           color=COLORS['pond_light'], alpha=0.3, zorder=3)

        # Lily pads
        lilypad_positions = [(WIDTH * 0.2, HEIGHT * 0.25),
                            (WIDTH * 0.5, HEIGHT * 0.2),
                            (WIDTH * 0.75, HEIGHT * 0.28)]
        for lx, ly in lilypad_positions:
            pad = patches.Ellipse((lx, ly), 120, 80,
                                 color=COLORS['lilypad'], zorder=4)
            ax.add_patch(pad)
            # Pad detail
            pad_line = patches.Wedge((lx, ly), 50, 170, 190,
                                    color=COLORS['lilypad_dark'], zorder=5)
            ax.add_patch(pad_line)

        # Cattails/reeds
        reed_positions = [50, 150, WIDTH - 100, WIDTH - 50]
        for rx in reed_positions:
            for h in range(6):
                ry = HEIGHT * 0.35 + h * 30
                sway = np.sin(local_frame * 0.03 + rx * 0.01) * 5
                reed = patches.Rectangle((rx + sway - 3, ry), 6, 25,
                                        color=COLORS['reed'], zorder=4)
                ax.add_patch(reed)
            # Cattail head
            head = patches.Ellipse((rx + sway, HEIGHT * 0.35 + 200), 15, 35,
                                  color=COLORS['cattail'], zorder=5)
            ax.add_patch(head)

        # Main frog on lilypad
        self.frog.x = WIDTH * 0.5
        self.frog.y = HEIGHT * 0.25
        self.frog.jump_offset = np.sin(local_frame * 0.05) * 5

        # Animate emotion changes
        if local_frame < self.duration * 0.3:
            self.frog.emotion = 'normal'
        elif local_frame < self.duration * 0.6:
            self.frog.emotion = 'happy'
        else:
            self.frog.emotion = 'singing'

        for p in self.frog.get_patches(ax, local_frame):
            ax.add_patch(p)

        # Flies
        for i, (fx, fy) in enumerate(self.flies):
            fly_x = fx + np.sin(local_frame * 0.1 + self.fly_phases[i]) * 30
            fly_y = fy + np.cos(local_frame * 0.15 + self.fly_phases[i]) * 20
            fly = patches.Circle((fly_x, fly_y), 5, color='#333333', zorder=15)
            ax.add_patch(fly)
            # Wings
            wing_spread = 3 + 2 * np.sin(local_frame * 0.5)
            ax.plot([fly_x - wing_spread, fly_x, fly_x + wing_spread],
                   [fly_y + 3, fly_y, fly_y + 3],
                   color='#666666', linewidth=1, alpha=0.7, zorder=15)

        # Occasional splash particles
        if local_frame % 60 == 0:
            particles.emit(WIDTH * 0.5, HEIGHT * 0.2,
                          count=15, spread=30, speed=3,
                          color=(0.4, 0.6, 1, 0.8), lifetime=40)

        # Dragonfly
        df_x = (local_frame * 5) % (WIDTH + 200) - 100
        df_y = HEIGHT * 0.6 + np.sin(local_frame * 0.05) * 50
        ax.plot([df_x - 20, df_x + 20], [df_y, df_y],
               color='#00CED1', linewidth=3, zorder=16)
        ax.scatter([df_x], [df_y], c='#008B8B', s=50, zorder=16)


class TransformationScene(Scene):
    """Eli transforms into a frog"""
    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame
        progress = local_frame / self.duration

        # Mystical background
        ax.set_facecolor('#2d0a4e')

        # Swirling particles
        np.random.seed(int(local_frame / 10))
        n_swirl = 50
        for i in range(n_swirl):
            angle = (i / n_swirl) * 2 * np.pi + local_frame * 0.02
            r = 100 + 300 * (1 + np.sin(local_frame * 0.01 + i))
            px = WIDTH/2 + r * np.cos(angle)
            py = HEIGHT/2 + r * np.sin(angle) * 0.6
            size = max(5, 10 + 20 * np.sin(local_frame * 0.05 + i))
            color = '#9400D3' if i % 2 == 0 else '#00FF00'
            ax.scatter([px], [py], c=color, s=size, alpha=0.6, zorder=5)

        # Central transformation circle
        circle_size = max(100, 150 + 50 * np.sin(local_frame * 0.1))
        for ring in range(3):
            alpha_val = max(0.1, 0.5 - ring * 0.1)
            circle = patches.Circle((WIDTH/2, HEIGHT/2),
                                   circle_size + ring * 30,
                                   fill=False, edgecolor='#FFD700',
                                   linewidth=3, alpha=alpha_val, zorder=10)
            ax.add_patch(circle)

        # Transform from human silhouette to frog
        if progress < 0.5:
            # Human silhouette
            human_alpha = 1 - progress * 2
            human_head = patches.Circle((WIDTH/2, HEIGHT/2 + 100), 40,
                                        color='white', alpha=human_alpha, zorder=11)
            ax.add_patch(human_head)
            human_body = patches.Rectangle((WIDTH/2 - 30, HEIGHT/2 - 60), 60, 120,
                                          color='white', alpha=human_alpha, zorder=11)
            ax.add_patch(human_body)

        # Frog emerges
        frog_alpha = max(0, (progress - 0.3) / 0.7)
        if frog_alpha > 0:
            frog = Frog(WIDTH/2, HEIGHT/2, scale=1.5 + progress)
            frog.emotion = 'happy' if progress > 0.8 else 'scared'
            for p in frog.get_patches(ax, local_frame):
                p.set_alpha(frog_alpha)
                ax.add_patch(p)

        # Magic particles
        if local_frame % 5 == 0:
            for _ in range(3):
                particles.emit(WIDTH/2 + np.random.randn() * 100,
                             HEIGHT/2 + np.random.randn() * 100,
                             count=5, spread=50, speed=2,
                             color=(0.5, 1, 0.5, 0.8), lifetime=50)

        # Text
        if progress > 0.7:
            text_alpha = (progress - 0.7) / 0.3
            ax.text(WIDTH/2, HEIGHT * 0.15,
                   "THE TRANSFORMATION IS COMPLETE",
                   fontsize=32, ha='center', va='center',
                   color='#FFD700', alpha=text_alpha,
                   fontweight='bold', family='monospace', zorder=20)


class BossFightScene(Scene):
    """Epic boss battle with the Great Heron"""
    def __init__(self, start_frame, duration):
        super().__init__(start_frame, duration)
        self.boss_health = 100
        self.frog_health = 100
        self.boss_x = WIDTH * 0.7
        self.frog = Frog(WIDTH * 0.3, HEIGHT * 0.3, scale=1.0)

    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame
        progress = local_frame / self.duration

        # Dramatic red-tinted background
        ax.set_facecolor('#2a0a0a')

        # Ground
        ground = patches.Rectangle((0, 0), WIDTH, HEIGHT * 0.3,
                                   color='#3d2914', zorder=1)
        ax.add_patch(ground)

        # Boss: The Great Heron
        heron_x = self.boss_x + np.sin(local_frame * 0.03) * 30
        heron_y = HEIGHT * 0.35

        # Heron body
        body = patches.Ellipse((heron_x, heron_y + 100), 80, 150,
                              color='#E8E8E8', zorder=10)
        ax.add_patch(body)

        # Heron head
        head = patches.Ellipse((heron_x + 40, heron_y + 200), 50, 40,
                              color='#E8E8E8', zorder=11)
        ax.add_patch(head)

        # Heron beak (threatening)
        beak_open = 5 + 10 * np.sin(local_frame * 0.2)
        ax.fill([heron_x + 60, heron_x + 120, heron_x + 60],
               [heron_y + 210, heron_y + 200, heron_y + 190 - beak_open],
               color='#FFA500', zorder=12)
        ax.fill([heron_x + 60, heron_x + 120, heron_x + 60],
               [heron_y + 190, heron_y + 200, heron_y + 200],
               color='#FF8C00', zorder=12)

        # Heron eye (menacing)
        ax.scatter([heron_x + 50], [heron_y + 210], c='red', s=100, zorder=13)
        ax.scatter([heron_x + 52], [heron_y + 212], c='black', s=30, zorder=14)

        # Heron legs
        for offset in [-20, 20]:
            ax.plot([heron_x + offset, heron_x + offset - 10],
                   [heron_y, heron_y - 80],
                   color='#FFA500', linewidth=5, zorder=9)

        # Boss health bar
        ax.add_patch(patches.Rectangle((WIDTH/2 - 200, HEIGHT - 80), 400, 30,
                                       color='#333333', zorder=20))
        self.boss_health = max(0, 100 - progress * 100)
        ax.add_patch(patches.Rectangle((WIDTH/2 - 195, HEIGHT - 75),
                                       390 * (self.boss_health / 100), 20,
                                       color='#FF0000', zorder=21))
        ax.text(WIDTH/2, HEIGHT - 100, "THE GREAT HERON",
               fontsize=20, ha='center', color='#FF4444',
               fontweight='bold', family='monospace', zorder=22)

        # Eli the frog (battle stance)
        frog_x = WIDTH * 0.25 + np.sin(local_frame * 0.05) * 20
        self.frog.x = frog_x
        self.frog.y = HEIGHT * 0.35
        self.frog.emotion = 'angry' if progress < 0.8 else 'happy'

        # Frog jumping attacks
        if local_frame % 60 < 30:
            self.frog.jump_offset = np.sin((local_frame % 60) / 30 * np.pi) * 100
            if local_frame % 60 == 15:
                particles.emit(frog_x, HEIGHT * 0.35, count=20, spread=20,
                             speed=5, color=(0.2, 1, 0.2, 1), lifetime=30)
        else:
            self.frog.jump_offset = 0

        for p in self.frog.get_patches(ax, local_frame):
            ax.add_patch(p)

        # Frog health bar
        ax.add_patch(patches.Rectangle((50, 50), 200, 20, color='#333333', zorder=20))
        ax.add_patch(patches.Rectangle((52, 52), 196 * (self.frog_health / 100), 16,
                                       color='#00FF00', zorder=21))
        ax.text(150, 85, "ELI", fontsize=16, ha='center', color='#00FF00',
               fontweight='bold', family='monospace', zorder=22)

        # Battle effects
        if local_frame % 30 == 0:
            # Impact particles
            particles.emit(heron_x, heron_y + 100, count=30, spread=50,
                         speed=4, color=(1, 0.5, 0, 0.9), lifetime=25)

        # Victory when boss defeated
        if progress > 0.95:
            ax.text(WIDTH/2, HEIGHT/2, "VICTORY!",
                   fontsize=72, ha='center', va='center',
                   color='#FFD700', fontweight='bold',
                   family='monospace', zorder=30)


class CreditsScene(Scene):
    """Rolling credits"""
    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame

        ax.set_facecolor('#000000')

        # Stars background
        np.random.seed(999)
        for _ in range(100):
            sx, sy = np.random.rand() * WIDTH, np.random.rand() * HEIGHT
            ax.scatter([sx], [sy], c='white', s=np.random.rand() * 20, alpha=0.7)

        credits = [
            ("ELI IS A FROG", 72, '#90EE90'),
            ("", 30, 'white'),
            ("Directed by", 24, '#888888'),
            ("Claude Code Productions", 36, '#FFD700'),
            ("", 30, 'white'),
            ("Starring", 24, '#888888'),
            ("ELI", 36, '#32CD32'),
            ("as Himself (The Frog)", 20, '#AAAAAA'),
            ("", 30, 'white'),
            ("The Great Heron", 36, '#FFFFFF'),
            ("as The Villain", 20, '#AAAAAA'),
            ("", 30, 'white'),
            ("Visual Effects", 24, '#888888'),
            ("Matplotlib Animation Studio", 28, '#87CEEB'),
            ("", 30, 'white'),
            ("Sound Design", 24, '#888888'),
            ("NumPy Audio Division", 28, '#87CEEB'),
            ("", 30, 'white'),
            ("Special Thanks", 24, '#888888'),
            ("The Flies (for their sacrifice)", 20, '#AAAAAA'),
            ("The Lily Pad Union Local 42", 20, '#AAAAAA'),
            ("", 50, 'white'),
            ("A CLAUDE CODE PRODUCTION", 28, '#FFD700'),
            ("", 30, 'white'),
            ("No frogs were harmed in the making", 16, '#666666'),
            ("of this cinematic experience", 16, '#666666'),
        ]

        scroll_speed = 1.5
        y_start = -local_frame * scroll_speed
        current_y = y_start + HEIGHT * 0.2

        for text, size, color in credits:
            if -100 < current_y < HEIGHT + 100:
                ax.text(WIDTH/2, current_y, text,
                       fontsize=size, ha='center', va='center',
                       color=color, family='monospace', zorder=10)
            current_y += size * 2

        # Frog waving at bottom
        if local_frame > 100:
            frog = Frog(WIDTH * 0.5, 100, scale=0.8)
            frog.emotion = 'happy'
            for p in frog.get_patches(ax, local_frame):
                ax.add_patch(p)


class ChapterTitle(Scene):
    """Chapter title cards"""
    def __init__(self, start_frame, duration, chapter_num, title):
        super().__init__(start_frame, duration)
        self.chapter_num = chapter_num
        self.title = title

    def render(self, ax, frame, particles):
        local_frame = frame - self.start_frame
        progress = local_frame / self.duration

        ax.set_facecolor('#000000')

        # Fade in/out
        alpha = 1.0
        if progress < 0.2:
            alpha = progress / 0.2
        elif progress > 0.8:
            alpha = (1 - progress) / 0.2

        ax.text(WIDTH/2, HEIGHT * 0.55,
               f"═══ CHAPTER {self.chapter_num} ═══",
               fontsize=28, ha='center', va='center',
               color='#FFD700', alpha=alpha,
               family='monospace', zorder=10)

        ax.text(WIDTH/2, HEIGHT * 0.45,
               self.title.upper(),
               fontsize=48, ha='center', va='center',
               color='#FFFFFF', alpha=alpha,
               fontweight='bold', family='monospace', zorder=10)


# ============================================================================
# MAIN ANIMATION
# ============================================================================
def create_animation():
    """Create the full animation"""
    print("Creating ELI IS A FROG - THE ULTIMATE CINEMATIC EXPERIENCE")
    print(f"Duration: {DURATION} seconds at {FPS} fps = {TOTAL_FRAMES} frames")

    # Create figure
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Particle system
    particles = ParticleSystem(max_particles=1000)

    # Define scenes with timing (frame numbers)
    # Total: 9000 frames = 150 seconds
    scenes = [
        # Opening
        TitleScene(0, 480),  # 8 seconds

        # Chapter 1: The Normal Life
        ChapterTitle(480, 180, 1, "The Normal Life"),  # 3 seconds
        PondScene(660, 600, 'day'),  # 10 seconds - establishing shot

        # Chapter 2: The Transformation
        ChapterTitle(1260, 180, 2, "The Transformation"),
        TransformationScene(1440, 600),  # 10 seconds

        # Chapter 3: Life as a Frog
        ChapterTitle(2040, 180, 3, "Life as a Frog"),
        PondScene(2220, 900, 'day'),  # 15 seconds
        PondScene(3120, 600, 'sunset'),  # 10 seconds
        PondScene(3720, 600, 'night'),  # 10 seconds

        # Chapter 4: The Great Heron Appears
        ChapterTitle(4320, 180, 4, "The Predator"),
        PondScene(4500, 300, 'day'),  # 5 seconds - calm before storm

        # Chapter 5: The Battle
        ChapterTitle(4800, 180, 5, "The Final Battle"),
        BossFightScene(4980, 1200),  # 20 seconds - epic boss fight!

        # Chapter 6: Victory
        ChapterTitle(6180, 180, 6, "Victory"),
        PondScene(6360, 900, 'sunset'),  # 15 seconds - celebration

        # Epilogue
        ChapterTitle(7260, 180, 7, "Epilogue"),
        PondScene(7440, 600, 'day'),  # 10 seconds - peaceful ending

        # Credits
        CreditsScene(8040, 960),  # 16 seconds
    ]

    def init():
        ax.clear()
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.set_aspect('equal')
        ax.axis('off')
        return []

    def animate(frame):
        ax.clear()
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(0, HEIGHT)
        ax.set_aspect('equal')
        ax.axis('off')

        # Find current scene
        for scene in scenes:
            if scene.start_frame <= frame < scene.end_frame:
                scene.render(ax, frame, particles)
                break

        # Update and draw particles
        particles.update()
        positions, colors, sizes = particles.get_active()
        if len(positions) > 0 and len(sizes) > 0:
            valid_mask = sizes > 0
            if np.any(valid_mask):
                ax.scatter(positions[valid_mask, 0], positions[valid_mask, 1],
                          c=colors[valid_mask], s=np.clip(sizes[valid_mask], 1, 100), zorder=100)

        # Progress indicator
        progress = frame / TOTAL_FRAMES * 100
        if frame % 100 == 0:
            print(f"\rRendering: {progress:.1f}%", end='', flush=True)

        return []

    print("Setting up animation...")
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=TOTAL_FRAMES, interval=1000/FPS,
                                   blit=False)

    return fig, anim


def main():
    """Main entry point"""
    print("=" * 60)
    print("  ELI IS A FROG - THE ULTIMATE CINEMATIC EXPERIENCE")
    print("  Director's Cut Extended Edition")
    print("=" * 60)
    print()

    # Generate soundtrack
    print("Generating soundtrack...")
    audio, sample_rate = generate_soundtrack(DURATION)

    # Save audio to temp file
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, 'soundtrack.wav')
    save_wav(audio_path, audio, sample_rate)
    print(f"Soundtrack saved to: {audio_path}")

    # Create animation
    fig, anim = create_animation()

    # Save video without audio first
    video_path = os.path.join(temp_dir, 'eli_frog_video.mp4')
    print(f"\nSaving video to: {video_path}")
    print("This may take several minutes...")

    writer = animation.FFMpegWriter(fps=FPS, bitrate=5000,
                                     metadata=dict(title='ELI IS A FROG',
                                                  artist='Claude Code Productions'))
    anim.save(video_path, writer=writer)
    print("\nVideo saved!")

    # Combine video and audio with FFmpeg
    final_path = '/Users/evandeutsch/elifrog/eli_is_a_frog_movie.mp4'
    print(f"\nCombining video and audio...")
    print(f"Final output: {final_path}")

    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        final_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        print(f"\n{'=' * 60}")
        print(f"  SUCCESS! Movie created: {final_path}")
        print(f"  Duration: {DURATION} seconds")
        print(f"  Resolution: {WIDTH}x{HEIGHT}")
        print(f"  Frame rate: {FPS} fps")
        print(f"{'=' * 60}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        print("Video saved without audio at:", video_path)
    except FileNotFoundError:
        print("FFmpeg not found. Video saved without audio at:", video_path)
        print("To add audio manually, install FFmpeg and run:")
        print(f"  ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {final_path}")

    # Cleanup temp files
    try:
        os.remove(video_path)
        os.remove(audio_path)
        os.rmdir(temp_dir)
    except:
        pass

    plt.close(fig)
    print("\nDone!")


if __name__ == '__main__':
    main()
