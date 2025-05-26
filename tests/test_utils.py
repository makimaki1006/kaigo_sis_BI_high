import os
import sqlite3
import pandas as pd

from db_utils import save_to_sqlite
from total_Scraping import clean_data_for_excel


def test_clean_data_for_excel():
    long_text = 'x' * 33000
    df = pd.DataFrame({
        'col1': [None, 'hello\r\nworld'],
        'col2': [long_text, 'short']
    })

    cleaned = clean_data_for_excel(df)

    assert cleaned.loc[0, 'col1'] == ''
    assert cleaned.loc[1, 'col1'] == 'hello\nworld'
    assert cleaned.loc[0, 'col2'].startswith('x' * 32000)
    assert cleaned.loc[0, 'col2'].endswith('...')
    assert len(cleaned.loc[0, 'col2']) == 32003
    # all columns converted to string
    assert cleaned.dtypes.eq('object').all()


def test_save_to_sqlite(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    db_file = tmp_path / 'test.db'
    save_to_sqlite(df, str(db_file), table_name='tbl')

    with sqlite3.connect(db_file) as conn:
        result = pd.read_sql('SELECT * FROM tbl', conn)

    pd.testing.assert_frame_equal(df, result)
