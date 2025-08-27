# Yield Based Valuation
def relative_dividend_yield(
    current_yield: float, historical_average_yield: float
) -> float:
    return current_yield / historical_average_yield


def yield_spread_analysis(
    dividend_yield: float, ten_year_treasury_yield: float
) -> float:
    return dividend_yield - ten_year_treasury_yield


def sector_relative_yield(
    stock_dividend_yield: float, sector_average_yield: float
) -> float:
    return stock_dividend_yield / sector_average_yield


# Dividend Adjusted Ratios
def pegy_ratio(
    pe_ratio: float, expected_growth_rate: float, dividend_yield: float
) -> float:
    return pe_ratio / (expected_growth_rate + dividend_yield)


def dividend_adjusted_pe(pe_ratio: float, dividend_yield: float) -> float:
    return pe_ratio * (1 + dividend_yield)


def price_to_dividend_ratio(
    current_share_price: float, annual_dividend: float
) -> float:
    return current_share_price / annual_dividend
