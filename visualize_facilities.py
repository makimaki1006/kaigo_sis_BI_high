import argparse
import sqlite3
from functools import lru_cache

import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import folium


def load_data(csv_path: str | None = None, db_path: str | None = None, table_name: str = "scraped_data") -> pd.DataFrame:
    """Load scraped data from CSV or SQLite."""
    if csv_path:
        return pd.read_csv(csv_path)
    if db_path:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql(f"SELECT * FROM {table_name}", conn)
    raise ValueError("Either csv_path or db_path must be provided")


@lru_cache(maxsize=None)
def _geocode(geolocator: Nominatim, address: str) -> tuple[float | None, float | None]:
    """Geocode an address with caching."""
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass
    return None, None


def add_coordinates(df: pd.DataFrame, geolocator: Nominatim) -> pd.DataFrame:
    """Append latitude and longitude columns based on address."""
    def _addr(row: pd.Series) -> str:
        parts = [row.get("事業所_市町村", ""), row.get("事業所_住所_番地まで", ""), row.get("事業所_住所_番地以降", "")]
        return "".join(str(p) for p in parts if p)

    coords = df.apply(lambda row: _geocode(geolocator, _addr(row)), axis=1)
    df[["latitude", "longitude"]] = list(coords)
    return df


def calculate_distance_km(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return the geodesic distance in kilometers between two points."""
    return geodesic(p1, p2).km


def filter_by_radius(df: pd.DataFrame, center: tuple[float, float], radius_km: float) -> pd.DataFrame:
    """Return subset of df within radius_km of center."""
    def _within(row: pd.Series) -> bool:
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            return False
        dist = calculate_distance_km(center, (row["latitude"], row["longitude"]))
        return dist <= radius_km

    return df[df.apply(_within, axis=1)].copy()


def create_map(df: pd.DataFrame, center: tuple[float, float], radius_km: float) -> folium.Map:
    """Create a folium map with facility markers."""
    m = folium.Map(location=center, zoom_start=12)
    folium.Circle(center, radius=radius_km * 1000, color="blue", fill=False).add_to(m)
    for _, row in df.iterrows():
        lat, lon = row["latitude"], row["longitude"]
        name = row.get("事業所_名称", "施設")
        address = row.get("事業所_市町村", "") + row.get("事業所_住所_番地まで", "") + row.get("事業所_住所_番地以降", "")
        folium.Marker([lat, lon], popup=f"{name}\n{address}").add_to(m)
    return m


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize facilities on a map")
    parser.add_argument("--city", required=True, help="City name as center")
    parser.add_argument("--radius", type=float, default=5, help="Radius in kilometers")
    parser.add_argument("--csv", dest="csv_path", help="CSV file with scraped data")
    parser.add_argument("--db", dest="db_path", help="SQLite database path")
    parser.add_argument("--output", default="map.html", help="Output HTML file")
    args = parser.parse_args()

    geolocator = Nominatim(user_agent="kaigo_sis_visualizer")
    center_loc = geolocator.geocode(args.city)
    if not center_loc:
        raise SystemExit(f"City not found: {args.city}")

    df = load_data(csv_path=args.csv_path, db_path=args.db_path)
    df = add_coordinates(df, geolocator)
    filtered = filter_by_radius(df, (center_loc.latitude, center_loc.longitude), args.radius)

    m = create_map(filtered, (center_loc.latitude, center_loc.longitude), args.radius)
    m.save(args.output)
    print(f"Map saved to {args.output} with {len(filtered)} facilities")


if __name__ == "__main__":
    main()
