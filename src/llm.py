"""Provider-agnostic LLM wrapper with token accounting.

Supports two backends behind one interface:
  * groq      — OpenAI-compatible API serving open models (Llama, etc.). Fast and cheap.
  * anthropic — Claude models.

The active provider is chosen in config (auto-detected from whichever API key is present), so the
rest of the codebase never branches on provider — it just calls `get_llm().complete(...)`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import get_settings


class LLMNotConfigured(RuntimeError):
    """Raised when an LLM call is attempted with no provider key configured."""


@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


class LLMClient:
    """Lazily constructs the underlying SDK client so importing this module never needs a key."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = None
        self._provider = None

    def _ensure_client(self):
        if self._client is not None:
            return self._client

        provider = self._settings.provider
        if provider == "groq":
            if not self._settings.groq_api_key:
                raise LLMNotConfigured("GROQ_API_KEY is not set. Add it to .env or export it.")
            from groq import Groq

            self._client = Groq(api_key=self._settings.groq_api_key)
        elif provider == "anthropic":
            if not self._settings.anthropic_api_key:
                raise LLMNotConfigured("ANTHROPIC_API_KEY is not set. Add it to .env or export it.")
            from anthropic import Anthropic

            self._client = Anthropic(api_key=self._settings.anthropic_api_key)
        else:
            raise LLMNotConfigured(
                "No LLM provider configured. Set GROQ_API_KEY (Groq) or ANTHROPIC_API_KEY (Claude) "
                "in .env. See .env.example."
            )

        self._provider = provider
        return self._client

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 0.0,
    ) -> LLMResult:
        client = self._ensure_client()
        system = system or "You are a precise, helpful assistant."
        max_tokens = max_tokens or self._settings.max_tokens

        if self._provider == "groq":
            model = model or self._settings.groq_answer_model
            resp = client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )
            return LLMResult(
                text=resp.choices[0].message.content or "",
                input_tokens=resp.usage.prompt_tokens,
                output_tokens=resp.usage.completion_tokens,
                model=model,
            )

        # anthropic
        model = model or self._settings.answer_model
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in resp.content if block.type == "text")
        return LLMResult(
            text=text,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            model=model,
        )


_client: LLMClient | None = None


def get_llm() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
