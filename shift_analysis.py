"""
Utility functions for holiday and fatigue analysis.
"""

from __future__ import annotations

import pandas as pd


def _month_part(day: int) -> str:
    """Return 'early', 'mid', or 'late' based on day of month."""
    if day <= 10:
        return "early"
    if day <= 20:
        return "mid"
    return "late"


def holiday_distribution(df: pd.DataFrame, date_col: str = "date", off_col: str = "is_off") -> pd.DataFrame:
    """Calculate holiday distribution by weekday and part of month.

    Parameters
    ----------
    df : DataFrame
        Schedule data containing at least ``date_col`` and ``off_col``.
    date_col : str, default "date"
        Column name with dates.
    off_col : str, default "is_off"
        Boolean column indicating holidays.

    Returns
    -------
    DataFrame
        Counts indexed by weekday and month part.
    """
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    off = data[data[off_col]].copy()
    off["weekday"] = off[date_col].dt.day_name()
    off["month_part"] = off[date_col].dt.day.apply(_month_part)
    result = off.groupby(["weekday", "month_part"]).size().unstack(fill_value=0)
    return result


def find_busy_holidays(
    df: pd.DataFrame,
    request_col: str = "requested_off",
    employee_col: str = "employee",
    date_col: str = "date",
    threshold: int = 1,
) -> pd.DataFrame:
    """Identify dates with many holiday requests.

    Returns a DataFrame with columns ``date``, ``num_requests``, ``employees`` and ``ratio``.
    ``ratio`` represents the proportion of employees requesting that date off.
    """
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    total_employees = data[employee_col].nunique()
    requests = data[data[request_col]]
    grouped = requests.groupby(date_col)[employee_col].agg(list)
    counts = grouped.apply(len)
    filtered = counts[counts >= threshold]
    result = pd.DataFrame({
        "date": filtered.index,
        "num_requests": filtered.values,
        "employees": grouped.loc[filtered.index].values,
    })
    result["ratio"] = result["num_requests"] / total_employees
    return result.sort_values("num_requests", ascending=False).reset_index(drop=True)


def calculate_fatigue_scores(
    df: pd.DataFrame,
    employee_col: str = "employee",
    date_col: str = "date",
    shift_col: str = "shift",
) -> pd.DataFrame:
    """Calculate fatigue metrics for each employee.

    ``shift`` values should include ``night`` for night shifts and ``off`` for holidays.
    All other values are considered working shifts.
    """
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col])
    data.sort_values([employee_col, date_col], inplace=True)

    def _calc(emp_df: pd.DataFrame) -> dict:
        nights = (emp_df[shift_col] == "night").sum()
        working = emp_df[shift_col] != "off"
        streaks = working.groupby((working != working.shift()).cumsum()).cumsum()
        streak_3 = (streaks >= 3).sum()
        streak_4 = (streaks >= 4).sum()
        streak_5 = (streaks >= 5).sum()
        score = nights + streak_3 + streak_4 + streak_5
        return {
            "night_shifts": nights,
            "streak_3": streak_3,
            "streak_4": streak_4,
            "streak_5": streak_5,
            "total_score": score,
        }

    metrics = data.groupby(employee_col).apply(_calc)
    return pd.DataFrame(metrics.tolist(), index=metrics.index).reset_index().rename(columns={"index": employee_col})

