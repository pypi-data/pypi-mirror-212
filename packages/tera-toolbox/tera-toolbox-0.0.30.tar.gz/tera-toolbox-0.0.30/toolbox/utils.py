import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from . import stats


def extract_values_from_key(list_of_dicts, key):
    return [d[key] for d in list_of_dicts if key in d]


def count_days(start_date, end_date, business=True, holidays=[]):
    date_range = pd.date_range(start_date, end_date, freq="D")

    if business:
        holidays = pd.to_datetime(holidays)
        weekdays = np.isin(date_range.weekday, [5, 6], invert=True)
        non_holidays = np.isin(date_range, holidays, invert=True)
        valid_days = np.logical_and(weekdays, non_holidays).sum()
    else:
        valid_days = len(date_range)

    return valid_days - 1


def add_days(
    start_date,
    num_days=0,
    num_months=0,
    num_years=0,
    business=True,
    holidays=[],
):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)

    holidays = [datetime.strptime(h, date_format) for h in holidays]

    new_date = start_date + relativedelta(
        days=num_days, months=num_months, years=num_years
    )

    if business:
        while new_date.weekday() in (5, 6) or new_date in holidays:
            new_date += timedelta(days=1)

    return new_date.strftime(date_format)


def random_bool(p, N):
    return np.random.choice(a=[True, False], size=(N,), p=[p, 1 - p])


def patrimonio_analysis(
    pl_inicial,
    ap,
    ex,
    months=1200,
    freq_ap=1,
    timing_ap=False,
    max_ap=999999999,
    max_ex=999999999,
    ap_till=720,
    ap_from=1,
    freq_ex=1,
    timing_ex=True,
    ex_till=1200,
    ex_from=1,
    juro_real=0.02,
    step_freq_ap=0,
    step_ap=0.0,
    step_freq_ex=0,
    step_ex=0.0,
    extra_ap=0,
    extra_prob_ap=0.0,
    extra_ex=0,
    extra_prob_ex=0.0,
    extra=[],
):
    extra = pd.DataFrame(np.array(extra), columns=["months", "aportes", "despesas"])
    df = pd.DataFrame(np.arange(1, months + 1, 1), columns=["months"])
    df["years"] = df["months"] / 12
    df["aportes"] = np.minimum(
        max_ap,
        (
            (df["months"] % freq_ap == 0)
            & (df["months"] <= ap_till)
            & (df["months"] >= ap_from)
        )
        * (ap * (1 + step_ap) ** (df["months"] // step_freq_ap)),
    ) + extra_ap * random_bool(extra_prob_ap, months)
    df["despesas"] = np.minimum(
        max_ex,
        (
            (df["months"] % freq_ex == 0)
            & (df["months"] <= ex_till)
            & (df["months"] >= ex_from)
        )
        * (ex * (1 + step_ex) ** (df["months"] // step_freq_ex)),
    ) + extra_ex * random_bool(extra_prob_ex, months)

    df["aportes"] = df["aportes"] + extra["aportes"]
    df["despesas"] = df["despesas"] + extra["despesas"]

    return calculate_patrimonio(df, pl_inicial, timing_ap, timing_ex, juro_real)


def calculate_patrimonio(df, pl_inicial, timing_ap, timing_ex, juro_real):
    juro_real = (1 + juro_real) ** (1 / 12) - 1
    result = []
    for i, r in df.iterrows():
        result.append(
            (
                (pl_inicial if i == 0 else result[i - 1])
                + (r["aportes"] if timing_ap else 0)
                - (r["despesas"] if timing_ex else 0)
            )
            * (1 + juro_real)
            + (r["aportes"] if not timing_ap else 0)
            - (r["despesas"] if not timing_ex else 0)
        )
    df["patrimonio"] = result

    return df


def sensitivity_analysis(data, function, var_x, var_y):
    # Initialize results list
    results = []

    # Iterate over all values in var_x and var_y
    for x in var_x["values"]:
        for y in var_y["values"]:
            # Update data dict
            data[var_x["key"]] = x
            data[var_y["key"]] = y

            # Call function with updated data as parameters
            result = function(**data)

            # Store x, y, and result in results list
            results.append((x, y, result))

    return results


def setup(data):
    """setup data to organize time-series sensitive data"""
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df


def clean(data, fill_method="zero"):
    """
    Cleans the data by replacing missing values and infinities.

    Args:
        data (pd.DataFrame): The input data.
        fill_method (str, optional): The method to use for filling missing values. Defaults to 'ffill'.
            Options are:
            - 'ffill': forward fill, which propagates the last observed non-null value forward until another non-null value is met.
            - 'bfill': backward fill, which propagates the next observed non-null value backwards until another non-null value is met.
            - 'zero': fill with zeros.

    Returns:
        pd.DataFrame: The cleaned data.
    """

    # Copy the data to avoid modifying the original DataFrame
    data_clean = data.copy()

    # Fill missing values
    if fill_method == "ffill":
        data_clean = data_clean.ffill()
    elif fill_method == "bfill":
        data_clean = data_clean.bfill()
    elif fill_method == "zero":
        data_clean = data_clean.fillna(0)
    else:
        raise ValueError(
            "Invalid fill method. Options are 'ffill', 'bfill', and 'zero'."
        )

    # Replace infinities
    data_clean = data_clean.replace([np.inf, -np.inf], 0)

    return data_clean


def to_returns(prices, log_returns=False):
    """
    Calculates the returns of one or more assets in a DataFrame or Series.

    Args:
        prices (Union[pd.DataFrame, pd.Series]): A DataFrame or Series containing the prices of the assets.
        log_returns (bool, optional): If True, calculates log returns instead of simple returns. Defaults to False.

    Returns:
        Union[pd.DataFrame, pd.Series]: Returns a DataFrame or Series with the returns of the assets.
    """

    # Ensure input is a DataFrame or Series
    if not isinstance(prices, (pd.DataFrame, pd.Series)):
        raise ValueError("Input must be a pandas DataFrame or Series.")

    # Calculate returns for each asset individually
    if isinstance(prices, pd.DataFrame):
        returns = prices.apply(
            lambda x: np.log(x / x.shift(1)).dropna()
            if log_returns
            else x.pct_change().dropna(),
            axis=0,
        )
    else:  # prices is a pd.Series
        returns = (
            np.log(prices / prices.shift(1)).dropna()
            if log_returns
            else prices.pct_change().dropna()
        )

    return returns


def to_rolling_returns(returns):
    """
    Calculates rolling compounded returns.

    Args:
        returns (pd.DataFrame): The input returns.

    Returns:
        pd.DataFrame: The rolling compounded returns.
    """
    return returns.add(1).cumprod() - 1


def rebase(prices, base=100, base_date=None):
    """
    Rebase a series to a given initial base.

    Args:
        prices (pd.DataFrame): The input price data.
        base (float, optional): The base value for the rebased series. Defaults to 100.
        base_date (str, optional): The date from which the base value should start. If not provided, the base value starts from the first non-NaN date for each asset in the data.

    Returns:
        pd.DataFrame: The rebased series.
    """

    # Convert the base_date to Timestamp if it's not None
    if base_date is not None:
        base_date = pd.to_datetime(base_date)

    for column in prices.columns:
        # If base_date is not provided, use the first non-NaN date for each asset
        actual_base_date = prices[column].first_valid_index()
        if base_date is not None:
            actual_base_date = max(actual_base_date, base_date)

        # Get the price at the base date
        base_price = prices.loc[actual_base_date, column]

        # Rebase the prices for this asset
        prices[column] = prices[column] / base_price * base

    return prices


def to_quotes(returns, base=100, base_date=None):
    """
    Converts returns to quote prices.

    Args:
        returns (pd.DataFrame): The input returns.
        base (float, optional): The base value for the quote prices. Defaults to 1e5.
        base_date (str, optional): The date from which the base value should start. If not provided, the base value starts from the beginning of the data.

    Returns:
        pd.DataFrame: The quote prices.
    """
    # Calculate rolling compounded returns
    rolling_returns = 1 + to_rolling_returns(returns)

    # Rebase the quotes to the given base and base_date
    rebased_quotes = rebase(rolling_returns, base, base_date)

    return rebased_quotes


def to_excess_returns(returns, rf=0.0, periods=1):
    """
    Calculates excess returns.

    Args:
        returns (np.ndarray, pd.DataFrame or pd.Series): The input returns.
        rf (float or pd.Series, optional): The risk-free rate. Defaults to 0.0.
        periods (int, optional): The number of periods for the risk-free rate calculation. Defaults to 252.

    Returns:
        np.ndarray, pd.DataFrame or pd.Series: The excess returns.
    """
    if periods is not None:
        rf = np.power(1 + rf, 1.0 / periods) - 1.0

    if isinstance(returns, pd.DataFrame) or isinstance(returns, pd.Series):
        excess_returns = returns.sub(rf, axis=0)
    else:  # numpy ndarray
        excess_returns = returns - rf

    if isinstance(rf, pd.Series):
        excess_returns = excess_returns.reindex(rf.index)

    return excess_returns


def group_returns(returns, groupby, compounded=True):
    """
    Summarizes returns based on grouping criteria.

    Args:
        returns (pd.DataFrame or pd.Series): The input returns.
        groupby (int, list, pd.Series, or pd.Grouper): The grouping criteria.
        compounded (bool, optional): If True, calculates compounded returns. Defaults to True.

    Returns:
        pd.DataFrame or pd.Series: The summarized returns.
    """
    if compounded:
        return returns.groupby(groupby).apply(stats.total_return)
    return returns.groupby(groupby).sum()


def aggregate_returns(returns, period=None, compounded=True):
    """
    Aggregates returns based on date periods.

    Args:
        returns (pd.DataFrame or pd.Series): The input returns.
        period (str or list, optional): The desired date period for aggregation. Defaults to None.
        compounded (bool, optional): If True, calculates compounded returns. Defaults to True.

    Returns:
        pd.DataFrame or pd.Series: The aggregated returns.
    """
    if period is None or "day" in period:
        return returns

    index = returns.index
    groupby_mapping = {
        "month": [index.year, index.month],
        "quarter": [index.year, index.quarter],
        "year": index.year,
        "week": [index.year, index.isocalendar().week],
        "eow": [index.year, index.isocalendar().week],
        "eom": [index.year, index.month],
        "eoq": [index.year, index.quarter],
    }

    if period in groupby_mapping:
        return group_returns(returns, groupby_mapping[period], compounded=compounded)

    return returns


def to_drawdown_series(returns):
    """
    Convert returns series to drawdown series.

    Args:
        returns (pd.Series or pd.DataFrame): The input returns series.

    Returns:
        pd.Series or pd.DataFrame: The drawdown series.
    """
    if not isinstance(returns, (pd.Series, pd.DataFrame)):
        raise ValueError("Input must be a pandas Series or DataFrame.")

    prices = to_quotes(returns, base=1)
    prices = clean(prices)

    max_prices = np.maximum.accumulate(prices)
    dd = prices / max_prices - 1.0

    # Handle division by zero or infinity
    dd = dd.replace([np.inf, -np.inf], np.nan).fillna(0)

    return dd
