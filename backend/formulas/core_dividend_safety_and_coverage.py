# Basic Yield Calculations
def current_dividend_yield(
    annual_dividend_per_share: float, current_price: float
) -> float:
    return (annual_dividend_per_share / current_price) * 100


def trailing_twelve_months_dividend_yield(
    sum_of_last_4_quarters_dividends: float, current_price: float
) -> float:
    return (sum_of_last_4_quarters_dividends / current_price) * 100


def forward_dividend_yield(
    projected_annual_dividend: float, current_price: float
) -> float:
    return (projected_annual_dividend / current_price) * 100


# Dividend Coverage Ratios
def earnings_coverage_ratio(
    earnings_per_share: float, dividend_per_share: float
) -> float:
    return earnings_per_share / dividend_per_share


def free_cash_flow_coverage(
    free_cash_flow: float, total_dividends_paid: float
) -> float:
    return free_cash_flow / total_dividends_paid


def cash_flow_from_operations_coverage(
    operating_cash_flow: float, total_dividends_paid: float
) -> float:
    return operating_cash_flow / total_dividends_paid


def free_cash_flow_to_equity_coverage(
    cash_flow_from_operations: float,
    capital_expenditures: float,
    net_borrowing: float,
    interest_expense: float,
    tax_rate: float,
    total_dividends_paid: float,
    total_share_repurchases: float,
) -> float:
    fcfe = (
        cash_flow_from_operations
        - capital_expenditures
        + net_borrowing
        - interest_expense * (1 - tax_rate)
    )
    return fcfe / (total_dividends_paid + total_share_repurchases)


# Payout Ratios
def earnings_payout_ratio(
    dividend_per_share: float, earnings_per_share: float
) -> float:
    return (dividend_per_share / earnings_per_share) * 100


def free_cash_flow_payout_ratio(
    total_dividends_paid: float, free_cash_flow: float
) -> float:
    return (total_dividends_paid / free_cash_flow) * 100


def cash_dividend_payout_ratio(
    dividend_per_share: float, operating_cash_flow: float, preferred_dividends: float
) -> float:
    return dividend_per_share / (operating_cash_flow - preferred_dividends)
