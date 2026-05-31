"""
ShortForge AI - Base Agent
All agents inherit from this class for consistent API interaction.
"""

import logging
import json
from typing import Optional
import anthropic

from config import config
from utils import parse_json_response, extract_text_from_content_blocks, build_error_response

logger = logging.getLogger("ShortForgeAI.BaseAgent")


class BaseAgent:
    """
    Base class for all ShortForge AI agents.
    Handles Anthropic API calls, response parsing, and error handling.
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
        self.model = config.app.anthropic_model
        self.max_tokens = config.app.max_tokens
        logger.info(f"Agent initialized: {agent_name}")

    def call_api(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = None,
    ) -> Optional[str]:
        """
        Call the Anthropic API and return raw text response.
        """
        temp = temperature if temperature is not None else config.app.temperature
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            raw_text = extract_text_from_content_blocks(response.content)
            logger.debug(f"[{self.agent_name}] API call successful. Tokens used: {response.usage.output_tokens}")
            return raw_text
        except anthropic.AuthenticationError:
            logger.error(f"[{self.agent_name}] Invalid API key.")
            raise
        except anthropic.RateLimitError:
            logger.warning(f"[{self.agent_name}] Rate limit hit. Retry later.")
            raise
        except Exception as e:
            logger.error(f"[{self.agent_name}] API error: {e}")
            raise

    def call_and_parse(
        self,
        system_prompt: str,
        user_prompt: str,
        feature_name: str = None,
    ) -> dict:
        """
        Call API and parse JSON response. Returns error dict on failure.
        """
        feature = feature_name or self.agent_name
        try:
            raw = self.call_api(system_prompt, user_prompt)
            if not raw:
                return build_error_response(feature, "Empty response from API")
            parsed = parse_json_response(raw)
            if not parsed:
                return build_error_response(feature, "Could not parse JSON response")
            return parsed
        except Exception as e:
            return build_error_response(feature, str(e))
