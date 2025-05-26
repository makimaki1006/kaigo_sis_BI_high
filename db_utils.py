import sqlite3
import pandas as pd


def save_to_sqlite(
    df: pd.DataFrame,
    db_path: str,
    table_name: str = 'scraped_data',
    append: bool = False,
) -> None:
    """Save a DataFrame to a SQLite database.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to save.
    db_path : str
        Path to the SQLite database file.
    table_name : str
        Name of the table to write to. Defaults to 'scraped_data'.
    append : bool
        If True, append records to an existing table. Otherwise the table is
        replaced.
    """

    df_with_timestamp = df.copy()
    df_with_timestamp["timestamp"] = pd.Timestamp.now()

    with sqlite3.connect(db_path) as conn:
        df_with_timestamp.to_sql(
            table_name,
            conn,
            if_exists='append' if append else 'replace',
            index=False,
        )
