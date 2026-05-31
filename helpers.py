"""
ShortForge AI - Utility Functions
Shared helpers used across all agents.
"""

import json
import re
import logging
from typing import Any, Optional

logger = logging.getLogger("ShortForgeAI.utils")


def parse_json_response(raw: str) -> Optional[dict]:
    """
    Safely parse JSON from LLM response.
    Handles markdown code fences, extra whitespace, and common LLM quirks.
    """
    if not raw:
        return None
    try:
        # Strip markdown fences
        cleaned = re.sub(r"```json\s*", "", raw)
        cleaned = re.sub(r"```\s*", "", cleaned)
        cleaned = cleaned.strip()
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse failed: {e}. Raw (first 300): {raw[:300]}")
        # Try extracting first JSON object
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        return None


def score_to_color(score: int) -> str:
    """Return a color hex based on score value."""
    if score >= 85:
        return "#00FF88"   # Neon green - excellent
    elif score >= 70:
        return "#FFD700"   # Gold - good
    elif score >= 55:
        return "#FF8C00"   # Orange - average
    else:
        return "#FF4444"   # Red - poor


def score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def truncate_text(text: str, max_chars: int = 100, suffix: str = "...") -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - len(suffix)] + suffix


def format_duration(seconds: int) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    remaining = seconds % 60
    return f"{minutes}m {remaining}s" if remaining else f"{minutes}m"


def safe_get(data: dict, *keys, default=None) -> Any:
    """Safely navigate nested dict with fallback."""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current if current is not None else default


def extract_text_from_content_blocks(content_blocks: list) -> str:
    """Extract all text blocks from Anthropic API response content."""
    return "\n".join(
        block.get("text", "") if isinstance(block, dict) else getattr(block, "text", "")
        for block in content_blocks
        if (isinstance(block, dict) and block.get("type") == "text")
        or (hasattr(block, "type") and block.type == "text")
    )


def build_error_response(feature: str, error: str) -> dict:
    """Build a standardized error response dict."""
    logger.error(f"[{feature}] Error: {error}")
    return {
        "error": True,
        "feature": feature,
        "message": str(error),
        "fallback": f"Could not generate {feature}. Please try again.",
    }


def validate_topic(topic: str) -> tuple[bool, str]:
    """Validate topic input - returns (is_valid, message)."""
    topic = topic.strip()
    if not topic:
        return False, "Topic cannot be empty."
    if len(topic) < 2:
        return False, "Topic is too short. Please be more specific."
    if len(topic) > 200:
        return False, "Topic is too long. Keep it under 200 characters."
    return True, topic
