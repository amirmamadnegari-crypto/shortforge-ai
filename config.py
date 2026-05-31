"""
ShortForge AI - Configuration System
Centralized configuration for all agents and settings.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ShortForgeAI")


# ─── App Config ───────────────────────────────────────────────────────────────
@dataclass
class AppConfig:
    app_name: str = "ShortForge AI"
    app_version: str = "1.0.0"
    app_description: str = "AI-powered YouTube Shorts viral content engine"
    anthropic_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4000
    temperature: float = 0.85  # Higher creativity for viral content


@dataclass
class UIConfig:
    primary_color: str = "#FF0033"       # YouTube red
    secondary_color: str = "#0A0A0A"     # Deep black
    accent_color: str = "#FFD700"        # Gold for scores
    success_color: str = "#00FF88"       # Neon green
    font_family: str = "Inter, sans-serif"
    sidebar_width: int = 320


@dataclass
class ContentConfig:
    """Limits and defaults for content generation."""
    ideas_count: int = 20
    hooks_count: int = 10
    script_min_seconds: int = 30
    script_max_seconds: int = 60
    hashtags_count: int = 20
    calendar_days: int = 30
    min_viral_score: int = 60      # Minimum acceptable viral score


@dataclass
class FootballConfig:
    """Football Creator Mode configuration."""
    enabled: bool = False
    league_focus: str = "Premier League"
    player_era: str = "Modern (2010-present)"
    content_pillars: list = field(default_factory=lambda: [
        "Player Stories",
        "Match Highlights",
        "Historical Moments",
        "Tactical Analysis",
        "Football Facts & Records",
        "Transfer Rumors",
        "GOAT Debates",
    ])
    viral_angles: list = field(default_factory=lambda: [
        "Underdog stories",
        "Record-breaking moments",
        "Shocking facts",
        "Greatest goals",
        "Career defining moments",
        "Rivalry highlights",
    ])


# ─── Master Config ────────────────────────────────────────────────────────────
@dataclass
class ShortForgeConfig:
    app: AppConfig = field(default_factory=AppConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    content: ContentConfig = field(default_factory=ContentConfig)
    football: FootballConfig = field(default_factory=FootballConfig)


# Singleton config instance
config = ShortForgeConfig()
