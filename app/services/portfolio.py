from __future__ import annotations

from typing import Dict, Any, List


async def fetch_user_portfolio(user_id: str) -> Dict[str, Any]:
    """
    Simulate fetching a user's portfolio from the database.

    For now, we return deterministic dummy data keyed by the user_id so you can
    test different cases quickly without a database. In a real implementation,
    this would perform an async DB query.
    """
    # Simple switch for different demo personas
    if user_id.endswith("-conservative"):
        return _build_portfolio(
            age=62,
            time_horizon_years=5,
            risk_tolerance="low",
            holdings=[
                {"symbol": "BND", "asset_class": "Bonds", "value": 65000.0},
                {"symbol": "CASH", "asset_class": "Cash", "value": 15000.0},
                {"symbol": "AAPL", "asset_class": "Stocks", "value": 20000.0},
            ],
        )

    if user_id.endswith("-aggressive"):
        return _build_portfolio(
            age=28,
            time_horizon_years=30,
            risk_tolerance="high",
            holdings=[
                {"symbol": "VTI", "asset_class": "Stocks", "value": 70000.0},
                {"symbol": "QQQ", "asset_class": "Stocks", "value": 25000.0},
                {"symbol": "CASH", "asset_class": "Cash", "value": 5000.0},
            ],
        )

    # Default to a balanced profile
    return _build_portfolio(
        age=40,
        time_horizon_years=15,
        risk_tolerance="medium",
        holdings=[
            {"symbol": "VTI", "asset_class": "Stocks", "value": 55000.0},
            {"symbol": "VXUS", "asset_class": "Stocks", "value": 15000.0},
            {"symbol": "BND", "asset_class": "Bonds", "value": 25000.0},
            {"symbol": "CASH", "asset_class": "Cash", "value": 5000.0},
        ],
    )


def _build_portfolio(
    *,
    age: int,
    time_horizon_years: int,
    risk_tolerance: str,
    holdings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Helper to assemble a portfolio dict consistently."""
    return {
        "user_id": "demo",
        "age": age,
        "time_horizon_years": time_horizon_years,
        "risk_tolerance": risk_tolerance,  # one of: low, medium, high
        "contributions_per_month": 1000.0,
        "holdings": holdings,
    }