import sqlite3
import pandas as pd


def save_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str = 'scraped_data') -> None:
    """Save a DataFrame to a SQLite database.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to save.
    db_path : str
        Path to the SQLite database file.
    table_name : str
        Name of the table to write to. Defaults to 'scraped_data'.
    """
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
