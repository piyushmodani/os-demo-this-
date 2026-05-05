from __future__ import annotations

from typing import Dict, Any, Tuple


def derive_risk_profile_and_allocation(portfolio: Dict[str, Any]) -> Tuple[str, Dict[str, float], str]:
    """
    Use simple, transparent fuzzy-style rules to infer a risk profile and target allocation.

    Inputs considered:
    - age
    - time horizon
    - stated risk tolerance (low/medium/high)
    - current stocks/bonds/cash mix

    Outputs:
    - risk_profile: one of {"Conservative", "Balanced", "Aggressive"}
    - allocation: target % weights across Stocks, Bonds, Cash (summing to 100)
    - reasoning: short explanation of how the decision was made
    """
    age = int(portfolio.get("age", 40))
    horizon = int(portfolio.get("time_horizon_years", 10))
    stated = str(portfolio.get("risk_tolerance", "medium")).lower()

    # Compute current high-level allocation to inform recommendations
    current = _summarize_current_allocation(portfolio)

    # Fuzzy scoring: combine age, horizon, and stated tolerance
    score = 0

    # Younger and long horizon push towards aggressive
    if age < 35:
        score += 2
    elif age < 50:
        score += 1
    else:
        score -= 1

    if horizon >= 20:
        score += 2
    elif horizon >= 10:
        score += 1
    else:
        score -= 1

    # Stated tolerance
    if stated in {"high", "aggressive"}:
        score += 2
    elif stated in {"medium", "balanced"}:
        score += 0
    else:
        score -= 2

    # Map score to profile
    if score >= 3:
        profile = "Aggressive"
        target = {"Stocks": 85.0, "Bonds": 10.0, "Cash": 5.0}
    elif score <= -1:
        profile = "Conservative"
        target = {"Stocks": 35.0, "Bonds": 55.0, "Cash": 10.0}
    else:
        profile = "Balanced"
        target = {"Stocks": 60.0, "Bonds": 35.0, "Cash": 5.0}

    reasoning = (
        f"Age={age}, horizon={horizon}y, stated tolerance='{stated}' -> score={score}. "
        f"Current mix (Stocks={current['Stocks']}%, Bonds={current['Bonds']}%, Cash={current['Cash']}%) informs rebalancing pace."
    )

    return profile, target, reasoning


def _summarize_current_allocation(portfolio: Dict[str, Any]) -> Dict[str, float]:
    """Aggregate holdings into Stocks/Bonds/Cash allocation percentages."""
    totals = {"Stocks": 0.0, "Bonds": 0.0, "Cash": 0.0}
    holdings = portfolio.get("holdings", [])
    total_value = sum(h.get("value", 0.0) for h in holdings) or 1.0

    for h in holdings:
        asset_class = str(h.get("asset_class", "")).title()
        value = float(h.get("value", 0.0))
        if asset_class not in totals:
            # Map any unknown classes to Stocks by default (e.g., ETFs holding equities)
            asset_class = "Stocks"
        totals[asset_class] += value

    return {k: round(v / total_value * 100.0, 2) for k, v in totals.items()}