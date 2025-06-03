import pandas as pd
from shift_analysis import holiday_distribution, find_busy_holidays, calculate_fatigue_scores


def test_holiday_distribution():
    data = pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-11', '2023-01-22']),
        'is_off': [True, True, True, True]
    })
    result = holiday_distribution(data)
    assert result.loc['Sunday', 'early'] == 1
    assert result.loc['Monday', 'early'] == 1
    assert result.loc['Wednesday', 'mid'] == 1
    assert result.loc['Sunday', 'late'] == 1


def test_find_busy_holidays():
    df = pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02']),
        'employee': ['A', 'B', 'A'],
        'requested_off': [True, True, True]
    })
    result = find_busy_holidays(df, threshold=2)
    assert len(result) == 1
    row = result.iloc[0]
    assert row['date'] == pd.Timestamp('2023-01-01')
    assert row['num_requests'] == 2
    assert set(row['employees']) == {'A', 'B'}
    assert 0 < row['ratio'] <= 1


def test_calculate_fatigue_scores():
    df = pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']),
        'employee': ['A'] * 4,
        'shift': ['day', 'night', 'day', 'day']
    })
    result = calculate_fatigue_scores(df)
    row = result[result['employee'] == 'A'].iloc[0]
    assert row['night_shifts'] == 1
    assert row['streak_3'] >= 1
    assert row['total_score'] >= row['night_shifts']
