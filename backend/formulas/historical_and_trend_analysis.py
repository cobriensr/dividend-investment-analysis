# Dividend Consistency Metrics
def classify_dividend_stocks(years_of_dividends_paid: int) -> str:
    if years_of_dividends_paid >= 50:
        return "King"
    elif years_of_dividends_paid >= 25:
        return "Champion"
    elif years_of_dividends_paid >= 10:
        return "Contender"
    elif years_of_dividends_paid >= 5:
        return "Challenger"
    else:
        return "N/A"


def payment_volatility_analysis(dividend_payments: list) -> float:
    if len(dividend_payments) < 2:
        return 0.0
    mean_payment = sum(dividend_payments) / len(dividend_payments)
    variance = sum((x - mean_payment) ** 2 for x in dividend_payments) / (
        len(dividend_payments) - 1
    )
    return variance**0.5


def recession_performance_score(
    dividend_history: list, recession_period: list
) -> float:
    if not dividend_history or not recession_period:
        return 0.0
    recession_dividends = [
        dividend for date, dividend in dividend_history if date in recession_period
    ]
    if not recession_dividends:
        return 0.0
    return sum(recession_dividends) / len(recession_dividends)


# Growth Trend Analysis
def dividend_growth_velocity(
    current_growth_rate: float, previous_growth_rate: float
) -> float:
    if previous_growth_rate == 0:
        return float("inf") if current_growth_rate > 0 else float("-inf")
    return current_growth_rate - previous_growth_rate


# Implemenatation Framework
# Professional Screening Process
# Systematic approach for spreadsheet implementation:
# Phase 1: Safety Screening

# FCF payout ratio <80%
# Debt/EBITDA <3.0x
# Interest coverage >3.0x
# Dividend coverage >1.5x Simply Safe Dividends

# Phase 2: Quality Assessment

# ROIC >12%
# ROE >15%
# Positive free cash flow
# Earnings quality ratio >1.0

# Phase 3: Growth Analysis

# 5-year dividend CAGR >3%
# Sustainable growth rate positive
# Payout ratio allows growth

# Phase 4: Valuation Screens

# Relative yield >1.0x historical
# PEGY ratio <1.5
# Reasonable P/E for sector
