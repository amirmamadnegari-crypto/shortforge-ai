"""
ShortForge AI - Thumbnail Intelligence Agent
Recommends emotions, colors, text, composition, and psychology for thumbnails.
"""

import logging
from agents.base_agent import BaseAgent
from prompts import thumbnail_prompt

logger = logging.getLogger("ShortForgeAI.ThumbnailAgent")


EMOTION_TARGETS = [
    "curiosity",
    "shock",
    "fear",
    "excitement",
    "nostalgia",
    "inspiration",
    "humor",
    "controversy",
]


class ThumbnailAgent(BaseAgent):
    """
    Provides thumbnail strategy using CTR psychology and design principles.
    """

    def __init__(self):
        super().__init__("ThumbnailAgent")

    def generate_thumbnail_strategy(
        self,
        topic: str,
        target_emotion: str = "curiosity",
        football_mode: bool = False,
    ) -> dict:
        """
        Generate complete thumbnail strategy for a YouTube Short.

        Args:
            topic: Video topic.
            target_emotion: Primary emotion to trigger (see EMOTION_TARGETS).
            football_mode: Enable football-specific thumbnail concepts.

        Returns:
            dict with thumbnail concepts, colors, composition, and psychology.
        """
        logger.info(f"Generating thumbnail strategy for: '{topic}' | Emotion: {target_emotion}")

        system, prompt = thumbnail_prompt(topic, target_emotion, football_mode)
        result = self.call_and_parse(system, prompt, "Thumbnail Intelligence")

        if not result.get("error") and "thumbnail_concepts" in result:
            logger.info(f"Generated {len(result['thumbnail_concepts'])} thumbnail concepts.")

        return result

    def get_best_concept(self, thumbnail_result: dict) -> dict:
        """Return the recommended thumbnail concept."""
        if thumbnail_result.get("error") or "thumbnail_concepts" not in thumbnail_result:
            return {}
        concepts = thumbnail_result["thumbnail_concepts"]
        best_idx = thumbnail_result.get("recommended_concept", 1) - 1
        if 0 <= best_idx < len(concepts):
            return concepts[best_idx]
        return concepts[0] if concepts else {}

    @staticmethod
    def available_emotions() -> list[str]:
        return EMOTION_TARGETS
