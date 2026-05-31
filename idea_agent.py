"""
ShortForge AI - Viral Idea Generator Agent
Generates 20 scored viral YouTube Shorts ideas from a topic.
"""

import logging
from typing import Optional
from agents.base_agent import BaseAgent
from prompts import idea_generator_prompt
from config import config

logger = logging.getLogger("ShortForgeAI.IdeaAgent")


class IdeaAgent(BaseAgent):
    """
    Generates viral YouTube Shorts ideas with scores and rationale.
    Supports Football Creator Mode for football-specific content.
    """

    def __init__(self):
        super().__init__("IdeaAgent")

    def generate_ideas(
        self,
        topic: str,
        football_mode: bool = False,
    ) -> dict:
        """
        Generate viral YouTube Shorts ideas for the given topic.

        Args:
            topic: The niche/topic/keyword to generate ideas for.
            football_mode: Enable football-specific idea generation.

        Returns:
            dict with ideas list and metadata.
        """
        logger.info(f"Generating ideas for: '{topic}' | Football mode: {football_mode}")

        football_cfg = config.football if football_mode else None
        system, prompt = idea_generator_prompt(topic, football_mode, football_cfg)

        result = self.call_and_parse(system, prompt, "Viral Idea Generator")

        if not result.get("error") and "ideas" in result:
            # Sort by viral score descending (LLM should already do this, but enforce it)
            result["ideas"] = sorted(
                result["ideas"],
                key=lambda x: x.get("viral_score", 0),
                reverse=True
            )
            logger.info(f"Generated {len(result['ideas'])} ideas. Top score: {result['ideas'][0].get('viral_score', 'N/A')}")

        return result

    def get_top_ideas(self, ideas_result: dict, top_n: int = 5) -> list:
        """Extract top N ideas from result."""
        if ideas_result.get("error") or "ideas" not in ideas_result:
            return []
        return ideas_result["ideas"][:top_n]

    def filter_by_score(self, ideas_result: dict, min_score: int = None) -> list:
        """Filter ideas by minimum viral score."""
        min_s = min_score or config.content.min_viral_score
        if ideas_result.get("error") or "ideas" not in ideas_result:
            return []
        return [i for i in ideas_result["ideas"] if i.get("viral_score", 0) >= min_s]
