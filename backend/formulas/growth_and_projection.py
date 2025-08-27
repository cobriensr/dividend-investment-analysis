# Growth Rate Calculations
def simple_annual_growth_rate(
    current_dividend: float, prior_year_dividend: float
) -> float:
    return ((current_dividend - prior_year_dividend) / prior_year_dividend) * 100


def compound_annual_growth_rate(
    ending_dividend: float, beginning_dividend: float, years: int
) -> float:
    return (ending_dividend / beginning_dividend) ** (1 / years) - 1


def weighted_average_growth_rate(
    growth_rates: list[float], weights: list[int]
) -> float:
    if len(growth_rates) != len(weights):
        raise ValueError("Growth rates and weights lists must have the same length.")

    weighted_sum = sum(gr * w for gr, w in zip(growth_rates, weights))
    sum_of_weights = sum(weights)

    if sum_of_weights == 0:
        raise ZeroDivisionError("Sum of weights cannot be zero.")

    return weighted_sum / sum_of_weights


# Dividend Discount Models
def gordon_growth_model(
    next_period_dividend: float, required_return: float, growth_rate: float
) -> float:
    if required_return <= growth_rate:
        raise ValueError("Required return must be greater than growth rate.")
    return next_period_dividend / (required_return - growth_rate)


def two_stage_dividend_discount_model(
    initial_dividend: float,
    initial_growth_rate: float,
    stable_growth_rate: float,
    required_return: float,
    initial_periods: int,
) -> float:
    if required_return <= stable_growth_rate:
        raise ValueError("Required return must be greater than stable growth rate.")

    # Calculate the present value of dividends during the initial growth period
    pv_initial_dividends = sum(
        initial_dividend * (1 + initial_growth_rate) ** t / (1 + required_return) ** t
        for t in range(1, initial_periods + 1)
    )

    # Calculate the present value of the terminal value
    terminal_value = (
        initial_dividend * (1 + initial_growth_rate) ** initial_periods
    ) / (required_return - stable_growth_rate)
    pv_terminal_value = terminal_value / (1 + required_return) ** initial_periods

    return pv_initial_dividends + pv_terminal_value


def three_stage_dividend_discount_model(
    initial_dividend: float,
    initial_growth_rate: float,
    stable_growth_rate: float,
    required_return: float,
    initial_periods: int,
    transition_periods: int,
) -> float:
    if required_return <= stable_growth_rate:
        raise ValueError("Required return must be greater than stable growth rate.")

    # Calculate the present value of dividends during the initial growth period
    pv_initial_dividends = sum(
        initial_dividend * (1 + initial_growth_rate) ** t / (1 + required_return) ** t
        for t in range(1, initial_periods + 1)
    )

    # Calculate the present value of dividends during the transition period
    pv_transition_dividends = sum(
        initial_dividend
        * (1 + initial_growth_rate) ** initial_periods
        * (1 + stable_growth_rate) ** t
        / (1 + required_return) ** (initial_periods + t)
        for t in range(1, transition_periods + 1)
    )

    # Calculate the present value of the terminal value
    terminal_value = (
        initial_dividend
        * (1 + initial_growth_rate) ** initial_periods
        * (1 + stable_growth_rate) ** transition_periods
    ) / (required_return - stable_growth_rate)
    pv_terminal_value = terminal_value / (1 + required_return) ** (
        initial_periods + transition_periods
    )

    return pv_initial_dividends + pv_transition_dividends + pv_terminal_value


# Yield on Cost Projections
def current_yield_on_cost(
    current_annual_dividend: float, original_cost_basis: float
) -> float:
    return current_annual_dividend / original_cost_basis


def projected_yield_on_cost(
    current_annual_dividend: float,
    original_cost_basis: float,
    years: int,
    growth_rate: float,
) -> float:
    future_dividend = current_annual_dividend * (1 + growth_rate) ** years
    return future_dividend / original_cost_basis


def chowder_number(
    current_dividend_yield: float, five_year_dividend_growth_rate: float
) -> float:
    return current_dividend_yield + five_year_dividend_growth_rate
