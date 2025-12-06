#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ███████╗██╗     ██╗    ██╗███████╗     █████╗     ███████╗██████╗  ██████╗  ██████╗    ║
║     ██╔════╝██║     ██║    ██║██╔════╝    ██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗██╔════╝    ║
║     █████╗  ██║     ██║    ██║███████╗    ███████║    █████╗  ██████╔╝██║   ██║██║  ███╗   ║
║     ██╔══╝  ██║     ██║    ██║╚════██║    ██╔══██║    ██╔══╝  ██╔══██╗██║   ██║██║   ██║   ║
║     ███████╗███████╗██║    ██║███████║    ██║  ██║    ██║     ██║  ██║╚██████╔╝╚██████╔╝   ║
║     ╚══════╝╚══════╝╚═╝    ╚═╝╚══════╝    ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ║
║                                                                               ║
║                    THE LEGEND OF THE EMERALD GUARDIAN                         ║
║                                                                               ║
║                   ═══════════════════════════════════                         ║
║                                                                               ║
║                        A CINEMATIC MASTERPIECE                                ║
║                                                                               ║
║     In a world where darkness threatens to consume all light,                 ║
║     one unlikely hero must rise to fulfill an ancient prophecy.               ║
║     This is the tale of Eli - transformed by fate, tested by fire,            ║
║     and destined to become... THE EMERALD GUARDIAN.                           ║
║                                                                               ║
║     Runtime: ~15 minutes | Resolution: 1920x1080 | FPS: 60                    ║
║     Features: Advanced particle systems, dynamic lighting,                    ║
║               parallax scrolling, weather effects, epic soundtrack            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

THE COMPLETE HERO'S JOURNEY - STORY STRUCTURE:

ACT I - THE ORDINARY WORLD
    Chapter 1: Prologue - The Ancient Prophecy
    Chapter 2: Eli's Peaceful Life (The Village)
    Chapter 3: The Call to Adventure (Strange Dreams)

ACT II - CROSSING THE THRESHOLD
    Chapter 4: The Dark Curse (Transformation)
    Chapter 5: Awakening (A New Form)
    Chapter 6: Meeting the Mentor (Sage the Ancient Turtle)

ACT III - TESTS, ALLIES, ENEMIES
    Chapter 7: The Enchanted Swamp (Training Begins)
    Chapter 8: Meeting Allies (Spark the Dragonfly, Luna the Frog Princess)
    Chapter 9: First Trial (The Serpent's Lair)
    Chapter 10: The Village of Frogs (A New Home)

ACT IV - THE APPROACH
    Chapter 11: The Shadow Rises (The Dark One's Army)
    Chapter 12: Love Blossoms (Eli and Luna)
    Chapter 13: The Gathering Storm (Preparing for War)

ACT V - THE ORDEAL
    Chapter 14: Betrayal (The Fallen Friend)
    Chapter 15: Captured (The Darkest Hour)
    Chapter 16: The Abyss (All Hope Lost)

ACT VI - THE REWARD
    Chapter 17: Inner Light (Finding Strength Within)
    Chapter 18: The Escape (Breaking Free)
    Chapter 19: Rallying the Armies (The Final Alliance)

ACT VII - THE ROAD BACK
    Chapter 20: The March to War (Epic Army Gathering)
    Chapter 21: The Final Battle Begins (Clash of Forces)
    Chapter 22: Boss Fight I - The Shadow Serpent
    Chapter 23: Boss Fight II - The Storm Heron

ACT VIII - THE RESURRECTION
    Chapter 24: The Ultimate Sacrifice (Eli Falls)
    Chapter 25: The Prophecy Fulfilled (Rebirth)
    Chapter 26: Boss Fight III - The Dark One (Final Confrontation)

ACT IX - RETURN WITH THE ELIXIR
    Chapter 27: Victory (Light Returns)
    Chapter 28: Coronation (The Emerald Guardian)
    Chapter 29: Happily Ever After (Peace Restored)
    Chapter 30: Epilogue - The Legend Lives On

    Credits - A Claude Code Production

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.collections import PathCollection, PatchCollection
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.transforms as transforms
import subprocess
import tempfile
import os
import wave
import struct
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable, Dict, Any
from enum import Enum, auto
import colorsys

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                            CONFIGURATION                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

FPS = 60  # Silky smooth 60fps
DURATION = 900  # 15 minutes - epic runtime (5x longer than original)
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 1920, 1080  # Full HD cinematic

# ═══════════════════════════════════════════════════════════════════════════════
#                              COLOR PALETTES
# ═══════════════════════════════════════════════════════════════════════════════

class Palette:
    """Cinematic color palettes for different moods and environments"""

    # Sky colors
    SKY_DAY = '#87CEEB'
    SKY_DAWN = '#FFB6C1'
    SKY_SUNSET = '#FF6B4A'
    SKY_DUSK = '#4A3B6B'
    SKY_NIGHT = '#0D1B2A'
    SKY_STORM = '#2C3E50'
    SKY_DARK = '#0A0A0F'

    # Water colors
    WATER_SURFACE = '#2E86AB'
    WATER_DEEP = '#1B4965'
    WATER_SHALLOW = '#5FA8D3'
    WATER_MAGICAL = '#00D4FF'
    WATER_DARK = '#0D2137'

    # Nature colors
    GRASS_LIGHT = '#90EE90'
    GRASS_NORMAL = '#228B22'
    GRASS_DARK = '#1A5C1A'
    LILYPAD_LIGHT = '#32CD32'
    LILYPAD_NORMAL = '#228B22'
    LILYPAD_DARK = '#1A6B1A'
    TREE_TRUNK = '#8B4513'
    TREE_LEAVES = '#2D5A27'
    REED = '#556B2F'
    CATTAIL = '#8B4513'
    FLOWER_PINK = '#FF69B4'
    FLOWER_YELLOW = '#FFD700'
    FLOWER_WHITE = '#FFFAFA'

    # Frog colors
    FROG_BODY = '#32CD32'
    FROG_BELLY = '#90EE90'
    FROG_DARK = '#228B22'
    FROG_GOLDEN = '#FFD700'
    FROG_BLUE = '#4169E1'
    FROG_RED = '#DC143C'
    EYE_WHITE = '#FFFFFF'
    EYE_PUPIL = '#000000'
    EYE_GOLDEN = '#FFD700'

    # Magic colors
    MAGIC_GREEN = '#00FF7F'
    MAGIC_BLUE = '#00BFFF'
    MAGIC_PURPLE = '#9400D3'
    MAGIC_GOLD = '#FFD700'
    MAGIC_WHITE = '#FFFFFF'
    MAGIC_DARK = '#4B0082'
    MAGIC_FIRE = '#FF4500'
    MAGIC_ICE = '#ADD8E6'

    # Evil colors
    EVIL_BLACK = '#0D0D0D'
    EVIL_PURPLE = '#2D0A4E'
    EVIL_RED = '#8B0000'
    EVIL_GREEN = '#006400'
    SHADOW = '#1A1A2E'

    # UI colors
    TEXT_WHITE = '#FFFFFF'
    TEXT_GOLD = '#FFD700'
    TEXT_SILVER = '#C0C0C0'
    HEALTH_GREEN = '#00FF00'
    HEALTH_RED = '#FF0000'
    HEALTH_YELLOW = '#FFFF00'

    # Celestial
    SUN = '#FFD700'
    SUN_GLOW = '#FFA500'
    MOON = '#F5F5DC'
    MOON_GLOW = '#E6E6FA'
    STAR = '#FFFFFF'

    # Weather
    RAIN = '#87CEEB'
    LIGHTNING = '#F0E68C'
    SNOW = '#FFFAFA'
    FOG = '#D3D3D3'


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                          EASING FUNCTIONS                                     ║
# ║         For smooth, professional-quality animation motion                     ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class Easing:
    """
    Professional easing functions for cinematic animation.
    All functions take t in [0, 1] and return value in [0, 1].
    Based on Robert Penner's easing equations.
    """

    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation - constant speed"""
        return t

    # ═══════════════════════ QUADRATIC ═══════════════════════

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease in - accelerating from zero velocity"""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease out - decelerating to zero velocity"""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease in/out - acceleration until halfway, then deceleration"""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    # ═══════════════════════ CUBIC ═══════════════════════

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease in - accelerating from zero velocity"""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease out - decelerating to zero velocity"""
        t -= 1
        return t * t * t + 1

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease in/out - acceleration until halfway, then deceleration"""
        if t < 0.5:
            return 4 * t * t * t
        t = 2 * t - 2
        return 0.5 * t * t * t + 1

    # ═══════════════════════ QUARTIC ═══════════════════════

    @staticmethod
    def ease_in_quart(t: float) -> float:
        """Quartic ease in"""
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t: float) -> float:
        """Quartic ease out"""
        t -= 1
        return 1 - t * t * t * t

    @staticmethod
    def ease_in_out_quart(t: float) -> float:
        """Quartic ease in/out"""
        if t < 0.5:
            return 8 * t * t * t * t
        t -= 1
        return 1 - 8 * t * t * t * t

    # ═══════════════════════ QUINTIC ═══════════════════════

    @staticmethod
    def ease_in_quint(t: float) -> float:
        """Quintic ease in"""
        return t * t * t * t * t

    @staticmethod
    def ease_out_quint(t: float) -> float:
        """Quintic ease out"""
        t -= 1
        return t * t * t * t * t + 1

    @staticmethod
    def ease_in_out_quint(t: float) -> float:
        """Quintic ease in/out"""
        if t < 0.5:
            return 16 * t * t * t * t * t
        t -= 1
        return 16 * t * t * t * t * t + 1

    # ═══════════════════════ SINUSOIDAL ═══════════════════════

    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sinusoidal ease in"""
        return 1 - np.cos(t * np.pi / 2)

    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sinusoidal ease out"""
        return np.sin(t * np.pi / 2)

    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sinusoidal ease in/out"""
        return 0.5 * (1 - np.cos(np.pi * t))

    # ═══════════════════════ EXPONENTIAL ═══════════════════════

    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease in"""
        return 0 if t == 0 else 2 ** (10 * (t - 1))

    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease out"""
        return 1 if t == 1 else 1 - 2 ** (-10 * t)

    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        """Exponential ease in/out"""
        if t == 0:
            return 0
        if t == 1:
            return 1
        if t < 0.5:
            return 0.5 * 2 ** (10 * (2 * t - 1))
        return 0.5 * (2 - 2 ** (-10 * (2 * t - 1)))

    # ═══════════════════════ CIRCULAR ═══════════════════════

    @staticmethod
    def ease_in_circ(t: float) -> float:
        """Circular ease in"""
        return 1 - np.sqrt(1 - t * t)

    @staticmethod
    def ease_out_circ(t: float) -> float:
        """Circular ease out"""
        t -= 1
        return np.sqrt(1 - t * t)

    @staticmethod
    def ease_in_out_circ(t: float) -> float:
        """Circular ease in/out"""
        if t < 0.5:
            return 0.5 * (1 - np.sqrt(1 - 4 * t * t))
        t = 2 * t - 2
        return 0.5 * (np.sqrt(1 - t * t) + 1)

    # ═══════════════════════ ELASTIC ═══════════════════════

    @staticmethod
    def ease_in_elastic(t: float) -> float:
        """Elastic ease in - like a spring"""
        if t == 0:
            return 0
        if t == 1:
            return 1
        p = 0.3
        s = p / 4
        t -= 1
        return -(2 ** (10 * t) * np.sin((t - s) * (2 * np.pi) / p))

    @staticmethod
    def ease_out_elastic(t: float) -> float:
        """Elastic ease out"""
        if t == 0:
            return 0
        if t == 1:
            return 1
        p = 0.3
        s = p / 4
        return 2 ** (-10 * t) * np.sin((t - s) * (2 * np.pi) / p) + 1

    @staticmethod
    def ease_in_out_elastic(t: float) -> float:
        """Elastic ease in/out"""
        if t == 0:
            return 0
        if t == 1:
            return 1
        p = 0.45
        s = p / 4
        t = 2 * t
        if t < 1:
            t -= 1
            return -0.5 * (2 ** (10 * t) * np.sin((t - s) * (2 * np.pi) / p))
        t -= 1
        return 2 ** (-10 * t) * np.sin((t - s) * (2 * np.pi) / p) * 0.5 + 1

    # ═══════════════════════ BACK ═══════════════════════

    @staticmethod
    def ease_in_back(t: float) -> float:
        """Back ease in - slight overshoot backwards"""
        s = 1.70158
        return t * t * ((s + 1) * t - s)

    @staticmethod
    def ease_out_back(t: float) -> float:
        """Back ease out - slight overshoot"""
        s = 1.70158
        t -= 1
        return t * t * ((s + 1) * t + s) + 1

    @staticmethod
    def ease_in_out_back(t: float) -> float:
        """Back ease in/out"""
        s = 1.70158 * 1.525
        t *= 2
        if t < 1:
            return 0.5 * (t * t * ((s + 1) * t - s))
        t -= 2
        return 0.5 * (t * t * ((s + 1) * t + s) + 2)

    # ═══════════════════════ BOUNCE ═══════════════════════

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Bounce ease out - like a bouncing ball"""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375

    @staticmethod
    def ease_in_bounce(t: float) -> float:
        """Bounce ease in"""
        return 1 - Easing.ease_out_bounce(1 - t)

    @staticmethod
    def ease_in_out_bounce(t: float) -> float:
        """Bounce ease in/out"""
        if t < 0.5:
            return Easing.ease_in_bounce(t * 2) * 0.5
        return Easing.ease_out_bounce(t * 2 - 1) * 0.5 + 0.5

    # ═══════════════════════ SPECIAL ═══════════════════════

    @staticmethod
    def smooth_step(t: float) -> float:
        """Smooth step - very smooth S-curve"""
        return t * t * (3 - 2 * t)

    @staticmethod
    def smoother_step(t: float) -> float:
        """Smoother step - even smoother S-curve"""
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def dramatic_pause(t: float, pause_at: float = 0.5, pause_duration: float = 0.2) -> float:
        """Creates a dramatic pause in the middle of animation"""
        if t < pause_at - pause_duration / 2:
            return Easing.ease_out_cubic(t / (pause_at - pause_duration / 2)) * 0.5
        elif t > pause_at + pause_duration / 2:
            remaining = (t - pause_at - pause_duration / 2) / (1 - pause_at - pause_duration / 2)
            return 0.5 + Easing.ease_in_cubic(remaining) * 0.5
        return 0.5

    @staticmethod
    def heartbeat(t: float) -> float:
        """Heartbeat pulse effect"""
        if t < 0.25:
            return Easing.ease_out_cubic(t * 4)
        elif t < 0.35:
            return 1 - Easing.ease_in_cubic((t - 0.25) * 10) * 0.3
        elif t < 0.5:
            return 0.7 + Easing.ease_out_cubic((t - 0.35) / 0.15) * 0.3
        else:
            return 1 - Easing.ease_in_cubic((t - 0.5) * 2)


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between two values"""
    return start + (end - start) * t


def lerp_color(color1: str, color2: str, t: float) -> str:
    """Interpolate between two hex colors"""
    c1 = tuple(int(color1.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    c2 = tuple(int(color2.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    r = lerp(c1[0], c2[0], t)
    g = lerp(c1[1], c2[1], t)
    b = lerp(c1[2], c2[2], t)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         ADVANCED PARTICLE SYSTEM                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class ParticleType(Enum):
    """Types of particles with different behaviors"""
    GENERIC = auto()
    FIRE = auto()
    SMOKE = auto()
    WATER = auto()
    SPARK = auto()
    MAGIC = auto()
    SNOW = auto()
    RAIN = auto()
    LEAF = auto()
    BUBBLE = auto()
    STAR = auto()
    EXPLOSION = auto()
    HEAL = auto()
    DARK = auto()


@dataclass
class Particle:
    """Individual particle with physics and rendering properties"""
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    ax: float = 0.0  # Acceleration
    ay: float = -0.1  # Gravity
    lifetime: float = 60
    max_lifetime: float = 60
    size: float = 10
    size_decay: float = 0.98
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)
    color_end: Tuple[float, float, float, float] = None
    particle_type: ParticleType = ParticleType.GENERIC
    rotation: float = 0
    rotation_speed: float = 0
    active: bool = True
    trail: List[Tuple[float, float]] = field(default_factory=list)
    trail_length: int = 0


class AdvancedParticleSystem:
    """
    Sophisticated particle system supporting multiple particle types,
    physics simulation, color interpolation, and special effects.
    """

    def __init__(self, max_particles: int = 2000):
        self.max_particles = max_particles
        self.particles: List[Particle] = []
        self.emitters: List[Dict] = []

    def emit(self, x: float, y: float,
             particle_type: ParticleType = ParticleType.GENERIC,
             count: int = 10,
             spread: float = 50,
             speed: float = 2,
             speed_variance: float = 0.5,
             direction: float = None,  # None = radial, else angle in radians
             direction_variance: float = np.pi,
             lifetime: float = 60,
             lifetime_variance: float = 10,
             size: float = 20,
             size_variance: float = 5,
             color: Tuple[float, float, float, float] = (1, 1, 1, 1),
             color_end: Tuple[float, float, float, float] = None,
             gravity: float = -0.1,
             size_decay: float = 0.98,
             trail_length: int = 0):
        """Emit particles with extensive customization"""

        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                # Remove oldest inactive or create new slot
                for i, p in enumerate(self.particles):
                    if not p.active:
                        self.particles.pop(i)
                        break
                else:
                    self.particles.pop(0)

            # Position with spread
            if spread > 0:
                angle = np.random.uniform(0, 2 * np.pi)
                r = np.random.uniform(0, spread)
                px = x + r * np.cos(angle)
                py = y + r * np.sin(angle)
            else:
                px, py = x, y

            # Velocity
            actual_speed = speed + np.random.uniform(-speed_variance, speed_variance) * speed
            if direction is None:
                # Radial
                vel_angle = np.random.uniform(0, 2 * np.pi)
            else:
                vel_angle = direction + np.random.uniform(-direction_variance, direction_variance)

            vx = actual_speed * np.cos(vel_angle)
            vy = actual_speed * np.sin(vel_angle)

            # Lifetime
            actual_lifetime = lifetime + np.random.uniform(-lifetime_variance, lifetime_variance)
            actual_lifetime = max(1, actual_lifetime)

            # Size
            actual_size = size + np.random.uniform(-size_variance, size_variance)
            actual_size = max(1, actual_size)

            particle = Particle(
                x=px, y=py,
                vx=vx, vy=vy,
                ay=gravity,
                lifetime=actual_lifetime,
                max_lifetime=actual_lifetime,
                size=actual_size,
                size_decay=size_decay,
                color=color,
                color_end=color_end,
                particle_type=particle_type,
                rotation=np.random.uniform(0, 2 * np.pi),
                rotation_speed=np.random.uniform(-0.1, 0.1),
                trail_length=trail_length
            )
            self.particles.append(particle)

    def emit_fire(self, x: float, y: float, intensity: float = 1.0):
        """Emit realistic fire particles"""
        self.emit(x, y,
                  particle_type=ParticleType.FIRE,
                  count=int(5 * intensity),
                  spread=20 * intensity,
                  speed=3,
                  direction=np.pi/2,  # Upward
                  direction_variance=0.3,
                  lifetime=40,
                  size=30 * intensity,
                  color=(1, 0.6, 0, 0.9),
                  color_end=(1, 0, 0, 0),
                  gravity=0.05,  # Fire rises
                  size_decay=0.95)
        # Add smoke
        self.emit(x, y + 30,
                  particle_type=ParticleType.SMOKE,
                  count=int(2 * intensity),
                  spread=15,
                  speed=1,
                  direction=np.pi/2,
                  direction_variance=0.2,
                  lifetime=80,
                  size=40 * intensity,
                  color=(0.3, 0.3, 0.3, 0.5),
                  color_end=(0.5, 0.5, 0.5, 0),
                  gravity=0.02,
                  size_decay=1.02)  # Smoke expands

    def emit_magic(self, x: float, y: float, color: str = 'green', intensity: float = 1.0):
        """Emit magical sparkle particles"""
        colors = {
            'green': ((0, 1, 0.5, 1), (0, 1, 0.5, 0)),
            'blue': ((0, 0.7, 1, 1), (0, 0.5, 1, 0)),
            'purple': ((0.6, 0, 1, 1), (0.8, 0, 1, 0)),
            'gold': ((1, 0.84, 0, 1), (1, 0.6, 0, 0)),
            'white': ((1, 1, 1, 1), (1, 1, 1, 0)),
            'dark': ((0.3, 0, 0.5, 1), (0, 0, 0, 0)),
        }
        c_start, c_end = colors.get(color, colors['green'])

        self.emit(x, y,
                  particle_type=ParticleType.MAGIC,
                  count=int(8 * intensity),
                  spread=30 * intensity,
                  speed=2,
                  lifetime=50,
                  size=15 * intensity,
                  color=c_start,
                  color_end=c_end,
                  gravity=-0.02,  # Magic floats up slightly
                  size_decay=0.96,
                  trail_length=5)

    def emit_explosion(self, x: float, y: float, intensity: float = 1.0, color: str = 'fire'):
        """Emit dramatic explosion"""
        colors = {
            'fire': ((1, 0.5, 0, 1), (1, 0, 0, 0)),
            'magic': ((0.5, 1, 0.5, 1), (0, 1, 0, 0)),
            'dark': ((0.5, 0, 0.5, 1), (0, 0, 0, 0)),
            'ice': ((0.7, 0.9, 1, 1), (0.5, 0.7, 1, 0)),
        }
        c_start, c_end = colors.get(color, colors['fire'])

        # Core explosion
        self.emit(x, y,
                  particle_type=ParticleType.EXPLOSION,
                  count=int(50 * intensity),
                  spread=10,
                  speed=8 * intensity,
                  lifetime=40,
                  size=40 * intensity,
                  color=c_start,
                  color_end=c_end,
                  gravity=-0.05,
                  size_decay=0.92,
                  trail_length=3)

        # Sparks
        self.emit(x, y,
                  particle_type=ParticleType.SPARK,
                  count=int(30 * intensity),
                  spread=5,
                  speed=12 * intensity,
                  lifetime=60,
                  size=8,
                  color=(1, 1, 0.5, 1),
                  color_end=(1, 0.5, 0, 0),
                  gravity=-0.15,
                  size_decay=0.98,
                  trail_length=8)

    def emit_water_splash(self, x: float, y: float, intensity: float = 1.0):
        """Emit water splash particles"""
        # Main droplets
        self.emit(x, y,
                  particle_type=ParticleType.WATER,
                  count=int(20 * intensity),
                  spread=20,
                  speed=5 * intensity,
                  direction=np.pi/2,
                  direction_variance=0.8,
                  lifetime=50,
                  size=12,
                  color=(0.5, 0.8, 1, 0.8),
                  color_end=(0.5, 0.8, 1, 0),
                  gravity=-0.2,
                  size_decay=0.97)

        # Mist
        self.emit(x, y,
                  particle_type=ParticleType.WATER,
                  count=int(10 * intensity),
                  spread=40,
                  speed=1,
                  lifetime=40,
                  size=30,
                  color=(0.8, 0.9, 1, 0.3),
                  color_end=(0.9, 0.95, 1, 0),
                  gravity=0.01,
                  size_decay=1.01)

    def emit_rain(self, width: float, height: float, intensity: float = 1.0):
        """Emit rain across the screen"""
        count = int(10 * intensity)
        for _ in range(count):
            x = np.random.uniform(0, width)
            self.emit(x, height + 50,
                      particle_type=ParticleType.RAIN,
                      count=1,
                      spread=0,
                      speed=15,
                      direction=-np.pi/2 - 0.1,  # Slightly angled
                      direction_variance=0.05,
                      lifetime=100,
                      size=3,
                      color=(0.7, 0.8, 0.9, 0.6),
                      color_end=(0.7, 0.8, 0.9, 0.3),
                      gravity=-0.1,
                      size_decay=1.0)

    def emit_snow(self, width: float, height: float, intensity: float = 1.0):
        """Emit snow across the screen"""
        count = int(5 * intensity)
        for _ in range(count):
            x = np.random.uniform(0, width)
            self.emit(x, height + 20,
                      particle_type=ParticleType.SNOW,
                      count=1,
                      spread=0,
                      speed=2,
                      direction=-np.pi/2,
                      direction_variance=0.3,
                      lifetime=200,
                      size=8,
                      color=(1, 1, 1, 0.9),
                      color_end=(1, 1, 1, 0.5),
                      gravity=-0.02,
                      size_decay=1.0)

    def emit_healing(self, x: float, y: float, intensity: float = 1.0):
        """Emit healing sparkles rising upward"""
        self.emit(x, y,
                  particle_type=ParticleType.HEAL,
                  count=int(15 * intensity),
                  spread=40,
                  speed=2,
                  direction=np.pi/2,
                  direction_variance=0.5,
                  lifetime=60,
                  size=12,
                  color=(0.5, 1, 0.5, 1),
                  color_end=(0.8, 1, 0.8, 0),
                  gravity=0.03,
                  size_decay=0.97)

    def emit_dark_energy(self, x: float, y: float, intensity: float = 1.0):
        """Emit dark, evil energy"""
        self.emit(x, y,
                  particle_type=ParticleType.DARK,
                  count=int(12 * intensity),
                  spread=50,
                  speed=1.5,
                  lifetime=70,
                  size=25,
                  color=(0.2, 0, 0.3, 0.8),
                  color_end=(0, 0, 0, 0),
                  gravity=0.01,
                  size_decay=0.99,
                  trail_length=4)

    def update(self):
        """Update all particles physics and state"""
        for p in self.particles:
            if not p.active:
                continue

            # Store trail position
            if p.trail_length > 0:
                p.trail.append((p.x, p.y))
                if len(p.trail) > p.trail_length:
                    p.trail.pop(0)

            # Physics update
            p.vx += p.ax
            p.vy += p.ay
            p.x += p.vx
            p.y += p.vy

            # Special behaviors by type
            if p.particle_type == ParticleType.SNOW:
                # Snow drifts side to side
                p.x += np.sin(p.lifetime * 0.1) * 0.5
            elif p.particle_type == ParticleType.FIRE:
                # Fire flickers
                p.x += np.random.uniform(-1, 1)
            elif p.particle_type == ParticleType.MAGIC:
                # Magic sparkles
                p.x += np.sin(p.lifetime * 0.2) * 0.3
                p.y += np.cos(p.lifetime * 0.15) * 0.3

            # Rotation
            p.rotation += p.rotation_speed

            # Size decay
            p.size *= p.size_decay

            # Lifetime
            p.lifetime -= 1
            if p.lifetime <= 0 or p.size < 0.5:
                p.active = False

        # Remove dead particles periodically
        if len(self.particles) > self.max_particles * 0.9:
            self.particles = [p for p in self.particles if p.active]

    def render(self, ax):
        """Render all active particles"""
        if not self.particles:
            return

        active_particles = [p for p in self.particles if p.active]
        if not active_particles:
            return

        # Group by similar rendering for efficiency
        positions = []
        colors = []
        sizes = []

        for p in active_particles:
            # Calculate interpolated color
            life_ratio = p.lifetime / p.max_lifetime
            if p.color_end:
                r = lerp(p.color_end[0], p.color[0], life_ratio)
                g = lerp(p.color_end[1], p.color[1], life_ratio)
                b = lerp(p.color_end[2], p.color[2], life_ratio)
                a = lerp(p.color_end[3], p.color[3], life_ratio)
            else:
                r, g, b, a = p.color
                a *= life_ratio  # Fade out

            positions.append([p.x, p.y])
            colors.append([r, g, b, clamp(a, 0, 1)])
            sizes.append(clamp(p.size, 0.1, 200))

            # Render trails
            if p.trail_length > 0 and len(p.trail) > 1:
                trail_x = [pos[0] for pos in p.trail]
                trail_y = [pos[1] for pos in p.trail]
                trail_alpha = np.linspace(0, a * 0.5, len(p.trail))
                for i in range(len(p.trail) - 1):
                    ax.plot([trail_x[i], trail_x[i+1]],
                           [trail_y[i], trail_y[i+1]],
                           color=(r, g, b, trail_alpha[i]),
                           linewidth=p.size * 0.3,
                           zorder=98)

        if positions:
            positions = np.array(positions)
            colors = np.array(colors)
            sizes = np.array(sizes)
            ax.scatter(positions[:, 0], positions[:, 1],
                      c=colors, s=sizes, zorder=99, marker='o')


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                          CAMERA SYSTEM                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class Camera:
    """
    Advanced camera system with shake, zoom, pan, and parallax effects.
    """

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.x = 0  # Camera position
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.rotation = 0
        self.target_rotation = 0

        # Shake parameters
        self.shake_intensity = 0
        self.shake_decay = 0.9
        self.shake_offset_x = 0
        self.shake_offset_y = 0

        # Smooth follow
        self.follow_speed = 0.1
        self.zoom_speed = 0.05

        # Cinematic bars
        self.letterbox = 0  # 0 = none, 1 = full cinematic bars
        self.target_letterbox = 0

    def shake(self, intensity: float, decay: float = 0.9):
        """Apply screen shake effect"""
        self.shake_intensity = intensity
        self.shake_decay = decay

    def set_position(self, x: float, y: float, immediate: bool = False):
        """Set camera target position"""
        self.target_x = x
        self.target_y = y
        if immediate:
            self.x = x
            self.y = y

    def set_zoom(self, zoom: float, immediate: bool = False):
        """Set camera zoom level"""
        self.target_zoom = clamp(zoom, 0.5, 3.0)
        if immediate:
            self.zoom = self.target_zoom

    def set_letterbox(self, amount: float, immediate: bool = False):
        """Set cinematic letterbox bars"""
        self.target_letterbox = clamp(amount, 0, 1)
        if immediate:
            self.letterbox = self.target_letterbox

    def follow(self, target_x: float, target_y: float, speed: float = None):
        """Smoothly follow a target"""
        if speed:
            self.follow_speed = speed
        self.target_x = target_x - self.width / 2
        self.target_y = target_y - self.height / 2

    def update(self):
        """Update camera state"""
        # Smooth position
        self.x = lerp(self.x, self.target_x, self.follow_speed)
        self.y = lerp(self.y, self.target_y, self.follow_speed)

        # Smooth zoom
        self.zoom = lerp(self.zoom, self.target_zoom, self.zoom_speed)

        # Smooth letterbox
        self.letterbox = lerp(self.letterbox, self.target_letterbox, 0.05)

        # Update shake
        if self.shake_intensity > 0.1:
            self.shake_offset_x = np.random.uniform(-1, 1) * self.shake_intensity
            self.shake_offset_y = np.random.uniform(-1, 1) * self.shake_intensity
            self.shake_intensity *= self.shake_decay
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
            self.shake_intensity = 0

    def get_view_bounds(self) -> Tuple[float, float, float, float]:
        """Get the current view bounds (x_min, x_max, y_min, y_max)"""
        # Calculate zoomed dimensions
        view_width = self.width / self.zoom
        view_height = self.height / self.zoom

        # Center offset
        center_x = self.x + self.width / 2 + self.shake_offset_x
        center_y = self.y + self.height / 2 + self.shake_offset_y

        x_min = center_x - view_width / 2
        x_max = center_x + view_width / 2
        y_min = center_y - view_height / 2
        y_max = center_y + view_height / 2

        return x_min, x_max, y_min, y_max

    def apply_to_axes(self, ax):
        """Apply camera transform to matplotlib axes"""
        x_min, x_max, y_min, y_max = self.get_view_bounds()
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    def render_letterbox(self, ax):
        """Render cinematic letterbox bars"""
        if self.letterbox > 0.01:
            bar_height = self.height * 0.1 * self.letterbox
            x_min, x_max, y_min, y_max = self.get_view_bounds()

            # Top bar
            top_bar = patches.Rectangle(
                (x_min, y_max - bar_height * (y_max - y_min) / self.height),
                x_max - x_min, bar_height * (y_max - y_min) / self.height * 2,
                color='black', zorder=1000
            )
            ax.add_patch(top_bar)

            # Bottom bar
            bottom_bar = patches.Rectangle(
                (x_min, y_min - bar_height * (y_max - y_min) / self.height),
                x_max - x_min, bar_height * (y_max - y_min) / self.height * 2,
                color='black', zorder=1000
            )
            ax.add_patch(bottom_bar)

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        return world_x, world_y  # With proper axes limits, this is identity

    def get_parallax_offset(self, depth: float) -> Tuple[float, float]:
        """Get parallax offset for a given depth layer (0=foreground, 1=background)"""
        parallax_factor = 1 - depth * 0.5
        offset_x = self.x * (1 - parallax_factor)
        offset_y = self.y * (1 - parallax_factor)
        return offset_x, offset_y


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         WEATHER SYSTEM                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class WeatherType(Enum):
    CLEAR = auto()
    CLOUDY = auto()
    RAIN = auto()
    STORM = auto()
    SNOW = auto()
    FOG = auto()
    MAGICAL = auto()


class WeatherSystem:
    """Dynamic weather system with transitions"""

    def __init__(self, particles: AdvancedParticleSystem):
        self.particles = particles
        self.current_weather = WeatherType.CLEAR
        self.target_weather = WeatherType.CLEAR
        self.intensity = 0
        self.target_intensity = 0
        self.transition_speed = 0.02

        # Storm specifics
        self.lightning_timer = 0
        self.lightning_flash = 0
        self.thunder_delay = 0

        # Wind
        self.wind_strength = 0
        self.wind_direction = 0  # radians

        # Clouds
        self.clouds: List[Dict] = []
        self._generate_clouds()

    def _generate_clouds(self):
        """Generate cloud positions"""
        self.clouds = []
        for _ in range(15):
            self.clouds.append({
                'x': np.random.uniform(-200, WIDTH + 200),
                'y': np.random.uniform(HEIGHT * 0.6, HEIGHT * 0.95),
                'size': np.random.uniform(100, 300),
                'speed': np.random.uniform(0.2, 1.0),
                'opacity': np.random.uniform(0.3, 0.8),
            })

    def set_weather(self, weather: WeatherType, intensity: float = 1.0, immediate: bool = False):
        """Set target weather"""
        self.target_weather = weather
        self.target_intensity = clamp(intensity, 0, 1)
        if immediate:
            self.current_weather = weather
            self.intensity = intensity

    def update(self, frame: int):
        """Update weather state"""
        # Transition intensity
        self.intensity = lerp(self.intensity, self.target_intensity, self.transition_speed)

        # Weather-specific updates
        if self.current_weather == WeatherType.RAIN or self.target_weather == WeatherType.RAIN:
            if self.intensity > 0.1:
                self.particles.emit_rain(WIDTH, HEIGHT, self.intensity)

        if self.current_weather == WeatherType.SNOW or self.target_weather == WeatherType.SNOW:
            if self.intensity > 0.1:
                self.particles.emit_snow(WIDTH, HEIGHT, self.intensity)

        if self.current_weather == WeatherType.STORM or self.target_weather == WeatherType.STORM:
            if self.intensity > 0.1:
                self.particles.emit_rain(WIDTH, HEIGHT, self.intensity * 2)

                # Lightning
                self.lightning_timer -= 1
                if self.lightning_timer <= 0 and np.random.random() < 0.02 * self.intensity:
                    self.lightning_flash = 10
                    self.thunder_delay = np.random.randint(20, 60)
                    self.lightning_timer = np.random.randint(60, 180)

        # Update lightning flash
        if self.lightning_flash > 0:
            self.lightning_flash -= 1

        # Update clouds
        for cloud in self.clouds:
            cloud['x'] += cloud['speed'] + self.wind_strength
            if cloud['x'] > WIDTH + 300:
                cloud['x'] = -300
            elif cloud['x'] < -300:
                cloud['x'] = WIDTH + 300

        # Weather transition
        if self.intensity < 0.1 and self.target_weather != self.current_weather:
            self.current_weather = self.target_weather

    def render_sky_overlay(self, ax, base_color: str) -> str:
        """Get modified sky color based on weather"""
        if self.current_weather == WeatherType.STORM:
            return lerp_color(base_color, Palette.SKY_STORM, self.intensity * 0.7)
        elif self.current_weather == WeatherType.CLOUDY:
            return lerp_color(base_color, '#9CA3AF', self.intensity * 0.4)
        elif self.current_weather == WeatherType.FOG:
            return lerp_color(base_color, Palette.FOG, self.intensity * 0.5)
        return base_color

    def render(self, ax):
        """Render weather effects"""
        # Lightning flash
        if self.lightning_flash > 0:
            flash_alpha = self.lightning_flash / 10 * 0.8
            flash = patches.Rectangle((0, 0), WIDTH, HEIGHT,
                                       color='white', alpha=flash_alpha, zorder=500)
            ax.add_patch(flash)

            # Lightning bolt
            if self.lightning_flash > 7:
                bolt_x = np.random.uniform(WIDTH * 0.2, WIDTH * 0.8)
                self._draw_lightning(ax, bolt_x, HEIGHT, bolt_x + np.random.uniform(-100, 100), HEIGHT * 0.3)

        # Clouds
        cloud_opacity_mult = 1.0
        if self.current_weather in [WeatherType.RAIN, WeatherType.STORM]:
            cloud_opacity_mult = 1.5
        elif self.current_weather == WeatherType.CLEAR:
            cloud_opacity_mult = 0.3

        for cloud in self.clouds:
            self._draw_cloud(ax, cloud['x'], cloud['y'], cloud['size'],
                           cloud['opacity'] * cloud_opacity_mult * self.intensity if self.current_weather != WeatherType.CLEAR else cloud['opacity'] * 0.3)

        # Fog overlay
        if self.current_weather == WeatherType.FOG and self.intensity > 0.1:
            fog = patches.Rectangle((0, 0), WIDTH, HEIGHT,
                                    color=Palette.FOG, alpha=self.intensity * 0.4, zorder=200)
            ax.add_patch(fog)

    def _draw_cloud(self, ax, x: float, y: float, size: float, opacity: float):
        """Draw a fluffy cloud"""
        opacity = clamp(opacity, 0, 0.9)
        # Cloud is made of overlapping circles
        offsets = [
            (0, 0, 1.0),
            (-0.3, 0.1, 0.7),
            (0.3, 0.1, 0.7),
            (-0.15, 0.2, 0.5),
            (0.15, 0.2, 0.5),
        ]
        for ox, oy, scale in offsets:
            circle = patches.Circle(
                (x + ox * size, y + oy * size),
                size * 0.4 * scale,
                color='white', alpha=opacity, zorder=50
            )
            ax.add_patch(circle)

    def _draw_lightning(self, ax, x1: float, y1: float, x2: float, y2: float, branches: int = 3):
        """Draw a lightning bolt"""
        points = [(x1, y1)]
        segments = 8
        for i in range(1, segments):
            t = i / segments
            x = lerp(x1, x2, t) + np.random.uniform(-50, 50)
            y = lerp(y1, y2, t)
            points.append((x, y))
        points.append((x2, y2))

        # Draw main bolt
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.plot(xs, ys, color=Palette.LIGHTNING, linewidth=4, zorder=501, alpha=0.9)
        ax.plot(xs, ys, color='white', linewidth=2, zorder=502, alpha=1.0)

        # Draw branches
        for _ in range(branches):
            branch_start = np.random.randint(1, len(points) - 2)
            bx1, by1 = points[branch_start]
            bx2 = bx1 + np.random.uniform(-100, 100)
            by2 = by1 - np.random.uniform(50, 150)
            branch_points = [(bx1, by1)]
            for i in range(1, 4):
                t = i / 4
                bx = lerp(bx1, bx2, t) + np.random.uniform(-20, 20)
                by = lerp(by1, by2, t)
                branch_points.append((bx, by))
            bxs = [p[0] for p in branch_points]
            bys = [p[1] for p in branch_points]
            ax.plot(bxs, bys, color=Palette.LIGHTNING, linewidth=2, zorder=501, alpha=0.7)


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         LIGHTING SYSTEM                                       ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class TimeOfDay(Enum):
    DAWN = auto()
    MORNING = auto()
    NOON = auto()
    AFTERNOON = auto()
    SUNSET = auto()
    DUSK = auto()
    NIGHT = auto()
    MIDNIGHT = auto()


class LightingSystem:
    """Dynamic lighting and time of day system"""

    TIME_COLORS = {
        TimeOfDay.DAWN: {'sky': '#FFB6C1', 'ambient': (1.0, 0.9, 0.9), 'sun_pos': 0.1},
        TimeOfDay.MORNING: {'sky': '#87CEEB', 'ambient': (1.0, 1.0, 0.95), 'sun_pos': 0.3},
        TimeOfDay.NOON: {'sky': '#87CEEB', 'ambient': (1.0, 1.0, 1.0), 'sun_pos': 0.5},
        TimeOfDay.AFTERNOON: {'sky': '#87CEEB', 'ambient': (1.0, 0.98, 0.95), 'sun_pos': 0.7},
        TimeOfDay.SUNSET: {'sky': '#FF6B4A', 'ambient': (1.0, 0.8, 0.7), 'sun_pos': 0.9},
        TimeOfDay.DUSK: {'sky': '#4A3B6B', 'ambient': (0.7, 0.6, 0.8), 'sun_pos': 0.95},
        TimeOfDay.NIGHT: {'sky': '#0D1B2A', 'ambient': (0.3, 0.3, 0.5), 'sun_pos': 0},
        TimeOfDay.MIDNIGHT: {'sky': '#0A0A0F', 'ambient': (0.2, 0.2, 0.3), 'sun_pos': 0},
    }

    def __init__(self):
        self.current_time = TimeOfDay.NOON
        self.target_time = TimeOfDay.NOON
        self.transition_progress = 1.0
        self.transition_speed = 0.01

        # Point lights
        self.point_lights: List[Dict] = []

        # Global modifiers
        self.brightness = 1.0
        self.contrast = 1.0

        # Stars (for night)
        self.stars = [(np.random.uniform(0, WIDTH),
                       np.random.uniform(HEIGHT * 0.4, HEIGHT),
                       np.random.uniform(0.3, 1.0),
                       np.random.uniform(0, 2*np.pi)) for _ in range(200)]

    def set_time(self, time: TimeOfDay, immediate: bool = False):
        """Set target time of day"""
        if time != self.current_time:
            self.target_time = time
            if immediate:
                self.current_time = time
                self.transition_progress = 1.0
            else:
                self.transition_progress = 0.0

    def add_point_light(self, x: float, y: float, radius: float,
                        color: Tuple[float, float, float] = (1, 0.9, 0.7),
                        intensity: float = 1.0) -> int:
        """Add a point light source"""
        light = {
            'x': x, 'y': y,
            'radius': radius,
            'color': color,
            'intensity': intensity,
            'flicker': 0,
        }
        self.point_lights.append(light)
        return len(self.point_lights) - 1

    def update_point_light(self, index: int, x: float = None, y: float = None,
                          intensity: float = None):
        """Update a point light"""
        if 0 <= index < len(self.point_lights):
            if x is not None:
                self.point_lights[index]['x'] = x
            if y is not None:
                self.point_lights[index]['y'] = y
            if intensity is not None:
                self.point_lights[index]['intensity'] = intensity

    def remove_point_light(self, index: int):
        """Remove a point light"""
        if 0 <= index < len(self.point_lights):
            self.point_lights.pop(index)

    def clear_point_lights(self):
        """Remove all point lights"""
        self.point_lights = []

    def update(self, frame: int):
        """Update lighting state"""
        # Transition between times
        if self.transition_progress < 1.0:
            self.transition_progress = min(1.0, self.transition_progress + self.transition_speed)
            if self.transition_progress >= 1.0:
                self.current_time = self.target_time

        # Update point light flicker
        for light in self.point_lights:
            light['flicker'] = 0.9 + np.random.uniform(-0.1, 0.1)

    def get_sky_color(self) -> str:
        """Get current sky color"""
        if self.transition_progress >= 1.0:
            return self.TIME_COLORS[self.current_time]['sky']

        current_sky = self.TIME_COLORS[self.current_time]['sky']
        target_sky = self.TIME_COLORS[self.target_time]['sky']
        return lerp_color(current_sky, target_sky,
                         Easing.ease_in_out_cubic(self.transition_progress))

    def get_ambient(self) -> Tuple[float, float, float]:
        """Get current ambient light color"""
        if self.transition_progress >= 1.0:
            return self.TIME_COLORS[self.current_time]['ambient']

        current = self.TIME_COLORS[self.current_time]['ambient']
        target = self.TIME_COLORS[self.target_time]['ambient']
        t = Easing.ease_in_out_cubic(self.transition_progress)
        return (
            lerp(current[0], target[0], t),
            lerp(current[1], target[1], t),
            lerp(current[2], target[2], t)
        )

    def render_celestial(self, ax, frame: int):
        """Render sun, moon, and stars"""
        time_data = self.TIME_COLORS[self.current_time]
        sun_pos = time_data['sun_pos']

        if self.current_time in [TimeOfDay.NIGHT, TimeOfDay.MIDNIGHT]:
            # Render stars
            for sx, sy, brightness, phase in self.stars:
                twinkle = 0.5 + 0.5 * np.sin(frame * 0.05 + phase)
                alpha = brightness * twinkle
                ax.scatter([sx], [sy], c='white', s=brightness * 20,
                          alpha=clamp(alpha, 0.1, 1.0), zorder=5)

            # Render moon
            moon_x = WIDTH * 0.8
            moon_y = HEIGHT * 0.85
            # Moon glow
            for i in range(3):
                glow = patches.Circle((moon_x, moon_y), 60 + i * 20,
                                      color=Palette.MOON_GLOW,
                                      alpha=0.1 - i * 0.03, zorder=6)
                ax.add_patch(glow)
            # Moon body
            moon = patches.Circle((moon_x, moon_y), 50,
                                 color=Palette.MOON, zorder=7)
            ax.add_patch(moon)
            # Moon craters
            crater_positions = [(moon_x - 15, moon_y + 10),
                               (moon_x + 20, moon_y - 5),
                               (moon_x + 5, moon_y + 20)]
            for cx, cy in crater_positions:
                crater = patches.Circle((cx, cy), 8,
                                        color='#E5E5D0', zorder=8)
                ax.add_patch(crater)

        elif sun_pos > 0:
            # Render sun
            sun_x = WIDTH * sun_pos
            sun_y = HEIGHT * (0.5 + 0.4 * np.sin(sun_pos * np.pi))

            # Sun glow
            for i in range(5):
                glow = patches.Circle((sun_x, sun_y), 80 + i * 30,
                                      color=Palette.SUN_GLOW,
                                      alpha=0.15 - i * 0.025, zorder=3)
                ax.add_patch(glow)

            # Sun rays
            num_rays = 12
            for i in range(num_rays):
                angle = (i / num_rays) * 2 * np.pi + frame * 0.005
                ray_length = 100 + 20 * np.sin(frame * 0.03 + i)
                ray_x = sun_x + np.cos(angle) * ray_length
                ray_y = sun_y + np.sin(angle) * ray_length
                ax.plot([sun_x, ray_x], [sun_y, ray_y],
                       color=Palette.SUN, linewidth=3, alpha=0.4, zorder=4)

            # Sun body
            sun = patches.Circle((sun_x, sun_y), 60,
                                color=Palette.SUN, zorder=5)
            ax.add_patch(sun)

    def render_point_lights(self, ax):
        """Render point light effects"""
        for light in self.point_lights:
            intensity = light['intensity'] * light['flicker']
            r, g, b = light['color']

            # Render light glow
            for i in range(5):
                radius = light['radius'] * (1 + i * 0.4)
                alpha = intensity * (0.2 - i * 0.035)
                glow = patches.Circle(
                    (light['x'], light['y']), radius,
                    color=(r, g, b), alpha=clamp(alpha, 0, 0.3), zorder=150
                )
                ax.add_patch(glow)

    def apply_ambient_to_color(self, color: str) -> str:
        """Apply ambient lighting to a color"""
        ambient = self.get_ambient()

        # Parse hex color
        r = int(color.lstrip('#')[0:2], 16) / 255
        g = int(color.lstrip('#')[2:4], 16) / 255
        b = int(color.lstrip('#')[4:6], 16) / 255

        # Apply ambient
        r = clamp(r * ambient[0] * self.brightness, 0, 1)
        g = clamp(g * ambient[1] * self.brightness, 0, 1)
        b = clamp(b * ambient[2] * self.brightness, 0, 1)

        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         CHARACTER SYSTEM                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class Emotion(Enum):
    NEUTRAL = auto()
    HAPPY = auto()
    SAD = auto()
    ANGRY = auto()
    SCARED = auto()
    DETERMINED = auto()
    LOVE = auto()
    SHOCKED = auto()
    SLEEPING = auto()
    HURT = auto()
    POWERFUL = auto()
    EVIL = auto()


class Character:
    """Base class for all animated characters"""

    def __init__(self, x: float, y: float, scale: float = 1.0, name: str = ""):
        self.x = x
        self.y = y
        self.scale = scale
        self.name = name
        self.emotion = Emotion.NEUTRAL
        self.facing = 1  # 1 = right, -1 = left
        self.alpha = 1.0

        # Animation state
        self.anim_frame = 0
        self.blink_timer = np.random.randint(0, 120)
        self.breath_phase = np.random.uniform(0, 2 * np.pi)

        # Movement
        self.target_x = x
        self.target_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_velocity = 0
        self.is_jumping = False
        self.ground_y = y

        # Speech
        self.speech_text = ""
        self.speech_timer = 0

    def move_to(self, x: float, y: float, speed: float = 0.1):
        """Set movement target"""
        self.target_x = x
        self.target_y = y
        if x < self.x:
            self.facing = -1
        elif x > self.x:
            self.facing = 1

    def jump(self, power: float = 15):
        """Make character jump"""
        if not self.is_jumping:
            self.jump_velocity = power
            self.is_jumping = True
            self.ground_y = self.y

    def say(self, text: str, duration: int = 180):
        """Make character speak"""
        self.speech_text = text
        self.speech_timer = duration

    def update(self, frame: int):
        """Update character state"""
        self.anim_frame = frame

        # Blinking
        self.blink_timer -= 1
        if self.blink_timer <= 0:
            self.blink_timer = np.random.randint(100, 200)

        # Movement interpolation
        self.x = lerp(self.x, self.target_x, 0.08)
        self.y = lerp(self.y, self.target_y, 0.08)

        # Jump physics
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity -= 0.8
            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0

        # Speech timer
        if self.speech_timer > 0:
            self.speech_timer -= 1

    def render(self, ax, frame: int):
        """Override in subclasses"""
        raise NotImplementedError

    def render_speech(self, ax):
        """Render speech bubble"""
        if self.speech_timer > 0 and self.speech_text:
            bubble_x = self.x + 60 * self.scale
            bubble_y = self.y + 80 * self.scale

            # Bubble background
            bubble = patches.FancyBboxPatch(
                (bubble_x - 60, bubble_y - 20), 120, 40,
                boxstyle="round,pad=0.05,rounding_size=10",
                facecolor='white', edgecolor='black',
                linewidth=2, zorder=200
            )
            ax.add_patch(bubble)

            # Bubble pointer
            pointer = patches.Polygon([
                [bubble_x - 20, bubble_y - 20],
                [self.x + 20 * self.scale, self.y + 50 * self.scale],
                [bubble_x, bubble_y - 20]
            ], color='white', zorder=199)
            ax.add_patch(pointer)

            # Text
            alpha = min(1, self.speech_timer / 30) if self.speech_timer < 30 else 1
            ax.text(bubble_x, bubble_y, self.speech_text,
                   ha='center', va='center', fontsize=10,
                   color='black', alpha=alpha, zorder=201)


class Frog(Character):
    """Eli the Frog - Our Hero"""

    def __init__(self, x: float, y: float, scale: float = 1.0,
                 color: str = 'green', name: str = "Eli"):
        super().__init__(x, y, scale, name)

        # Color variants
        self.colors = {
            'green': (Palette.FROG_BODY, Palette.FROG_BELLY, Palette.FROG_DARK),
            'golden': ('#FFD700', '#FFEC8B', '#DAA520'),
            'blue': ('#4169E1', '#87CEEB', '#0000CD'),
            'red': ('#DC143C', '#FA8072', '#8B0000'),
            'dark': ('#2F4F4F', '#696969', '#1C1C1C'),
            'princess': ('#FF69B4', '#FFB6C1', '#DB7093'),
        }
        self.body_color, self.belly_color, self.dark_color = self.colors.get(
            color, self.colors['green'])

        # Special states
        self.is_glowing = False
        self.glow_color = Palette.MAGIC_GREEN
        self.glow_intensity = 0
        self.power_level = 0  # For transformation effects
        self.has_crown = False
        self.mouth_open = 0

    def set_glow(self, enabled: bool, color: str = None, intensity: float = 1.0):
        """Enable/disable magical glow"""
        self.is_glowing = enabled
        self.glow_intensity = intensity if enabled else 0
        if color:
            self.glow_color = color

    def render(self, ax, frame: int):
        """Render the frog with all details"""
        if self.alpha <= 0:
            return

        s = self.scale * 50
        x, y = self.x, self.y

        # Breathing animation
        breath = np.sin(frame * 0.05 + self.breath_phase) * 2

        # Glow effect
        if self.is_glowing and self.glow_intensity > 0:
            for i in range(3):
                glow_size = s * (2.5 + i * 0.5)
                glow = patches.Circle(
                    (x, y), glow_size,
                    color=self.glow_color,
                    alpha=self.glow_intensity * (0.15 - i * 0.04) * self.alpha,
                    zorder=9
                )
                ax.add_patch(glow)

        # Shadow
        shadow = patches.Ellipse(
            (x, y - s * 0.8), s * 2.2, s * 0.4,
            color='black', alpha=0.2 * self.alpha, zorder=8
        )
        ax.add_patch(shadow)

        # Back legs
        for side in [-1, 1]:
            leg_angle = 20 + np.sin(frame * 0.1) * 5 if not self.is_jumping else 45
            leg = patches.Ellipse(
                (x + side * s * 0.7 * self.facing, y - s * 0.5),
                s * 0.6, s * 0.35,
                angle=side * leg_angle * self.facing,
                color=self.dark_color, alpha=self.alpha, zorder=10
            )
            ax.add_patch(leg)

        # Body
        body_height = s * 1.4 + breath
        body = patches.Ellipse(
            (x, y), s * 2, body_height,
            color=self.body_color, alpha=self.alpha, zorder=11
        )
        ax.add_patch(body)

        # Belly
        belly = patches.Ellipse(
            (x, y - s * 0.1), s * 1.3, s * 0.9,
            color=self.belly_color, alpha=self.alpha, zorder=12
        )
        ax.add_patch(belly)

        # Front legs
        for side in [-1, 1]:
            front_leg = patches.Ellipse(
                (x + side * s * 0.5 * self.facing, y - s * 0.4),
                s * 0.35, s * 0.25,
                angle=side * -15 * self.facing,
                color=self.dark_color, alpha=self.alpha, zorder=13
            )
            ax.add_patch(front_leg)

        # Eyes
        is_blinking = self.blink_timer < 5
        eye_y = y + s * 0.4

        for side in [-1, 1]:
            eye_x = x + side * s * 0.4 * self.facing

            # Eye bulge
            bulge = patches.Circle(
                (eye_x, eye_y + s * 0.15), s * 0.35,
                color=self.body_color, alpha=self.alpha, zorder=14
            )
            ax.add_patch(bulge)

            if not is_blinking and self.emotion != Emotion.SLEEPING:
                # Eye white
                eye_white = patches.Circle(
                    (eye_x, eye_y), s * 0.28,
                    color='white', alpha=self.alpha, zorder=15
                )
                ax.add_patch(eye_white)

                # Pupil - varies by emotion
                pupil_size = s * 0.14
                pupil_offset_x = 0
                pupil_offset_y = 0

                if self.emotion == Emotion.SCARED:
                    pupil_size = s * 0.08
                elif self.emotion == Emotion.ANGRY:
                    pupil_offset_y = s * 0.05
                elif self.emotion == Emotion.LOVE:
                    # Heart-shaped indication
                    pupil_size = s * 0.12
                elif self.emotion == Emotion.EVIL:
                    pupil_size = s * 0.06

                pupil = patches.Circle(
                    (eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_size,
                    color='black', alpha=self.alpha, zorder=16
                )
                ax.add_patch(pupil)

                # Eye highlight
                highlight = patches.Circle(
                    (eye_x + s * 0.08, eye_y + s * 0.08), s * 0.06,
                    color='white', alpha=self.alpha * 0.8, zorder=17
                )
                ax.add_patch(highlight)
            else:
                # Closed eye
                eye_line = patches.Rectangle(
                    (eye_x - s * 0.2, eye_y - s * 0.02),
                    s * 0.4, s * 0.04,
                    color=self.dark_color, alpha=self.alpha, zorder=15
                )
                ax.add_patch(eye_line)

        # Mouth - varies by emotion
        mouth_y = y - s * 0.2

        if self.emotion == Emotion.HAPPY or self.mouth_open > 0:
            mouth = patches.Arc(
                (x, mouth_y), s * 0.8, s * 0.5,
                angle=0, theta1=200, theta2=340,
                color=self.dark_color, linewidth=3, zorder=18
            )
            ax.add_patch(mouth)
        elif self.emotion == Emotion.SAD:
            mouth = patches.Arc(
                (x, mouth_y - s * 0.1), s * 0.5, s * 0.3,
                angle=0, theta1=20, theta2=160,
                color=self.dark_color, linewidth=3, zorder=18
            )
            ax.add_patch(mouth)
        elif self.emotion == Emotion.ANGRY:
            # Angry frown
            ax.plot([x - s * 0.3, x + s * 0.3],
                   [mouth_y + s * 0.05, mouth_y + s * 0.05],
                   color=self.dark_color, linewidth=3, zorder=18)
        elif self.emotion == Emotion.SHOCKED:
            mouth = patches.Circle(
                (x, mouth_y), s * 0.15,
                color=self.dark_color, alpha=self.alpha, zorder=18
            )
            ax.add_patch(mouth)
        else:
            # Neutral
            mouth = patches.Arc(
                (x, mouth_y), s * 0.5, s * 0.2,
                angle=0, theta1=200, theta2=340,
                color=self.dark_color, linewidth=2, zorder=18
            )
            ax.add_patch(mouth)

        # Crown (if has_crown)
        if self.has_crown:
            crown_y = y + s * 0.9
            # Crown base
            crown_points = [
                [x - s * 0.4, crown_y],
                [x - s * 0.35, crown_y + s * 0.3],
                [x - s * 0.2, crown_y + s * 0.15],
                [x, crown_y + s * 0.4],
                [x + s * 0.2, crown_y + s * 0.15],
                [x + s * 0.35, crown_y + s * 0.3],
                [x + s * 0.4, crown_y],
            ]
            crown = patches.Polygon(crown_points, color='#FFD700',
                                   alpha=self.alpha, zorder=20)
            ax.add_patch(crown)
            # Crown jewel
            jewel = patches.Circle((x, crown_y + s * 0.25), s * 0.08,
                                  color='#FF0000', alpha=self.alpha, zorder=21)
            ax.add_patch(jewel)

        # Emotion-specific effects
        if self.emotion == Emotion.LOVE:
            # Floating hearts
            for i in range(3):
                heart_y = y + s * (0.8 + (frame * 0.02 + i * 0.5) % 1.5)
                heart_x = x + s * 0.5 + np.sin(frame * 0.05 + i) * s * 0.3
                heart_alpha = 1 - ((frame * 0.02 + i * 0.5) % 1.5) / 1.5
                ax.text(heart_x, heart_y, '♥', fontsize=int(12 * self.scale),
                       color='#FF69B4', alpha=heart_alpha * self.alpha,
                       ha='center', va='center', zorder=25)

        elif self.emotion == Emotion.ANGRY:
            # Anger veins
            vein_x = x + s * 0.5
            vein_y = y + s * 0.6
            ax.text(vein_x, vein_y, '💢', fontsize=int(10 * self.scale),
                   alpha=self.alpha, ha='center', zorder=25)

        elif self.emotion == Emotion.POWERFUL:
            # Power aura
            for i in range(2):
                aura = patches.Circle(
                    (x, y), s * (2 + i * 0.5) + np.sin(frame * 0.1) * s * 0.2,
                    fill=False, edgecolor=self.glow_color,
                    linewidth=2, alpha=0.5 - i * 0.2, zorder=8
                )
                ax.add_patch(aura)

        # Render speech bubble
        self.render_speech(ax)


class WiseTurtle(Character):
    """Sage the Ancient Turtle - Eli's Mentor"""

    def __init__(self, x: float, y: float, scale: float = 1.5):
        super().__init__(x, y, scale, "Sage")
        self.shell_pattern_phase = np.random.uniform(0, 2 * np.pi)

    def render(self, ax, frame: int):
        if self.alpha <= 0:
            return

        s = self.scale * 40
        x, y = self.x, self.y

        # Shell
        shell = patches.Ellipse((x, y + s * 0.2), s * 2.5, s * 2,
                                color='#8B4513', alpha=self.alpha, zorder=10)
        ax.add_patch(shell)

        # Shell pattern (hexagonal-ish)
        shell_top = patches.Ellipse((x, y + s * 0.3), s * 2, s * 1.5,
                                    color='#A0522D', alpha=self.alpha, zorder=11)
        ax.add_patch(shell_top)

        # Shell segments
        for i in range(5):
            angle = (i / 5) * np.pi + 0.3
            seg_x = x + np.cos(angle) * s * 0.7
            seg_y = y + s * 0.3 + np.sin(angle) * s * 0.5
            seg = patches.Circle((seg_x, seg_y), s * 0.3,
                                 color='#6B4423', alpha=self.alpha * 0.7, zorder=12)
            ax.add_patch(seg)

        # Head
        head_x = x + s * 1.2 * self.facing
        head = patches.Ellipse((head_x, y), s * 0.8, s * 0.6,
                              color='#6B8E23', alpha=self.alpha, zorder=13)
        ax.add_patch(head)

        # Wise old eyes
        for side in [-1, 1]:
            eye_x = head_x + side * s * 0.15 * self.facing
            eye_y = y + s * 0.1

            # Eye
            eye = patches.Circle((eye_x, eye_y), s * 0.12,
                                 color='white', alpha=self.alpha, zorder=14)
            ax.add_patch(eye)

            # Small wise pupil
            pupil = patches.Circle((eye_x, eye_y), s * 0.05,
                                   color='black', alpha=self.alpha, zorder=15)
            ax.add_patch(pupil)

        # Wise wrinkles / eyebrows
        brow_y = y + s * 0.25
        ax.plot([head_x - s * 0.25, head_x - s * 0.1],
               [brow_y, brow_y + s * 0.05],
               color='#556B2F', linewidth=2, alpha=self.alpha, zorder=16)
        ax.plot([head_x + s * 0.1, head_x + s * 0.25],
               [brow_y + s * 0.05, brow_y],
               color='#556B2F', linewidth=2, alpha=self.alpha, zorder=16)

        # Gentle smile
        mouth = patches.Arc((head_x, y - s * 0.15), s * 0.3, s * 0.15,
                           angle=0, theta1=200, theta2=340,
                           color='#556B2F', linewidth=2, zorder=16)
        ax.add_patch(mouth)

        # Legs
        leg_positions = [(-1, -0.3), (1, -0.3), (-0.8, 0.5), (0.8, 0.5)]
        for lx, ly in leg_positions:
            leg = patches.Ellipse((x + lx * s, y + ly * s * 0.5 - s * 0.3),
                                 s * 0.4, s * 0.25,
                                 color='#6B8E23', alpha=self.alpha, zorder=9)
            ax.add_patch(leg)

        # Tail
        tail = patches.Polygon([
            [x - s * 1.2, y - s * 0.2],
            [x - s * 1.5, y - s * 0.3],
            [x - s * 1.2, y - s * 0.4],
        ], color='#6B8E23', alpha=self.alpha, zorder=9)
        ax.add_patch(tail)

        # Wisdom aura (subtle)
        if frame % 3 == 0:
            aura = patches.Circle((x, y), s * 3,
                                  fill=False, edgecolor='#FFD700',
                                  linewidth=1, alpha=0.1, zorder=8)
            ax.add_patch(aura)

        self.render_speech(ax)


class Dragonfly(Character):
    """Spark the Brave Dragonfly - Eli's loyal friend"""

    def __init__(self, x: float, y: float, scale: float = 0.8):
        super().__init__(x, y, scale, "Spark")
        self.wing_phase = 0
        self.hover_offset = 0

    def render(self, ax, frame: int):
        if self.alpha <= 0:
            return

        s = self.scale * 30
        x = self.x
        # Hovering motion
        self.hover_offset = np.sin(frame * 0.15) * s * 0.3
        y = self.y + self.hover_offset

        # Wings (fast flapping)
        self.wing_phase = frame * 0.8
        wing_angle = np.sin(self.wing_phase) * 30

        for side in [-1, 1]:
            # Upper wings
            wing_points = [
                [x, y],
                [x + side * s * 1.5, y + s * 0.8 + wing_angle * side * 0.02],
                [x + side * s * 0.5, y + s * 0.3],
            ]
            wing = patches.Polygon(wing_points, color='#ADD8E6',
                                  alpha=self.alpha * 0.6, zorder=12)
            ax.add_patch(wing)

            # Lower wings
            wing_points2 = [
                [x, y - s * 0.2],
                [x + side * s * 1.2, y - s * 0.5 - wing_angle * side * 0.02],
                [x + side * s * 0.3, y - s * 0.3],
            ]
            wing2 = patches.Polygon(wing_points2, color='#87CEEB',
                                   alpha=self.alpha * 0.5, zorder=12)
            ax.add_patch(wing2)

        # Body segments
        body_colors = ['#00CED1', '#008B8B', '#006666']
        for i, color in enumerate(body_colors):
            seg_y = y - i * s * 0.4
            seg = patches.Ellipse((x, seg_y), s * 0.4, s * 0.5,
                                 color=color, alpha=self.alpha, zorder=13)
            ax.add_patch(seg)

        # Tail
        for i in range(4):
            tail_y = y - s * (1.2 + i * 0.3)
            tail_width = s * (0.25 - i * 0.04)
            tail = patches.Ellipse((x, tail_y), tail_width, s * 0.35,
                                  color='#005555', alpha=self.alpha, zorder=13)
            ax.add_patch(tail)

        # Head
        head = patches.Circle((x, y + s * 0.5), s * 0.35,
                             color='#00CED1', alpha=self.alpha, zorder=14)
        ax.add_patch(head)

        # Big compound eyes
        for side in [-1, 1]:
            eye = patches.Circle((x + side * s * 0.2, y + s * 0.55), s * 0.18,
                                color='#FF4500', alpha=self.alpha, zorder=15)
            ax.add_patch(eye)
            # Eye shine
            shine = patches.Circle((x + side * s * 0.22, y + s * 0.58), s * 0.05,
                                  color='white', alpha=self.alpha * 0.7, zorder=16)
            ax.add_patch(shine)

        self.render_speech(ax)


class ShadowSerpent(Character):
    """The Shadow Serpent - First Major Boss"""

    def __init__(self, x: float, y: float, scale: float = 2.0):
        super().__init__(x, y, scale, "Shadow Serpent")
        self.coil_phase = 0
        self.health = 100
        self.is_attacking = False

    def render(self, ax, frame: int):
        if self.alpha <= 0:
            return

        s = self.scale * 30
        x, y = self.x, self.y
        self.coil_phase = frame * 0.03

        # Menacing shadow aura
        for i in range(3):
            aura = patches.Circle((x, y), s * (4 + i),
                                  color='#1a0033', alpha=0.1 - i * 0.03, zorder=5)
            ax.add_patch(aura)

        # Serpent body (sinuous coils)
        num_segments = 15
        for i in range(num_segments):
            t = i / num_segments
            seg_x = x - s * 3 * t + np.sin(self.coil_phase + t * 4) * s * 0.8
            seg_y = y - s * t * 2 + np.cos(self.coil_phase + t * 3) * s * 0.5
            seg_size = s * (1.2 - t * 0.6)

            # Dark scales
            segment = patches.Circle((seg_x, seg_y), seg_size,
                                    color='#2d0a4e', alpha=self.alpha, zorder=10 + i)
            ax.add_patch(segment)

            # Purple highlights
            highlight = patches.Circle((seg_x, seg_y + seg_size * 0.3),
                                       seg_size * 0.6,
                                       color='#4a0080', alpha=self.alpha * 0.5,
                                       zorder=11 + i)
            ax.add_patch(highlight)

        # Head
        head_x = x + s * 0.5
        head_y = y + np.sin(frame * 0.05) * s * 0.3

        head = patches.Ellipse((head_x, head_y), s * 2, s * 1.5,
                              angle=15 * self.facing,
                              color='#2d0a4e', alpha=self.alpha, zorder=30)
        ax.add_patch(head)

        # Evil eyes
        for side in [-1, 1]:
            eye_x = head_x + s * 0.3 * self.facing
            eye_y = head_y + side * s * 0.3

            eye = patches.Ellipse((eye_x, eye_y), s * 0.4, s * 0.25,
                                 color='#FF0000', alpha=self.alpha, zorder=31)
            ax.add_patch(eye)

            # Slit pupil
            pupil = patches.Ellipse((eye_x, eye_y), s * 0.08, s * 0.2,
                                   color='black', alpha=self.alpha, zorder=32)
            ax.add_patch(pupil)

        # Fangs
        if self.is_attacking or self.emotion == Emotion.ANGRY:
            for side in [-1, 1]:
                fang_x = head_x + s * 0.8
                fang_points = [
                    [fang_x, head_y + side * s * 0.2],
                    [fang_x + s * 0.5, head_y + side * s * 0.1],
                    [fang_x + s * 0.1, head_y + side * s * 0.4 * side],
                ]
                fang = patches.Polygon(fang_points, color='white',
                                       alpha=self.alpha, zorder=33)
                ax.add_patch(fang)

        # Forked tongue
        tongue_flick = np.sin(frame * 0.3) * s * 0.2
        tongue_x = head_x + s * 1
        ax.plot([head_x + s * 0.8, tongue_x, tongue_x + s * 0.3],
               [head_y, head_y, head_y + tongue_flick],
               color='#8B0000', linewidth=3, alpha=self.alpha, zorder=34)
        ax.plot([tongue_x, tongue_x + s * 0.3],
               [head_y, head_y - tongue_flick],
               color='#8B0000', linewidth=3, alpha=self.alpha, zorder=34)


class StormHeron(Character):
    """The Storm Heron - Second Major Boss"""

    def __init__(self, x: float, y: float, scale: float = 2.5):
        super().__init__(x, y, scale, "Storm Heron")
        self.wing_phase = 0
        self.health = 100

    def render(self, ax, frame: int):
        if self.alpha <= 0:
            return

        s = self.scale * 25
        x, y = self.x, self.y
        self.wing_phase = frame * 0.08

        wing_flap = np.sin(self.wing_phase) * 0.3

        # Wings
        for side in [-1, 1]:
            wing_angle = 20 + wing_flap * 40 * side
            wing_span = s * 4

            # Main wing
            wing_points = [
                [x, y + s * 1.5],
                [x + side * wing_span, y + s * 2 + wing_flap * s * side],
                [x + side * wing_span * 0.8, y + s * 1],
                [x + side * s * 0.5, y + s * 0.5],
            ]
            wing = patches.Polygon(wing_points, color='#E8E8E8',
                                  alpha=self.alpha, zorder=10)
            ax.add_patch(wing)

            # Wing feathers
            for i in range(5):
                f_t = i / 5
                f_x = x + side * wing_span * (0.3 + f_t * 0.7)
                f_y = y + s * (1.5 + wing_flap * f_t * side)
                feather = patches.Ellipse((f_x, f_y), s * 0.3, s * 1,
                                         angle=side * (30 + wing_flap * 20),
                                         color='#D3D3D3', alpha=self.alpha, zorder=11)
                ax.add_patch(feather)

        # Body
        body = patches.Ellipse((x, y + s * 1), s * 1.5, s * 3,
                              color='#F5F5F5', alpha=self.alpha, zorder=15)
        ax.add_patch(body)

        # Neck
        neck_curve_x = [x + i * s * 0.15 * self.facing for i in range(8)]
        neck_curve_y = [y + s * (2.5 + i * 0.5 - (i/8)**2 * 2) for i in range(8)]
        for i in range(7):
            neck_seg = patches.Circle((neck_curve_x[i], neck_curve_y[i]),
                                      s * (0.4 - i * 0.03),
                                      color='#F0F0F0', alpha=self.alpha, zorder=16 + i)
            ax.add_patch(neck_seg)

        # Head
        head_x = neck_curve_x[-1] + s * 0.5 * self.facing
        head_y = neck_curve_y[-1]

        head = patches.Ellipse((head_x, head_y), s * 1.2, s * 0.8,
                              angle=15 * self.facing,
                              color='#F5F5F5', alpha=self.alpha, zorder=25)
        ax.add_patch(head)

        # Menacing eye
        eye_x = head_x + s * 0.2 * self.facing
        eye_y = head_y + s * 0.1
        eye = patches.Circle((eye_x, eye_y), s * 0.15,
                            color='#FF4500', alpha=self.alpha, zorder=26)
        ax.add_patch(eye)
        pupil = patches.Circle((eye_x + s * 0.03 * self.facing, eye_y), s * 0.06,
                              color='black', alpha=self.alpha, zorder=27)
        ax.add_patch(pupil)

        # Deadly beak
        beak_points = [
            [head_x + s * 0.5 * self.facing, head_y + s * 0.1],
            [head_x + s * 2.5 * self.facing, head_y],
            [head_x + s * 0.5 * self.facing, head_y - s * 0.2],
        ]
        beak = patches.Polygon(beak_points, color='#FFA500',
                              alpha=self.alpha, zorder=28)
        ax.add_patch(beak)

        # Legs
        leg_y = y - s * 0.5
        for side in [-1, 1]:
            # Upper leg
            ax.plot([x + side * s * 0.3, x + side * s * 0.5],
                   [leg_y, leg_y - s * 2],
                   color='#FFA500', linewidth=4, alpha=self.alpha, zorder=14)
            # Lower leg
            ax.plot([x + side * s * 0.5, x + side * s * 0.3],
                   [leg_y - s * 2, leg_y - s * 3],
                   color='#FFA500', linewidth=3, alpha=self.alpha, zorder=14)


class TheDarkOne(Character):
    """The Dark One - Ultimate Final Boss"""

    def __init__(self, x: float, y: float, scale: float = 3.0):
        super().__init__(x, y, scale, "The Dark One")
        self.health = 100
        self.phase = 1  # Boss phases 1-3
        self.aura_phase = 0

    def render(self, ax, frame: int):
        if self.alpha <= 0:
            return

        s = self.scale * 40
        x, y = self.x, self.y
        self.aura_phase = frame * 0.02

        # Massive dark aura
        for i in range(5):
            aura_size = s * (5 + i * 1.5) + np.sin(self.aura_phase + i) * s * 0.5
            aura = patches.Circle((x, y), aura_size,
                                  color='#0a0010',
                                  alpha=0.15 - i * 0.025, zorder=3)
            ax.add_patch(aura)

        # Swirling dark energy
        for i in range(12):
            angle = (i / 12) * 2 * np.pi + self.aura_phase
            dist = s * 3 + np.sin(self.aura_phase * 2 + i) * s
            ex = x + np.cos(angle) * dist
            ey = y + np.sin(angle) * dist
            energy = patches.Circle((ex, ey), s * 0.4,
                                    color='#4B0082', alpha=0.6, zorder=4)
            ax.add_patch(energy)

        # Main form - amorphous dark entity
        body = patches.Circle((x, y), s * 2 + np.sin(frame * 0.05) * s * 0.2,
                              color='#0D0D0D', alpha=self.alpha, zorder=10)
        ax.add_patch(body)

        # Inner glow
        inner = patches.Circle((x, y), s * 1.5,
                               color='#1a0033', alpha=self.alpha, zorder=11)
        ax.add_patch(inner)

        # Core
        core = patches.Circle((x, y), s * 0.8,
                              color='#4B0082', alpha=self.alpha, zorder=12)
        ax.add_patch(core)

        # Multiple evil eyes
        eye_positions = [
            (0, 0.5, 1.0),    # Center top (main eye)
            (-0.4, 0.2, 0.6), # Left
            (0.4, 0.2, 0.6),  # Right
            (-0.2, -0.3, 0.4),
            (0.2, -0.3, 0.4),
        ]

        for ex_off, ey_off, eye_scale in eye_positions:
            eye_x = x + ex_off * s
            eye_y = y + ey_off * s

            # Eye socket
            socket = patches.Circle((eye_x, eye_y), s * 0.3 * eye_scale,
                                   color='#8B0000', alpha=self.alpha, zorder=13)
            ax.add_patch(socket)

            # Glowing eye
            eye = patches.Circle((eye_x, eye_y), s * 0.2 * eye_scale,
                                 color='#FF0000', alpha=self.alpha, zorder=14)
            ax.add_patch(eye)

            # Pulsing pupil
            pulse = np.sin(frame * 0.1) * 0.3 + 0.7
            pupil = patches.Circle((eye_x, eye_y), s * 0.08 * eye_scale * pulse,
                                   color='#FFFF00', alpha=self.alpha, zorder=15)
            ax.add_patch(pupil)

        # Dark tendrils
        for i in range(8):
            angle = (i / 8) * 2 * np.pi + np.sin(frame * 0.02) * 0.5
            tendril_length = s * (2.5 + np.sin(frame * 0.05 + i) * 0.5)

            points = []
            for j in range(6):
                t = j / 5
                tx = x + np.cos(angle + np.sin(frame * 0.03 + j) * 0.3) * tendril_length * t
                ty = y + np.sin(angle + np.cos(frame * 0.04 + j) * 0.3) * tendril_length * t
                points.append([tx, ty])

            for j in range(len(points) - 1):
                width = 8 * (1 - j / len(points))
                ax.plot([points[j][0], points[j+1][0]],
                       [points[j][1], points[j+1][1]],
                       color='#1a0033', linewidth=width,
                       alpha=self.alpha * 0.8, zorder=9)


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         ENVIRONMENT SYSTEM                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class Environment:
    """Base environment renderer"""

    def __init__(self):
        self.elements = []

    def render_background(self, ax, frame: int, lighting: LightingSystem):
        raise NotImplementedError

    def render_foreground(self, ax, frame: int):
        pass


class PondEnvironment(Environment):
    """Peaceful pond environment"""

    def __init__(self):
        super().__init__()
        # Generate lilypads
        self.lilypads = [
            {'x': WIDTH * 0.2, 'y': HEIGHT * 0.22, 'size': 100, 'rot': 0},
            {'x': WIDTH * 0.5, 'y': HEIGHT * 0.18, 'size': 120, 'rot': 15},
            {'x': WIDTH * 0.75, 'y': HEIGHT * 0.25, 'size': 90, 'rot': -10},
            {'x': WIDTH * 0.35, 'y': HEIGHT * 0.28, 'size': 80, 'rot': 25},
        ]
        # Reeds
        self.reeds = [50, 120, WIDTH - 80, WIDTH - 150]
        # Flies
        self.flies = [(np.random.uniform(100, WIDTH-100),
                      np.random.uniform(HEIGHT*0.4, HEIGHT*0.7),
                      np.random.uniform(0, 2*np.pi)) for _ in range(6)]

    def render_background(self, ax, frame: int, lighting: LightingSystem):
        # Sky
        sky_color = lighting.get_sky_color()
        ax.set_facecolor(sky_color)

        # Render celestial bodies
        lighting.render_celestial(ax, frame)

        # Distant hills (parallax layer)
        hill_color = lighting.apply_ambient_to_color('#228B22')
        for i, (hx, hw, hh) in enumerate([(0, 600, 150), (400, 800, 200), (900, 700, 180)]):
            hill = patches.Ellipse((hx + hw/2, HEIGHT * 0.4 + hh/2),
                                  hw, hh, color=hill_color, alpha=0.6, zorder=2)
            ax.add_patch(hill)

        # Pond water
        water_color = lighting.apply_ambient_to_color(Palette.WATER_SURFACE)
        pond = patches.Rectangle((0, 0), WIDTH, HEIGHT * 0.35,
                                 color=water_color, zorder=5)
        ax.add_patch(pond)

        # Water surface shimmer
        for i in range(8):
            wave_y = HEIGHT * 0.35 - i * 10
            phase = frame * 0.03 + i * 0.5
            wave_x = np.linspace(0, WIDTH, 50)
            wave_heights = wave_y + np.sin(wave_x * 0.01 + phase) * 3
            ax.fill_between(wave_x, wave_heights, wave_y - 5,
                           color=Palette.WATER_SHALLOW, alpha=0.15, zorder=6)

        # Lilypads
        for pad in self.lilypads:
            bob = np.sin(frame * 0.02 + pad['x'] * 0.01) * 2
            pad_color = lighting.apply_ambient_to_color(Palette.LILYPAD_NORMAL)

            lilypad = patches.Ellipse((pad['x'], pad['y'] + bob),
                                      pad['size'], pad['size'] * 0.6,
                                      angle=pad['rot'],
                                      color=pad_color, zorder=7)
            ax.add_patch(lilypad)

            # Lilypad notch
            notch = patches.Wedge((pad['x'], pad['y'] + bob),
                                  pad['size'] * 0.4, 170 + pad['rot'], 190 + pad['rot'],
                                  color=water_color, zorder=8)
            ax.add_patch(notch)

        # Cattails/reeds
        for rx in self.reeds:
            for h in range(7):
                ry = HEIGHT * 0.35 + h * 25
                sway = np.sin(frame * 0.02 + rx * 0.01 + h * 0.2) * 4
                reed = patches.Rectangle((rx + sway - 3, ry), 6, 22,
                                         color='#556B2F', zorder=6)
                ax.add_patch(reed)
            # Cattail head
            head_sway = np.sin(frame * 0.02 + rx * 0.01) * 4
            head = patches.Ellipse((rx + head_sway, HEIGHT * 0.35 + 190),
                                  14, 35, color='#8B4513', zorder=7)
            ax.add_patch(head)

        # Flies
        for i, (fx, fy, phase) in enumerate(self.flies):
            fly_x = fx + np.sin(frame * 0.08 + phase) * 25
            fly_y = fy + np.cos(frame * 0.1 + phase) * 15
            fly = patches.Circle((fly_x, fly_y), 4, color='#333333', zorder=20)
            ax.add_patch(fly)
            # Wings
            wing_spread = 2 + np.sin(frame * 0.5 + i) * 2
            ax.plot([fly_x - wing_spread, fly_x, fly_x + wing_spread],
                   [fly_y + 2, fly_y, fly_y + 2],
                   color='#666666', linewidth=1, alpha=0.6, zorder=20)


class DarkForestEnvironment(Environment):
    """Ominous dark forest"""

    def __init__(self):
        super().__init__()
        self.trees = [(np.random.uniform(0, WIDTH),
                      np.random.uniform(0.4, 0.9),
                      np.random.uniform(0.8, 1.5)) for _ in range(15)]

    def render_background(self, ax, frame: int, lighting: LightingSystem):
        ax.set_facecolor('#0a0a12')

        # Eerie fog layers
        for i in range(3):
            fog_y = HEIGHT * (0.3 + i * 0.2)
            fog = patches.Rectangle((0, fog_y - 50), WIDTH, 100,
                                    color='#1a1a2a', alpha=0.3, zorder=3 + i)
            ax.add_patch(fog)

        # Dead trees
        for tx, ty_mult, scale in self.trees:
            ty = HEIGHT * ty_mult
            trunk_h = 200 * scale
            trunk_w = 20 * scale

            # Trunk
            trunk = patches.Rectangle((tx - trunk_w/2, ty - trunk_h),
                                      trunk_w, trunk_h,
                                      color='#1a1a1a', zorder=5)
            ax.add_patch(trunk)

            # Gnarled branches
            for b in range(4):
                b_angle = np.pi/4 + b * np.pi/6 + np.sin(frame * 0.01 + tx) * 0.1
                b_len = 60 * scale
                bx = tx + np.cos(b_angle) * b_len * (1 if b % 2 == 0 else -1)
                by = ty - trunk_h * 0.7 + b * 20
                ax.plot([tx, bx], [by, by + 30],
                       color='#1a1a1a', linewidth=8 * scale, zorder=5)

        # Ground fog
        fog = patches.Rectangle((0, 0), WIDTH, HEIGHT * 0.2,
                                color='#2a2a3a', alpha=0.5, zorder=4)
        ax.add_patch(fog)


class BattleArenaEnvironment(Environment):
    """Epic battle arena"""

    def __init__(self):
        super().__init__()

    def render_background(self, ax, frame: int, lighting: LightingSystem):
        # Dramatic dark red sky
        ax.set_facecolor('#1a0a0a')

        # Ominous clouds
        for i in range(5):
            cx = (frame * 0.5 + i * 400) % (WIDTH + 400) - 200
            cy = HEIGHT * (0.7 + i * 0.05)
            cloud = patches.Ellipse((cx, cy), 300, 80,
                                   color='#2a1515', alpha=0.6, zorder=2)
            ax.add_patch(cloud)

        # Cracked ground
        ground = patches.Rectangle((0, 0), WIDTH, HEIGHT * 0.3,
                                   color='#2a1a10', zorder=5)
        ax.add_patch(ground)

        # Lava cracks
        for i in range(8):
            cx = WIDTH * (i + 0.5) / 8
            crack_glow = np.sin(frame * 0.05 + i) * 0.3 + 0.7
            crack = patches.Rectangle((cx - 5, 0), 10, HEIGHT * 0.25,
                                      color='#FF4500', alpha=crack_glow * 0.5, zorder=6)
            ax.add_patch(crack)

        # Dramatic pillars
        for i, px in enumerate([WIDTH * 0.1, WIDTH * 0.9]):
            pillar = patches.Rectangle((px - 30, 0), 60, HEIGHT * 0.6,
                                       color='#333333', zorder=7)
            ax.add_patch(pillar)
            # Fire on top
            fire_flicker = np.sin(frame * 0.1 + i) * 10
            fire = patches.Circle((px, HEIGHT * 0.6 + fire_flicker),
                                  40 + fire_flicker, color='#FF4500',
                                  alpha=0.8, zorder=8)
            ax.add_patch(fire)


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                              SCENE SYSTEM                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class Scene:
    """Base scene class"""
    def __init__(self, start: int, duration: int):
        self.start = start
        self.end = start + duration
        self.duration = duration

    def progress(self, frame: int) -> float:
        return clamp((frame - self.start) / self.duration, 0, 1)

    def render(self, ax, frame: int, ctx: dict):
        raise NotImplementedError


class TitleScene(Scene):
    """Epic title screen"""
    def render(self, ax, frame: int, ctx: dict):
        p = self.progress(frame)
        local = frame - self.start
        ax.set_facecolor('#000008')

        # Stars
        np.random.seed(42)
        for i in range(120):
            twinkle = 0.4 + 0.6 * abs(np.sin(local * 0.04 + i))
            ax.scatter([np.random.rand() * WIDTH], [np.random.rand() * HEIGHT],
                      c='white', s=twinkle * 20, alpha=twinkle, zorder=1)

        # Title with elastic entrance
        if p > 0.1:
            t_prog = Easing.ease_out_elastic(min(1, (p - 0.1) / 0.3))
            for i in range(3):
                ax.text(WIDTH/2, HEIGHT * 0.62, "ELI IS A FROG",
                       fontsize=int(70 * t_prog), fontweight='bold', ha='center', va='center',
                       color='#00FF00', alpha=0.2 - i * 0.05, zorder=10)
            ax.text(WIDTH/2, HEIGHT * 0.62, "ELI IS A FROG",
                   fontsize=int(70 * t_prog), fontweight='bold', ha='center', va='center',
                   color='#90EE90', zorder=11)

        # Subtitle fade
        if p > 0.35:
            s_alpha = Easing.ease_out_cubic(min(1, (p - 0.35) / 0.2))
            ax.text(WIDTH/2, HEIGHT * 0.48, "THE LEGEND OF THE EMERALD GUARDIAN",
                   fontsize=26, ha='center', color='#FFD700', alpha=s_alpha, zorder=11)

        # Dancing frogs
        if p > 0.5:
            for i in range(5):
                bounce = abs(np.sin(local * 0.12 + i * 0.9)) * 25
                frog = Frog(WIDTH * (0.18 + i * 0.16), HEIGHT * 0.2 + bounce, 0.6)
                frog.emotion = Emotion.HAPPY
                frog.alpha = min(1, (p - 0.5) / 0.2)
                frog.render(ax, local)

        if local % 10 == 0:
            ctx['particles'].emit_magic(WIDTH/2 + np.random.randn() * 150, HEIGHT * 0.6, 'gold', 0.6)


class ChapterScene(Scene):
    """Chapter title card"""
    def __init__(self, start: int, duration: int, num: int, title: str):
        super().__init__(start, duration)
        self.num, self.title = num, title

    def render(self, ax, frame: int, ctx: dict):
        p = self.progress(frame)
        ax.set_facecolor('#000000')
        alpha = 1 - abs(p - 0.5) * 2 if p < 0.15 or p > 0.85 else 1
        alpha = max(0, min(1, alpha * 2))

        ax.text(WIDTH/2, HEIGHT * 0.55, f"— CHAPTER {self.num} —",
               fontsize=24, ha='center', color='#FFD700', alpha=alpha, zorder=10)
        ax.text(WIDTH/2, HEIGHT * 0.42, self.title.upper(),
               fontsize=48, fontweight='bold', ha='center', color='white', alpha=alpha, zorder=10)


class StoryScene(Scene):
    """General story scene with environment and characters"""
    def __init__(self, start: int, duration: int, env_type: str = 'pond', time: str = 'day'):
        super().__init__(start, duration)
        self.env = PondEnvironment() if env_type == 'pond' else DarkForestEnvironment() if env_type == 'forest' else BattleArenaEnvironment()
        self.time = time
        self.chars = []
        self.events = []

    def add_char(self, char: Character): self.chars.append(char)
    def add_event(self, start_pct: float, callback): self.events.append((start_pct, callback))

    def render(self, ax, frame: int, ctx: dict):
        p = self.progress(frame)
        local = frame - self.start

        # Set time of day
        times = {'dawn': TimeOfDay.DAWN, 'day': TimeOfDay.NOON, 'sunset': TimeOfDay.SUNSET,
                'night': TimeOfDay.NIGHT, 'dark': TimeOfDay.MIDNIGHT}
        ctx['lighting'].set_time(times.get(self.time, TimeOfDay.NOON), immediate=True)

        self.env.render_background(ax, frame, ctx['lighting'])

        for start_pct, cb in self.events:
            if p >= start_pct:
                cb(p, local, ctx, self.chars)

        for c in self.chars:
            c.update(local)
            c.render(ax, local)


class TransformScene(Scene):
    """Magical transformation"""
    def render(self, ax, frame: int, ctx: dict):
        p = self.progress(frame)
        local = frame - self.start
        ax.set_facecolor('#1a0a2e')

        # Swirling vortex
        for i in range(25):
            angle = (i / 25) * 2 * np.pi + local * 0.025
            dist = 120 + 200 * (1 - abs(p - 0.5) * 2)
            px, py = WIDTH/2 + np.cos(angle) * dist, HEIGHT/2 + np.sin(angle) * dist * 0.7
            ax.scatter([px], [py], c='#9400D3' if i % 2 else '#00FF7F', s=15 + 15 * np.sin(local * 0.05 + i), alpha=0.7, zorder=5)

        # Rings
        for r in range(3):
            ax.add_patch(patches.Circle((WIDTH/2, HEIGHT/2), 100 + r * 35 + np.sin(local * 0.08) * 15,
                        fill=False, edgecolor='#FFD700', linewidth=2, alpha=0.5 - r * 0.1, zorder=10))

        # Human fade
        if p < 0.4:
            alpha = 1 - p * 2.5
            ax.add_patch(patches.Circle((WIDTH/2, HEIGHT/2 + 70), 30, color='white', alpha=alpha, zorder=15))
            ax.add_patch(patches.Rectangle((WIDTH/2 - 20, HEIGHT/2 - 40), 40, 90, color='white', alpha=alpha, zorder=15))

        # Frog emerge
        if p > 0.25:
            frog = Frog(WIDTH/2, HEIGHT/2, 0.8 + p)
            frog.alpha = min(1, (p - 0.25) / 0.4)
            frog.emotion = Emotion.SHOCKED if p < 0.65 else Emotion.POWERFUL
            frog.set_glow(True, '#00FF7F', frog.alpha)
            frog.render(ax, local)

        if local % 4 == 0:
            ctx['particles'].emit_magic(WIDTH/2 + np.random.randn() * 60, HEIGHT/2 + np.random.randn() * 60, 'purple', 0.8)

        if p > 0.8:
            ax.text(WIDTH/2, HEIGHT * 0.12, "THE TRANSFORMATION IS COMPLETE",
                   fontsize=32, ha='center', color='#FFD700', alpha=(p - 0.8) / 0.2, fontweight='bold', zorder=100)


class BattleScene(Scene):
    """Boss battle"""
    def __init__(self, start: int, duration: int, boss_type: str):
        super().__init__(start, duration)
        self.boss_type = boss_type
        self.env = BattleArenaEnvironment()

    def render(self, ax, frame: int, ctx: dict):
        p = self.progress(frame)
        local = frame - self.start
        self.env.render_background(ax, frame, ctx['lighting'])

        # Create boss
        if self.boss_type == 'serpent':
            boss = ShadowSerpent(WIDTH * 0.7, HEIGHT * 0.4, 1.8)
        elif self.boss_type == 'heron':
            boss = StormHeron(WIDTH * 0.75, HEIGHT * 0.35, 2.0)
        else:
            boss = TheDarkOne(WIDTH * 0.65, HEIGHT * 0.5, 2.5)

        hero = Frog(WIDTH * 0.25, HEIGHT * 0.35, 1.2)
        hero.emotion = Emotion.DETERMINED if p < 0.7 else Emotion.POWERFUL
        hero.set_glow(p > 0.5, '#00FF7F', min(1, (p - 0.5) * 2))

        boss.emotion = Emotion.ANGRY
        if hasattr(boss, 'is_attacking'):
            boss.is_attacking = (local % 50) < 25

        # Combat
        if local % 40 == 0 and p < 0.9:
            hero.jump(10)
            ctx['particles'].emit_magic(hero.x, hero.y, 'green', 1.2)
            ctx['camera'].shake(12, 0.88)
        if local % 55 == 25:
            ctx['particles'].emit_dark_energy(boss.x, boss.y, 1.0)

        boss.render(ax, local)
        hero.render(ax, local)

        # Health bars
        boss_hp = max(0, 100 - p * 105)
        ax.add_patch(patches.Rectangle((WIDTH/2 - 180, HEIGHT - 55), 360, 25, color='#222', zorder=200))
        ax.add_patch(patches.Rectangle((WIDTH/2 - 175, HEIGHT - 52), 350 * boss_hp / 100, 19, color='#FF0000', zorder=201))
        ax.text(WIDTH/2, HEIGHT - 75, self.boss_type.upper().replace('_', ' '), fontsize=18, ha='center', color='#FF4444', fontweight='bold', zorder=202)

        # Victory
        if p > 0.92:
            ax.add_patch(patches.Rectangle((0, 0), WIDTH, HEIGHT, color='white', alpha=(p - 0.92) / 0.08 * 0.7, zorder=300))
            ax.text(WIDTH/2, HEIGHT/2, "VICTORY!", fontsize=70, ha='center', va='center', color='#FFD700', alpha=(p - 0.92) / 0.08, fontweight='bold', zorder=301)


class CreditsScene(Scene):
    """Rolling credits"""
    def render(self, ax, frame: int, ctx: dict):
        local = frame - self.start
        ax.set_facecolor('#000000')

        np.random.seed(999)
        for _ in range(100):
            ax.scatter([np.random.rand() * WIDTH], [np.random.rand() * HEIGHT], c='white', s=np.random.rand() * 12, alpha=0.6)

        credits = [("ELI IS A FROG", 65, '#90EE90'), ("THE LEGEND OF THE EMERALD GUARDIAN", 24, '#FFD700'), ("", 35, 'w'),
                   ("Directed by", 20, '#888'), ("Claude Code Productions", 28, '#FFD700'), ("", 25, 'w'),
                   ("Starring", 20, '#888'), ("ELI - The Emerald Guardian", 24, '#32CD32'),
                   ("SAGE - The Wise Mentor", 22, '#8B4513'), ("SPARK - The Loyal Friend", 22, '#00CED1'),
                   ("LUNA - The Princess", 22, '#FF69B4'), ("", 25, 'w'),
                   ("THE SHADOW SERPENT", 22, '#4B0082'), ("THE STORM HERON", 22, '#708090'),
                   ("THE DARK ONE", 22, '#8B0000'), ("", 30, 'w'),
                   ("Animation", 20, '#888'), ("Matplotlib Studios", 24, '#87CEEB'), ("", 20, 'w'),
                   ("Sound", 20, '#888'), ("NumPy Audio", 24, '#87CEEB'), ("", 35, 'w'),
                   ("A CLAUDE CODE PRODUCTION", 28, '#FFD700'), ("", 25, 'w'),
                   ("THE END", 45, '#90EE90')]

        y = -local * 1.0 + HEIGHT * 0.25
        for txt, sz, col in credits:
            if -40 < y < HEIGHT + 40:
                ax.text(WIDTH/2, y, txt, fontsize=sz, ha='center', color=col, zorder=10)
            y += sz * 1.7

        if local > self.duration * 0.85:
            frog = Frog(WIDTH/2, 90, 0.9)
            frog.emotion = Emotion.HAPPY
            frog.has_crown = True
            frog.render(ax, local)


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                           EPIC SOUNDTRACK                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

def generate_epic_soundtrack(duration: int, sample_rate: int = 44100) -> np.ndarray:
    """Generate an epic orchestral-style soundtrack"""
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples)
    audio = np.zeros(samples)

    # Ambient pad (strings-like)
    pad_freqs = [130.81, 164.81, 196.00, 261.63]  # C major chord
    for freq in pad_freqs:
        # Slow attack pad
        env = (1 - np.exp(-t * 0.5)) * np.exp(-t * 0.001)
        audio += np.sin(2 * np.pi * freq * t) * env * 0.03
        audio += np.sin(2 * np.pi * freq * 2 * t) * env * 0.015  # Harmonic

    # Epic drums pattern
    drum_pattern = [0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 3.0, 3.5]
    for base_time in range(0, duration, 4):
        for offset in drum_pattern:
            hit_time = base_time + offset
            if hit_time < duration:
                start = int(hit_time * sample_rate)
                length = min(int(0.2 * sample_rate), samples - start)
                if length > 0:
                    drum_t = np.linspace(0, 0.2, length)
                    # Kick drum
                    kick = np.sin(2 * np.pi * (80 - drum_t * 200) * drum_t) * np.exp(-drum_t * 15)
                    audio[start:start+length] += kick * 0.15

    # Heroic melody
    melody_notes = [
        (261.63, 0.5), (293.66, 0.5), (329.63, 1.0), (293.66, 0.5), (261.63, 0.5),
        (329.63, 0.5), (349.23, 0.5), (392.00, 1.5), (349.23, 0.5),
        (329.63, 0.5), (293.66, 0.5), (261.63, 1.0), (196.00, 1.0),
        (261.63, 0.5), (329.63, 0.5), (392.00, 1.0), (440.00, 0.5), (392.00, 0.5),
        (349.23, 1.0), (329.63, 1.0), (293.66, 2.0),
    ]

    melody_duration = sum(n[1] for n in melody_notes)
    current_time = 5  # Start after intro

    while current_time < duration - 30:  # Leave room for ending
        note_time = current_time
        for freq, dur in melody_notes:
            if note_time + dur < duration:
                start = int(note_time * sample_rate)
                length = min(int(dur * sample_rate), samples - start)
                if length > 0:
                    note_t = np.linspace(0, dur, length)
                    envelope = (1 - np.exp(-note_t * 10)) * np.exp(-note_t * 1.5)
                    note = np.sin(2 * np.pi * freq * note_t) * envelope
                    note += np.sin(2 * np.pi * freq * 2 * note_t) * envelope * 0.3
                    audio[start:start+length] += note * 0.08
            note_time += dur
        current_time += melody_duration + 8  # Gap between repetitions

    # Ribbit sounds at key moments
    ribbit_times = [10, 25, 45, 70, 100, 130, 160, 200, 250, 300, 400, 500, 600, 700, 800]
    for rt in ribbit_times:
        if rt < duration:
            start = int(rt * sample_rate)
            ribbit_len = int(0.25 * sample_rate)
            if start + ribbit_len < samples:
                ribbit_t = np.linspace(0, 0.25, ribbit_len)
                freq1 = 220 + 80 * np.sin(2 * np.pi * 6 * ribbit_t)
                freq2 = 330 + 100 * np.sin(2 * np.pi * 8 * ribbit_t)
                env = np.exp(-ribbit_t * 10) * (1 - np.exp(-ribbit_t * 50))
                ribbit = (np.sin(2 * np.pi * freq1 * ribbit_t) * 0.4 +
                         np.sin(2 * np.pi * freq2 * ribbit_t) * 0.3) * env
                audio[start:start+ribbit_len] += ribbit * 0.2

    # Battle intensity sections (louder drums, faster tempo)
    battle_sections = [(420, 480), (540, 600), (660, 750)]
    for start_sec, end_sec in battle_sections:
        if start_sec < duration:
            start_s = int(start_sec * sample_rate)
            end_s = min(int(end_sec * sample_rate), samples)
            section_len = end_s - start_s
            if section_len > 0:
                battle_t = np.linspace(0, end_sec - start_sec, section_len)
                # Intense low rumble
                rumble = np.sin(2 * np.pi * 40 * battle_t) * 0.1
                rumble += np.sin(2 * np.pi * 60 * battle_t) * 0.08
                audio[start_s:end_s] += rumble * np.exp(-battle_t * 0.02)

    # Triumphant ending
    if duration > 60:
        end_start = int((duration - 30) * sample_rate)
        end_length = min(int(25 * sample_rate), samples - end_start)
        if end_length > 0:
            end_t = np.linspace(0, 25, end_length)
            # Major chord swell
            for freq in [261.63, 329.63, 392.00, 523.25]:
                swell = np.sin(2 * np.pi * freq * end_t)
                swell *= (1 - np.exp(-end_t * 0.3)) * np.exp(-(end_t - 12) ** 2 / 50)
                audio[end_start:end_start+end_length] += swell * 0.05

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.85

    return audio


def save_wav(filename: str, audio: np.ndarray, sample_rate: int = 44100):
    """Save audio as WAV file"""
    audio_int = np.int16(audio * 32767)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int.tobytes())


# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                         MAIN ANIMATION ENGINE                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

def build_scenes() -> List[Scene]:
    """Build the complete movie scene list"""
    scenes = []
    f = 0  # Frame counter

    # ACT I - THE ORDINARY WORLD
    scenes.append(TitleScene(f, 480)); f += 480  # 8 sec
    scenes.append(ChapterScene(f, 180, 1, "The Prophecy")); f += 180

    # Peaceful pond establishing shot
    s = StoryScene(f, 600, 'pond', 'day'); f += 600
    s.add_char(Frog(WIDTH * 0.5, HEIGHT * 0.22, 1.0))
    scenes.append(s)

    # The strange dreams
    scenes.append(ChapterScene(f, 180, 2, "Strange Dreams")); f += 180
    scenes.append(StoryScene(f, 480, 'pond', 'night')); f += 480

    # ACT II - THE TRANSFORMATION
    scenes.append(ChapterScene(f, 180, 3, "The Curse")); f += 180
    scenes.append(TransformScene(f, 720)); f += 720  # 12 sec transformation

    scenes.append(ChapterScene(f, 180, 4, "Awakening")); f += 180
    s = StoryScene(f, 600, 'pond', 'dawn'); f += 600
    s.add_char(Frog(WIDTH * 0.5, HEIGHT * 0.22, 1.2))
    scenes.append(s)

    # ACT III - MEETING ALLIES
    scenes.append(ChapterScene(f, 180, 5, "The Mentor")); f += 180
    s = StoryScene(f, 720, 'pond', 'day'); f += 720
    s.add_char(Frog(WIDTH * 0.35, HEIGHT * 0.22, 1.0))
    s.add_char(WiseTurtle(WIDTH * 0.65, HEIGHT * 0.25, 1.2))
    scenes.append(s)

    scenes.append(ChapterScene(f, 180, 6, "Allies Gather")); f += 180
    s = StoryScene(f, 720, 'pond', 'day'); f += 720
    s.add_char(Frog(WIDTH * 0.3, HEIGHT * 0.22, 1.0))
    s.add_char(Dragonfly(WIDTH * 0.5, HEIGHT * 0.5, 0.7))
    s.add_char(Frog(WIDTH * 0.7, HEIGHT * 0.25, 0.9, 'princess', 'Luna'))
    scenes.append(s)

    # ACT IV - THE TRIALS
    scenes.append(ChapterScene(f, 180, 7, "The Dark Forest")); f += 180
    scenes.append(StoryScene(f, 600, 'forest', 'night')); f += 600

    scenes.append(ChapterScene(f, 180, 8, "First Trial")); f += 180
    scenes.append(BattleScene(f, 900, 'serpent')); f += 900  # 15 sec battle

    # ACT V - RISING ACTION
    scenes.append(ChapterScene(f, 180, 9, "Love Blossoms")); f += 180
    s = StoryScene(f, 600, 'pond', 'sunset'); f += 600
    s.add_char(Frog(WIDTH * 0.4, HEIGHT * 0.22, 1.0))
    s.add_char(Frog(WIDTH * 0.6, HEIGHT * 0.22, 0.9, 'princess', 'Luna'))
    scenes.append(s)

    scenes.append(ChapterScene(f, 180, 10, "The Storm Approaches")); f += 180
    scenes.append(StoryScene(f, 480, 'pond', 'night')); f += 480

    # ACT VI - THE ORDEAL
    scenes.append(ChapterScene(f, 180, 11, "The Predator")); f += 180
    scenes.append(BattleScene(f, 900, 'heron')); f += 900

    scenes.append(ChapterScene(f, 180, 12, "Darkest Hour")); f += 180
    scenes.append(StoryScene(f, 600, 'forest', 'dark')); f += 600

    # ACT VII - THE FINAL BATTLE
    scenes.append(ChapterScene(f, 180, 13, "The Final Battle")); f += 180
    scenes.append(BattleScene(f, 1200, 'dark_one')); f += 1200  # 20 sec final boss

    # ACT VIII - RESOLUTION
    scenes.append(ChapterScene(f, 180, 14, "Victory")); f += 180
    s = StoryScene(f, 720, 'pond', 'dawn'); f += 720
    hero = Frog(WIDTH * 0.5, HEIGHT * 0.22, 1.3)
    hero.has_crown = True
    hero.set_glow(True, '#FFD700', 0.5)
    s.add_char(hero)
    scenes.append(s)

    scenes.append(ChapterScene(f, 180, 15, "The Legend Lives On")); f += 180
    s = StoryScene(f, 600, 'pond', 'day'); f += 600
    s.add_char(Frog(WIDTH * 0.3, HEIGHT * 0.22, 1.0))
    s.add_char(Frog(WIDTH * 0.5, HEIGHT * 0.22, 1.0))
    s.add_char(Frog(WIDTH * 0.7, HEIGHT * 0.22, 1.0))
    scenes.append(s)

    # CREDITS
    scenes.append(CreditsScene(f, 1200)); f += 1200

    print(f"Total frames: {f} ({f/FPS:.1f} seconds / {f/FPS/60:.1f} minutes)")
    return scenes


def create_animation():
    """Create the complete cinematic animation"""
    print("=" * 70)
    print("  ELI IS A FROG - THE LEGEND OF THE EMERALD GUARDIAN")
    print("  Creating the Ultimate Cinematic Masterpiece...")
    print("=" * 70)

    # Build scene list
    scenes = build_scenes()
    total_frames = scenes[-1].end

    # Create figure
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Create systems
    particles = AdvancedParticleSystem(max_particles=1500)
    camera = Camera(WIDTH, HEIGHT)
    lighting = LightingSystem()
    weather = WeatherSystem(particles)

    ctx = {
        'particles': particles,
        'camera': camera,
        'lighting': lighting,
        'weather': weather,
    }

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

        # Find and render current scene
        for scene in scenes:
            if scene.start <= frame < scene.end:
                scene.render(ax, frame, ctx)
                break

        # Update systems
        particles.update()
        camera.update()
        lighting.update(frame)
        weather.update(frame)

        # Render particles
        particles.render(ax)

        # Progress display
        if frame % 120 == 0:
            pct = frame / total_frames * 100
            print(f"\rRendering: {pct:.1f}% ({frame}/{total_frames})", end='', flush=True)

        return []

    print(f"\nTotal runtime: {total_frames/FPS:.0f} seconds ({total_frames/FPS/60:.1f} minutes)")
    print(f"Resolution: {WIDTH}x{HEIGHT} @ {FPS}fps")
    print(f"Total frames: {total_frames}")
    print("\nStarting animation...")

    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=total_frames, interval=1000/FPS, blit=False
    )

    return fig, anim, total_frames


def main():
    """Main entry point"""
    print("\n" + "═" * 70)
    print("║" + " " * 68 + "║")
    print("║" + "  ELI IS A FROG - THE LEGEND OF THE EMERALD GUARDIAN  ".center(68) + "║")
    print("║" + "  The Ultimate Cinematic Masterpiece  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("═" * 70 + "\n")

    # Generate soundtrack
    print("Generating epic soundtrack...")
    audio = generate_epic_soundtrack(DURATION)

    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, 'soundtrack.wav')
    save_wav(audio_path, audio)
    print(f"Soundtrack saved: {audio_path}")

    # Create animation
    fig, anim, total_frames = create_animation()

    # Save
    video_path = os.path.join(temp_dir, 'eli_video.mp4')
    print(f"\nSaving video to: {video_path}")
    print("This will take a while for a 15-minute epic...")

    try:
        writer = animation.FFMpegWriter(
            fps=FPS, bitrate=8000,
            metadata={'title': 'ELI IS A FROG', 'artist': 'Claude Code Productions'}
        )
        anim.save(video_path, writer=writer)
        print("\n\nVideo saved!")

        # Combine with audio
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eli_is_a_frog_movie.mp4')
        print(f"Combining audio... Output: {final_path}")

        subprocess.run([
            'ffmpeg', '-y', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', final_path
        ], check=True, capture_output=True)

        print("\n" + "═" * 70)
        print("  SUCCESS! Epic movie created!")
        print(f"  File: {final_path}")
        print(f"  Runtime: {DURATION // 60} minutes")
        print("═" * 70)

    except Exception as e:
        print(f"\nError: {e}")
        print(f"Video without audio saved at: {video_path}")

    plt.close(fig)
    print("\nDone!")


if __name__ == '__main__':
    main()
