"""
ShortForge AI - SEO Generator Agent
Generates titles, descriptions, hashtags, and keywords for YouTube Shorts.
"""

import logging
from agents.base_agent import BaseAgent
from prompts import seo_generator_prompt

logger = logging.getLogger("ShortForgeAI.SEOAgent")


class SEOAgent(BaseAgent):
    """
    Generates full SEO packages to maximize YouTube discoverability.
    """

    def __init__(self):
        super().__init__("SEOAgent")

    def generate_seo(
        self,
        topic: str,
        script_summary: str = "",
        football_mode: bool = False,
    ) -> dict:
        """
        Generate complete SEO package for a YouTube Short.

        Args:
            topic: Video topic/keyword.
            script_summary: Optional script context for better SEO.
            football_mode: Enable football-specific SEO.

        Returns:
            dict with titles, description, hashtags, and keywords.
        """
        logger.info(f"Generating SEO for: '{topic}'")

        system, prompt = seo_generator_prompt(topic, script_summary, football_mode)
        result = self.call_and_parse(system, prompt, "SEO Generator")

        if not result.get("error"):
            titles_count = len(result.get("titles", []))
            hashtags = result.get("hashtags", {})
            total_tags = (
                len(hashtags.get("primary", [])) +
                len(hashtags.get("niche", [])) +
                len(hashtags.get("trending", []))
            )
            logger.info(f"SEO generated. Titles: {titles_count}, Hashtags: {total_tags}")

        return result

    def get_best_title(self, seo_result: dict) -> str:
        """Get the best recommended title."""
        if seo_result.get("error") or "titles" not in seo_result:
            return ""
        titles = seo_result["titles"]
        best_idx = seo_result.get("best_title", 1) - 1
        if 0 <= best_idx < len(titles):
            return titles[best_idx].get("title", "")
        return titles[0].get("title", "") if titles else ""

    def get_all_hashtags(self, seo_result: dict) -> list[str]:
        """Flatten and return all hashtags."""
        if seo_result.get("error") or "hashtags" not in seo_result:
            return []
        h = seo_result["hashtags"]
        return h.get("primary", []) + h.get("niche", []) + h.get("trending", [])
