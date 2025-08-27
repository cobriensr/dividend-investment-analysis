# REITs (Real Estate Invesment Trusts)
def funds_from_operations(
    net_income: float,
    depreciation: float,
    amortization: float,
    gains_on_asset_sales: float,
) -> float:
    return net_income + depreciation + amortization - gains_on_asset_sales


def adjusted_funds_from_operations(
    funds_from_operations: float,
    maintenance_capex: float,
    straight_line_rent_from_10k: float = None,
    rental_revenue: float = None,
) -> float:
    # Use reported straight-line rent if available, otherwise estimate
    if straight_line_rent_from_10k is not None:
        straight_line_rent_adjustments = straight_line_rent_from_10k
    elif rental_revenue is not None:
        # Industry standard: 2-3% of rental revenue
        straight_line_rent_adjustments = rental_revenue * 0.025
    else:
        # If no data available, assume zero
        straight_line_rent_adjustments = 0

    return funds_from_operations - maintenance_capex - straight_line_rent_adjustments


def net_asset_value_premium_or_discount(
    stock_price: float, nav_per_share: float, net_asset_value: float
) -> float:
    return ((stock_price - nav_per_share) / net_asset_value) * 100


def cash_available_for_distribution(
    adjusted_funds_from_operations: float, recurring_capex: float
) -> float:
    return adjusted_funds_from_operations - recurring_capex


# MLPs (Master Limited Partnerships)
def distributable_cash_flow(
    net_income: float, depreciation: float, maintenance_capex: float
) -> float:
    return net_income + depreciation - maintenance_capex


def incentive_distribution_rights_impact(
    distributable_cash_flow: float, incentive_distribution_rights: float
) -> float:
    return distributable_cash_flow - incentive_distribution_rights


# Utilities
def rate_base(
    net_plant_in_service: float, working_capital: float, deferred_taxes: float
) -> float:
    return net_plant_in_service + working_capital - deferred_taxes


def rate_base_growth(beginning_rate_base: float, ending_rate_base: float) -> float:
    # calculate the rate_base twice first for beginning and ending rate bases
    return (ending_rate_base - beginning_rate_base) / beginning_rate_base

def idr_impact(
    distributable_cash_flow_per_unit: float,
    tier_1_threshold: float = 0.50,
    tier_2_threshold: float = 0.60,
    tier_3_threshold: float = 0.75
) -> dict:
    """
    Standard IDR waterfall:
    - Tier 0: $0.00-$0.50 = 98% to LP, 2% to GP
    - Tier 1: $0.50-$0.60 = 85% to LP, 15% to GP
    - Tier 2: $0.60-$0.75 = 75% to LP, 25% to GP
    - Tier 3: Above $0.75 = 50% to LP, 50% to GP
    """
    dcf = distributable_cash_flow_per_unit

    if dcf <= tier_1_threshold:
        lp_distribution = dcf * 0.98
        gp_distribution = dcf * 0.02
    elif dcf <= tier_2_threshold:
        lp_distribution = (tier_1_threshold * 0.98) + ((dcf - tier_1_threshold) * 0.85)
        gp_distribution = (tier_1_threshold * 0.02) + ((dcf - tier_1_threshold) * 0.15)
    elif dcf <= tier_3_threshold:
        lp_distribution = (tier_1_threshold * 0.98) + (0.10 * 0.85) + ((dcf - tier_2_threshold) * 0.75)
        gp_distribution = (tier_1_threshold * 0.02) + (0.10 * 0.15) + ((dcf - tier_2_threshold) * 0.25)
    else:
        lp_distribution = (tier_1_threshold * 0.98) + (0.10 * 0.85) + (0.15 * 0.75) + ((dcf - tier_3_threshold) * 0.50)
        gp_distribution = (tier_1_threshold * 0.02) + (0.10 * 0.15) + (0.15 * 0.25) + ((dcf - tier_3_threshold) * 0.50)

    return {
        'lp_distribution': lp_distribution,
        'gp_distribution': gp_distribution,
        'lp_percentage': (lp_distribution / dcf * 100) if dcf > 0 else 0,
        'gp_take': (gp_distribution / dcf * 100) if dcf > 0 else 0,
        'marginal_lp_share': 50 if dcf > tier_3_threshold else (75 if dcf > tier_2_threshold else (85 if dcf > tier_1_threshold else 98))
    }

def allowed_earnings(
    rate_base: float,
    allowed_roe: float,
    equity_ratio: float,
    cost_of_debt: float,
    debt_ratio: float,
    tax_rate: float = 0.21
) -> dict:
    # Equity portion of earnings
    equity_income = rate_base * allowed_roe * equity_ratio

    # Debt portion (interest expense)
    debt_cost = rate_base * cost_of_debt * debt_ratio

    # After-tax WACC approach
    after_tax_debt_cost = debt_cost * (1 - tax_rate)

    # Total allowed earnings (different methods)
    return {
        'equity_income_portion': equity_income,
        'allowed_net_income': equity_income,  # Net income attributable to equity
        'total_allowed_return': equity_income + debt_cost,  # Before interest
        'wacc_based_return': equity_income + after_tax_debt_cost
    }
