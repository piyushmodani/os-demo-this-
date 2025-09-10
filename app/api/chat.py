from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.portfolio import fetch_user_portfolio
from app.services.fuzzy import derive_risk_profile_and_allocation
from app.clients.openai_client import generate_advice


router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for /chat endpoint."""
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, max_length=4000, description="User's question or prompt")


class ChatResponse(BaseModel):
    """Response body for /chat endpoint."""
    mentor_response: str
    risk_profile: str
    allocation: Dict[str, float]
    disclaimer: str


DISCLAIMER_TEXT = (
    "This conversation provides educational information only and is not financial, investment, or tax advice. "
    "Consider your personal circumstances and consult a licensed financial professional before making decisions."
)


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Accepts a user's message, fetches dummy portfolio data, applies fuzzy logic rules to
    determine a risk profile and target allocation, sends context + message to the LLM, and
    returns a mentor-style response with a disclaimer.
    """
    try:
        # 1) Fetch (simulated) portfolio data for the user
        portfolio = await fetch_user_portfolio(user_id=payload.user_id)

        # 2) Apply fuzzy logic to derive risk profile and a target allocation
        risk_profile, target_allocation, reasoning = derive_risk_profile_and_allocation(portfolio)

        # 3) Build concise context for the model
        context = _build_context(portfolio=portfolio, risk_profile=risk_profile, allocation=target_allocation, reasoning=reasoning)

        # 4) Ask the model for advice using the context and user's message
        model_reply = await generate_advice(context=context, user_message=payload.message)

        # 5) Append disclaimer to the mentor response
        mentor_with_disclaimer = f"{model_reply}\n\n— {DISCLAIMER_TEXT}"

        return ChatResponse(
            mentor_response=mentor_with_disclaimer,
            risk_profile=risk_profile,
            allocation=target_allocation,
            disclaimer=DISCLAIMER_TEXT,
        )
    except HTTPException:
        # Re-raise explicit HTTP errors unmodified
        raise
    except Exception as exc:  # pylint: disable=broad-except
        # Hide internal details from the client
        raise HTTPException(status_code=500, detail="Unexpected error while generating advice.") from exc


def _build_context(portfolio: Dict[str, Any], risk_profile: str, allocation: Dict[str, float], reasoning: str) -> str:
    """Create a compact, readable context string for the model."""
    total_value = sum(h.get("value", 0.0) for h in portfolio.get("holdings", [])) or 0.0

    lines = [
        "You are an AI financial mentor who explains clearly and concisely.",
        "Provide practical, implementable guidance tailored to the user's profile.",
        "Avoid giving tax, legal, or personalized investment advice.",
        "If uncertain, state assumptions and suggest what information would help.",
        "",
        f"User profile: age={portfolio.get('age')}, horizon_years={portfolio.get('time_horizon_years')}, risk_tolerance={portfolio.get('risk_tolerance')}",
        f"Monthly contribution: {portfolio.get('contributions_per_month')}",
        f"Current portfolio value: {round(total_value, 2)}",
        "Holdings (symbol | class | value):",
    ]

    for h in portfolio.get("holdings", []):
        lines.append(f"- {h.get('symbol')} | {h.get('asset_class')} | {h.get('value')}")

    lines.extend(
        [
            "",
            f"Fuzzy risk profile: {risk_profile}",
            f"Target allocation: {allocation}",
            f"Fuzzy reasoning: {reasoning}",
            "",
            "Respond in 4-8 concise sentences in a supportive, mentoring tone.",
        ]
    )

    return "\n".join(lines)