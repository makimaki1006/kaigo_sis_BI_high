import pandas as pd
from visualize_facilities import calculate_distance_km, filter_by_radius


def test_calculate_distance_km():
    tokyo = (35.6895, 139.6917)
    yokohama = (35.4437, 139.6380)
    dist = calculate_distance_km(tokyo, yokohama)
    assert 20 < dist < 40


def test_filter_by_radius():
    data = pd.DataFrame({
        'latitude': [35.7, 35.4],
        'longitude': [139.7, 139.6],
        'name': ['A', 'B']
    })
    center = (35.6895, 139.6917)
    result = filter_by_radius(data, center, radius_km=15)
    assert len(result) == 1
    assert result.iloc[0]['name'] == 'A'
