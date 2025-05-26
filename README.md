# kaigo_sis_BI_high

## Requirements
- Python 3.10 or later
- Google Chrome installed (used by Selenium)

## Setup
Install dependencies with pip:

```bash
pip install pandas selenium webdriver-manager openpyxl
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

