"""
ShortForge AI - Script Generator Agent
Generates complete 30-60 second YouTube Shorts scripts with all 4 sections.
"""

import logging
from agents.base_agent import BaseAgent
from prompts import script_generator_prompt

logger = logging.getLogger("ShortForgeAI.ScriptAgent")


SCRIPT_TONES = [
    "energetic",
    "calm-authoritative",
    "storytelling",
    "humorous",
    "dramatic",
    "educational",
    "inspirational",
    "controversial",
]


class ScriptAgent(BaseAgent):
    """
    Generates production-ready YouTube Shorts scripts.
    Includes hook, main story, curiosity loop, and call to action.
    """

    def __init__(self):
        super().__init__("ScriptAgent")

    def generate_script(
        self,
        topic: str,
        hook: str = "",
        tone: str = "energetic",
        football_mode: bool = False,
    ) -> dict:
        """
        Generate a complete YouTube Shorts script.

        Args:
            topic: Video topic/title.
            hook: Opening hook line (can be from HookAgent).
            tone: Delivery tone (see SCRIPT_TONES).
            football_mode: Enable football-specific scripting.

        Returns:
            dict with full script structure and metadata.
        """
        logger.info(f"Generating script for: '{topic}' | Tone: {tone}")

        system, prompt = script_generator_prompt(topic, hook, tone, football_mode)
        result = self.call_and_parse(system, prompt, "Script Generator")

        if not result.get("error"):
            duration = result.get("estimated_duration_seconds", 0)
            logger.info(f"Script generated. Estimated duration: {duration}s")

        return result

    def get_readable_script(self, script_result: dict) -> str:
        """Extract the full readable script text."""
        if script_result.get("error"):
            return "Error generating script."
        return script_result.get("full_script_readable", "")

    def get_script_sections(self, script_result: dict) -> dict:
        """Extract the 4 script sections."""
        if script_result.get("error") or "script" not in script_result:
            return {}
        return script_result["script"]

    @staticmethod
    def available_tones() -> list[str]:
        return SCRIPT_TONES
