"""
ShortForge AI - Growth Advisor Agent
Provides channel growth strategies, content pillars, and audience targeting.
Includes Viral Score System and Content Calendar.
"""

import logging
from agents.base_agent import BaseAgent
from prompts import viral_score_prompt, content_calendar_prompt, growth_advisor_prompt

logger = logging.getLogger("ShortForgeAI.GrowthAgent")


POSTING_FREQUENCIES = [
    "1x per day",
    "2x per day",
    "3x per day",
    "every other day",
    "5x per week",
]


class GrowthAgent(BaseAgent):
    """
    Provides viral scoring, content calendar, and channel growth strategy.
    """

    def __init__(self):
        super().__init__("GrowthAgent")

    def score_content(
        self,
        topic: str = "",
        hook: str = "",
        script_summary: str = "",
        title: str = "",
        football_mode: bool = False,
    ) -> dict:
        """
        Score content across 5 viral dimensions.

        Args:
            topic: Video topic.
            hook: Opening hook.
            script_summary: Script or summary.
            title: Proposed title.
            football_mode: Football mode flag.

        Returns:
            dict with viral score breakdown and recommendations.
        """
        logger.info(f"Scoring content for: '{topic}'")

        content_package = {
            "topic": topic,
            "hook": hook,
            "script_summary": script_summary,
            "title": title,
        }
        system, prompt = viral_score_prompt(content_package, football_mode)
        result = self.call_and_parse(system, prompt, "Viral Score System")

        if not result.get("error"):
            score = result.get("overall_viral_score", 0)
            grade = result.get("grade", "?")
            logger.info(f"Viral score: {score}/100 (Grade: {grade})")

        return result

    def generate_calendar(
        self,
        topic: str,
        posting_frequency: str = "1x per day",
        football_mode: bool = False,
    ) -> dict:
        """
        Generate a 30-day content calendar.

        Args:
            topic: Channel niche/topic.
            posting_frequency: How often to post.
            football_mode: Football mode flag.

        Returns:
            dict with weekly plans and strategy.
        """
        logger.info(f"Generating 30-day calendar for: '{topic}'")

        system, prompt = content_calendar_prompt(topic, posting_frequency, football_mode)
        return self.call_and_parse(system, prompt, "Content Calendar")

    def get_growth_advice(
        self,
        topic: str,
        current_subs: int = 0,
        football_mode: bool = False,
    ) -> dict:
        """
        Generate channel growth strategy.

        Args:
            topic: Channel niche.
            current_subs: Current subscriber count.
            football_mode: Football mode flag.

        Returns:
            dict with growth phases, content pillars, and audience targeting.
        """
        logger.info(f"Generating growth advice for: '{topic}' | Subs: {current_subs}")

        system, prompt = growth_advisor_prompt(topic, current_subs, football_mode)
        return self.call_and_parse(system, prompt, "Channel Growth Advisor")

    @staticmethod
    def available_frequencies() -> list[str]:
        return POSTING_FREQUENCIES
