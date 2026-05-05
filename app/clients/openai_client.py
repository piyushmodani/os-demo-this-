from __future__ import annotations

import os
from typing import Optional

from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


_client: Optional[AsyncOpenAI] = None


def _get_client() -> Optional[AsyncOpenAI]:
    """Instantiate the AsyncOpenAI client if an API key is available."""
    global _client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    if _client is None:
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def generate_advice(*, context: str, user_message: str) -> str:
    """
    Ask the OpenAI Chat Completions API for a response. If the API key is missing or
    the request fails, return a deterministic heuristic fallback so the endpoint remains usable.
    """
    client = _get_client()

    system_prompt = (
        "You are an experienced but cautious AI financial mentor. "
        "Be supportive, clear, and concise. Avoid deterministic guarantees."
    )

    if client is None:
        return _fallback_response(context=context, user_message=user_message)

    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.4,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"},
            ],
        )
        choice = response.choices[0]
        return choice.message.content or _fallback_response(context=context, user_message=user_message)
    except Exception:
        return _fallback_response(context=context, user_message=user_message)


def _fallback_response(*, context: str, user_message: str) -> str:
    """
    Simple, deterministic template used when the OpenAI API is not available.
    It references the provided context and gives conservative, general guidance.
    """
    # Use a very small truncation to keep responses brief in fallback
    snippet = (user_message or "").strip()
    if len(snippet) > 160:
        snippet = snippet[:157] + "..."

    return (
        "Based on your profile and current allocation, consider aligning with the suggested target mix. "
        "Focus on broad diversification, low costs, and periodic rebalancing. "
        "Keep an emergency fund in cash and increase contributions when feasible. "
        f"Regarding your question: '{snippet}', prioritize long-term discipline over short-term moves."
    )