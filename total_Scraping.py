import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from tabs import tab1, tab2, tab3, tab4, tab5

def setup_webdriver():
    """WebDriverの設定と初期化"""
    options = webdriver.ChromeOptions()
    # ヘッドレスモードを使いたい場合は以下をコメントアウト
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    return driver

def scrape_website(driver, url):
    """1つのURLから全タブの情報を取得"""
    all_data = {}
    
    try:
        driver.get(url)
        # ページの読み込み待機
        time.sleep(2)
        
        # 各タブからデータを取得
        tab1_data = tab1.scrape(driver)
        tab2_data = tab2.scrape(driver)
        tab3_data = tab3.scrape(driver)
        tab4_data = tab4.scrape(driver)
        tab5_data = tab5.scrape(driver)
        
        # 全データを統合
        all_data.update(tab1_data)
        all_data.update(tab2_data)
        all_data.update(tab3_data)
        all_data.update(tab4_data)
        all_data.update(tab5_data)
        
        # URLも記録
        all_data["URL"] = url
        
        print(f"Successfully scraped: {url}")
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        all_data["URL"] = url
        all_data["エラー"] = str(e)
    
    return all_data

def clean_data_for_excel(df):
    """ExcelへのエクスポートのためにDataFrameをクリーンアップ"""
    df_clean = df.copy()
    
    for column in df_clean.columns:
        # NaN値を空文字列に変換
        df_clean[column] = df_clean[column].fillna('')
        
        # 文字列型に変換
        df_clean[column] = df_clean[column].astype(str)
        
        # Excelのセル文字数制限（32,767文字）を超える場合は切り詰める
        df_clean[column] = df_clean[column].apply(
            lambda x: x[:32000] + "..." if len(str(x)) > 32000 else x
        )
        
        # 改行文字を適切に処理（Excelでも改行として表示される）
        df_clean[column] = df_clean[column].apply(
            lambda x: str(x).replace('\r\n', '\n').replace('\r', '\n')
        )
    
    return df_clean

def save_to_excel_with_formatting(df, filename):
    """フォーマット付きでExcelに保存"""
    try:
        # データをクリーンアップ
        df_clean = clean_data_for_excel(df)
        
        # ExcelWriterを使用してより詳細な制御を行う
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # メインデータを保存
            df_clean.to_excel(writer, sheet_name='スクレイピング結果', index=False)
            
            # ワークシートを取得
            worksheet = writer.sheets['スクレイピング結果']
            
            # 列幅を自動調整（最大50文字まで）
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            # ヘッダー行を固定
            worksheet.freeze_panes = 'A2'
        
        print(f"Excel file saved successfully: {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving to Excel with formatting: {e}")
        # フォールバック：シンプルな保存を試行
        try:
            df_clean = clean_data_for_excel(df)
            df_clean.to_excel(filename, index=False, engine='openpyxl')
            print(f"Excel file saved with basic formatting: {filename}")
            return True
        except Exception as e2:
            print(f"Error in fallback save: {e2}")
            return False

def main():
    """メイン処理"""
    excel_path = '事業所.xlsx'
    
    try:
        # ExcelファイルからURLリストを読み込み
        urls_df = pd.read_excel(excel_path, usecols=["URL"])
        print(f"Found {len(urls_df)} URLs to scrape")
        
        # WebDriverの初期化
        driver = setup_webdriver()
        
        scraped_data_list = []
        total_urls = len(urls_df)
        
        for index, row in urls_df.iterrows():
            url = row['URL']
            print(f"Processing {index + 1}/{total_urls}: {url}")
            
            # 各URLからデータを取得
            scraped_row = scrape_website(driver, url)
            scraped_data_list.append(scraped_row)
            
            # サーバーに負荷をかけないよう少し待機
            time.sleep(1)
            
            # 10件ごとに中間保存（大量データの場合のリスク軽減）
            if (index + 1) % 10 == 0:
                temp_df = pd.DataFrame(scraped_data_list)
                temp_filename = f"中間保存_{index + 1}件.xlsx"
                save_to_excel_with_formatting(temp_df, temp_filename)
                print(f"Intermediate save completed: {temp_filename}")
        
        # WebDriverを終了
        driver.quit()
        
        # 結果をDataFrameに変換
        scraped_data = pd.DataFrame(scraped_data_list)
        
        # 最終結果をExcelファイルに出力
        output_filename = "統合スクレイピング結果.xlsx"
        success = save_to_excel_with_formatting(scraped_data, output_filename)
        
        if success:
            print(f"Scraping completed! Results saved to {output_filename}")
            print(f"Total records: {len(scraped_data)}")
            print(f"Total columns: {len(scraped_data.columns)}")
            
            # データの統計情報を表示
            print("\n=== データ概要 ===")
            print(f"収集したURL数: {len(scraped_data)}")
            print(f"エラーが発生したURL数: {scraped_data['エラー'].notna().sum() if 'エラー' in scraped_data.columns else 0}")
            print(f"正常に処理されたURL数: {len(scraped_data) - (scraped_data['エラー'].notna().sum() if 'エラー' in scraped_data.columns else 0)}")
            
            # CSVでもバックアップ保存
            csv_filename = "統合スクレイピング結果.csv"
            scraped_data.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"CSV backup saved: {csv_filename}")
        else:
            print("Excel保存に失敗しました。CSVで保存します。")
            csv_filename = "統合スクレイピング結果_エラー時.csv"
            scraped_data.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"CSV file saved: {csv_filename}")
        
    except Exception as e:
        print(f"Error in main process: {e}")
        
        # エラー時でも可能な限りデータを保存
        if 'scraped_data_list' in locals() and scraped_data_list:
            emergency_df = pd.DataFrame(scraped_data_list)
            emergency_filename = "緊急保存_スクレイピング結果.csv"
            emergency_df.to_csv(emergency_filename, index=False, encoding='utf-8-sig')
            print(f"Emergency save completed: {emergency_filename}")
    
    finally:
        # 万が一WebDriverが残っている場合の処理
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()
