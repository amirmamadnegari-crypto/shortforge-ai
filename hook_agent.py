"""
ShortForge AI - Hook Generator Agent
Generates 10 attention-grabbing hooks optimized for first 3 seconds.
"""

import logging
from agents.base_agent import BaseAgent
from prompts import hook_generator_prompt

logger = logging.getLogger("ShortForgeAI.HookAgent")


HOOK_STYLES = [
    "general",
    "shocking",
    "controversial",
    "storytelling",
    "question-based",
    "listicle",
    "emotional",
    "humor",
]


class HookAgent(BaseAgent):
    """
    Generates high-retention YouTube Shorts hooks.
    Each hook is scored and categorized by psychological trigger.
    """

    def __init__(self):
        super().__init__("HookAgent")

    def generate_hooks(
        self,
        topic: str,
        style: str = "general",
        football_mode: bool = False,
    ) -> dict:
        """
        Generate 10 viral hooks for the given topic.

        Args:
            topic: The topic/title of the Short.
            style: Preferred hook style (see HOOK_STYLES).
            football_mode: Enable football-specific hooks.

        Returns:
            dict with hooks list and metadata.
        """
        logger.info(f"Generating hooks for: '{topic}' | Style: {style}")

        system, prompt = hook_generator_prompt(topic, style, football_mode)
        result = self.call_and_parse(system, prompt, "Hook Generator")

        if not result.get("error") and "hooks" in result:
            # Sort by retention score
            result["hooks"] = sorted(
                result["hooks"],
                key=lambda x: x.get("retention_score", 0),
                reverse=True,
            )
            logger.info(f"Generated {len(result['hooks'])} hooks.")

        return result

    def get_best_hook(self, hooks_result: dict) -> dict:
        """Return the highest-scored hook."""
        if hooks_result.get("error") or "hooks" not in hooks_result:
            return {}
        hooks = hooks_result["hooks"]
        return hooks[0] if hooks else {}

    @staticmethod
    def available_styles() -> list[str]:
        return HOOK_STYLES
