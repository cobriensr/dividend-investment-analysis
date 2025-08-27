# Total Return Calculations
import numpy as np

risk_free_rate = 0.043  # 10 year treasury yield
expected_market_return = 0.10


# Convert annual risk-free rate to daily if your returns are daily
def daily_risk_free_rate(annual_risk_free_rate: float) -> float:
    return (1 + annual_risk_free_rate) ** (1 / 252) - 1


def total_return(
    ending_price: float, beginning_price: float, dividends: float
) -> float:
    return (ending_price - beginning_price + dividends) / beginning_price


def annualized_return(
    ending_price: float, beginning_price: float, dividends: float, years: float
) -> float:
    total = total_return(ending_price, beginning_price, dividends)
    return (1 + total) ** (1 / years) - 1


def weighted_average_cost_of_capital(
    risk_free_rate: float,
    beta: float,
    expected_market_return: float,
    interest_expense: float,
    total_debt: float,
    shares_outstanding: float,
    stock_price: float,
    income_tax_expense: float,
    pre_tax_income: float,
) -> float:
    # Cost of Equity using CAPM
    equity_risk_premium = expected_market_return - risk_free_rate
    cost_of_equity = risk_free_rate + beta * equity_risk_premium

    # Cost of Debt
    cost_of_debt = interest_expense / total_debt if total_debt > 0 else 0

    # Market Values
    market_value_of_equity = shares_outstanding * stock_price
    market_value_of_debt = total_debt  # Book value approximation
    total_value = market_value_of_equity + market_value_of_debt

    # Tax Rate
    effective_tax_rate = (
        income_tax_expense / pre_tax_income if pre_tax_income > 0 else 0.21
    )  # Default to 21% corporate rate

    # WACC Calculation
    if total_value > 0:
        equity_weight = market_value_of_equity / total_value
        debt_weight = market_value_of_debt / total_value
        wacc = (equity_weight * cost_of_equity) + (
            debt_weight * cost_of_debt * (1 - effective_tax_rate)
        )
    else:
        wacc = cost_of_equity  # If no debt, WACC = Cost of Equity

    return wacc


# Risk-Adjusted Performance
def sharpe_ratio(
    portfolio_return: float, risk_free_rate: float, standard_deviation: float
) -> float:
    excess_return = portfolio_return - risk_free_rate
    return excess_return / standard_deviation if standard_deviation != 0 else 0


def downside_deviation(returns: list, target_return: float = 0) -> float:
    # Filter only returns below target
    downside_returns = [r for r in returns if r < target_return]

    if not downside_returns:
        return 0  # No downside risk

    # Calculate downside deviations
    downside_deviations = [(r - target_return) ** 2 for r in downside_returns]

    # Calculate downside deviation
    n = len(returns)  # Use total number of returns, not just downside
    downside_variance = sum(downside_deviations) / n
    downside_deviation = np.sqrt(downside_variance)

    return downside_deviation


def sortino_ratio(
    returns: list, risk_free_rate: float, target_return: float = None
) -> float:
    """
    Corrected Sortino ratio calculation.
    """
    import numpy as np

    if target_return is None:
        target_return = risk_free_rate

    avg_return = np.mean(returns)
    excess_return = avg_return - risk_free_rate

    downside_deviation = downside_deviation(returns, target_return)

    if downside_deviation == 0:
        return float("inf") if excess_return > 0 else 0

    return excess_return / downside_deviation


def treynor_ratio(portfolio_return: float, risk_free_rate: float, beta: float) -> float:
    excess_return = portfolio_return - risk_free_rate
    return excess_return / beta if beta != 0 else 0
