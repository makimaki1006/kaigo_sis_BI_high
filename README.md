# kaigo_sis_BI_high

## Requirements
- Python 3.10 or later
- Google Chrome installed (used by Selenium)

## Setup
Install dependencies with pip:

```bash
pip install pandas selenium webdriver-manager openpyxl geopy folium
```

## Input
Place an Excel file named `事業所.xlsx` in this directory. It must have a column called `URL` containing the pages to scrape.

## Running
Execute the scraper using:

```bash
python total_Scraping.py
```

## Output
The following files are generated in the current directory:

- `統合スクレイピング結果.xlsx` – main scraping results.
- `統合スクレイピング結果.csv` – CSV backup. If Excel export fails, `統合スクレイピング結果_エラー時.csv` is saved instead.
- `中間保存_<番号>件.xlsx` – periodic backups every 10 processed URLs.
- `緊急保存_スクレイピング結果.csv` – emergency backup written when an exception stops the run.
- `scraped_data.db` – SQLite database storing the results.

## Visualization
Use `visualize_facilities.py` to display facilities near a given city on a map.

```bash
python visualize_facilities.py --city "札幌市" --radius 5 --csv 統合スクレイピング結果.csv
```

This script geocodes facility addresses and outputs an interactive map (`map.html`).



## Shift and Holiday Analysis
The `shift_analysis.py` module provides utilities for analyzing holiday
patterns and fatigue metrics. Import the functions you need and pass a
`pandas.DataFrame` with schedule information.

```python
import pandas as pd
from shift_analysis import holiday_distribution, find_busy_holidays
```
