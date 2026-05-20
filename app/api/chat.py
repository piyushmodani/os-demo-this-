from typing import Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.portfolio import fetch_user_portfolio


router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for /chat endpoint."""
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, max_length=4000, description="User's question or prompt")


class ChatSimpleResponse(BaseModel):
    """Simplified response containing the simulated portfolio and echo of the message."""
    portfolio: Dict[str, Any]
    message: str


@router.post("/chat", response_model=ChatSimpleResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatSimpleResponse:
    """
    Accepts a user's message, fetches dummy portfolio data, and returns it with the original message.
    No external calls or fuzzy logic are performed at this stage.
    """
    portfolio = await fetch_user_portfolio(user_id=payload.user_id)
    return ChatSimpleResponse(portfolio=portfolio, message=payload.message)