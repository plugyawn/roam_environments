"""Chat completion client wired to Cerebras OpenAI-compatible endpoint."""

from __future__ import annotations

import os

from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

from ..config import RuntimeConfig


class CerebrasModelClient(OpenAIChatCompletionClient):
    """OpenAIChatCompletionClient configured for Cerebras-hosted models."""

    def __init__(self, config: RuntimeConfig) -> None:
        api_key = os.environ.get("CEREBRAS_API_KEY")
        if not api_key:
            raise RuntimeError("CEREBRAS_API_KEY is not set")

        model_info = {
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": ModelFamily.UNKNOWN,
            "multiple_system_messages": True,
        }

        super().__init__(
            model=config.model.model_name,
            base_url=config.model.base_url,
            api_key=api_key,
            timeout=config.model.request_timeout,
            temperature=config.model.temperature,
            max_tokens=config.model.max_output_tokens,
            model_info=model_info,
        )
