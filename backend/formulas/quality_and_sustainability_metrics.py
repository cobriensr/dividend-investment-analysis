import math
import numpy as np


# Cash Flow Quality Indicators
def free_cash_flow_margin(free_cash_flow: float, revenue: float) -> float:
    return free_cash_flow / revenue


def free_cash_flow_conversion_rate(free_cash_flow: float, ebitda: float) -> float:
    return free_cash_flow / ebitda


def quality_of_earnings_ratio(operating_cash_flow: float, net_income: float) -> float:
    return operating_cash_flow / net_income


def accruals_ratio(
    net_income: float, operating_cash_flow: float, average_total_assets: float
) -> float:
    return (net_income - operating_cash_flow) / average_total_assets


# Balance Sheet Strength
def debt_to_capital_ratio(total_debt: float, shareholders_equity: float) -> float:
    return total_debt / (total_debt + shareholders_equity)


def net_debt_to_ebitda(total_debt: float, cash: float, ebitda: float) -> float:
    net_debt = total_debt - cash
    return net_debt / ebitda


def interest_coverage_ratio(ebit: float, interest_expense: float) -> float:
    return ebit / interest_expense


# Return on Capital Metrics
def return_on_invested_capital(
    net_operating_profit_after_tax: float, invested_capital: float
) -> float:
    return net_operating_profit_after_tax / invested_capital


def return_on_equity(net_income: float, shareholders_equity: float) -> float:
    return net_income / shareholders_equity


def sustainable_growth_rate(
    return_on_equity: float, dividend_payout_ratio: float
) -> float:
    retention_ratio = 1 - dividend_payout_ratio
    return return_on_equity * retention_ratio


# Economic Moat Assessment


def calculate_moat_score(
    roic_10_year: list,
    gross_margins_5_year: list,
    market_share: float,
    customer_retention: float,
    intangible_assets: float,
    market_cap: float,
    user_growth_rate: float,
    cost_growth_rate: float,
) -> dict:

    score = 0
    components = {}

    # 1. ROIC Persistence (20 points)
    if len(roic_10_year) >= 5:
        roic_std = np.std(roic_10_year)
        if roic_std < 0.05:  # Less than 5% standard deviation
            components["roic_persistence"] = 20
        else:
            components["roic_persistence"] = max(0, 20 - (roic_std * 200))
        score += components["roic_persistence"]

    # 2. ROIC Level (20 points)
    avg_roic = np.mean(roic_10_year) if roic_10_year else 0
    if avg_roic > 0.15:  # >15%
        components["roic_level"] = 20
    else:
        components["roic_level"] = max(0, (avg_roic / 0.15) * 20)
    score += components["roic_level"]

    # 3. Gross Margin Stability (15 points)
    if len(gross_margins_5_year) >= 3:
        margin_std = np.std(gross_margins_5_year)
        if margin_std < 0.02:  # Less than 2% standard deviation
            components["margin_stability"] = 15
        else:
            components["margin_stability"] = max(0, 15 - (margin_std * 500))
        score += components["margin_stability"]

    # 4. Market Share (15 points)
    if market_share > 0.30:  # >30% market share
        components["market_share"] = 15
    else:
        components["market_share"] = (market_share / 0.30) * 15
    score += components["market_share"]

    # 5. Switching Costs (10 points)
    if customer_retention > 0.90:  # >90% retention
        components["switching_costs"] = 10
    else:
        components["switching_costs"] = max(0, (customer_retention - 0.5) * 25)
    score += components["switching_costs"]

    # 6. Intangible Assets (10 points)
    intangible_ratio = intangible_assets / market_cap if market_cap > 0 else 0
    if intangible_ratio > 0.3:
        components["intangible_assets"] = 10
    else:
        components["intangible_assets"] = (intangible_ratio / 0.3) * 10
    score += components["intangible_assets"]

    # 7. Network Effects (10 points)
    if cost_growth_rate > 0:
        network_effect_ratio = (user_growth_rate**2) / cost_growth_rate
        if network_effect_ratio > 2:
            components["network_effects"] = 10
        else:
            components["network_effects"] = min(10, (network_effect_ratio / 2) * 10)
    else:
        components["network_effects"] = 0
    score += components["network_effects"]

    # Determine moat rating
    if score >= 70:
        moat_rating = "Wide Moat"
    elif score >= 40:
        moat_rating = "Narrow Moat"
    else:
        moat_rating = "No Moat"

    return {"total_score": score, "moat_rating": moat_rating, "components": components}


def persistence_rate(roic_history: list) -> float:
    if len(roic_history) < 2:
        return 0.5  # Default to medium persistence

    # Method 1: Simple correlation between consecutive years
    correlations = []
    for i in range(len(roic_history) - 1):
        if roic_history[i] > 0 and roic_history[i + 1] > 0:
            persistence = min(roic_history[i + 1] / roic_history[i], 1.0)
            correlations.append(persistence)

    if correlations:
        return sum(correlations) / len(correlations)
    return 0.5


def fade_rate(roic: float, wacc: float, persistence_rate: float) -> float:
    excess_return = roic - wacc
    if excess_return <= 0:
        return 1.0  # No excess returns to fade

    fade_rate = 1 - persistence_rate
    return fade_rate


def competitive_advantage_period_enhanced(
    roic: float, wacc: float, persistence_rate: float = 0.7
) -> float:

    if roic <= wacc:
        return 0  # No competitive advantage

    if persistence_rate >= 1:
        return float("inf")  # Permanent competitive advantage (unrealistic)

    # CAP = -ln(threshold) / ln(persistence_rate)
    # Where threshold is the minimum meaningful excess return (typically 0.1 or 10% of original excess)
    threshold = 0.1
    cap = (
        -math.log(threshold) / math.log(persistence_rate) if persistence_rate > 0 else 0
    )

    return min(cap, 30)  # Cap at 30 years for practical purposes
