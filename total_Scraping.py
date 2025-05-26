import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

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

def scrape_tab1_corporation_info(driver):
    """タブ1: 法人情報の取得"""
    data = {}
    try:
        # タブ1をクリック
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[1]/a'))
        ).click()
        
        # 法人情報の取得
        data["法人等の名称"] = driver.find_element(By.ID, "rowSpanId3").text
        data["法人等のふりがな"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[2]/td").text
        data["法人番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[3]/td").text
        data["主たる事務所の所在地_郵便番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[5]/td").text
        data["主たる事務所の所在地_市町村"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[4]/td").text
        data["法人代表者氏名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[6]/td").text
        data["代表者職名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[7]/td").text
        data["設立年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[8]/td").text
        data["法人種別"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[9]/td").text
        data["電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[10]/td").text
        data["FAX番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-1']/table/tbody/tr[11]/td").text
        
        # サービス提供状況（画像要素の処理）
        service_elements = [
            ("居宅介護支援", "//div[@id='tableGroup-1']/table[2]/tbody/tr[4]/td/img"),
            ("訪問介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[5]/td/img"),
            ("訪問入浴介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[6]/td/img"),
            ("訪問看護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[7]/td/img"),
            ("訪問リハビリテーション", "//div[@id='tableGroup-1']/table[2]/tbody/tr[8]/td/img"),
            ("通所介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[9]/td/img"),
            ("通所リハビリテーション", "//div[@id='tableGroup-1']/table[2]/tbody/tr[10]/td/img"),
            ("短期入所生活介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[11]/td/img"),
            ("短期入所療養介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[12]/td/img"),
            ("特定施設入居者生活介護", "//div[@id='tableGroup-1']/table[2]/tbody/tr[13]/td/img"),
            ("福祉用具貸与", "//div[@id='tableGroup-1']/table[2]/tbody/tr[14]/td/img"),
            ("特定福祉用具販売", "//div[@id='tableGroup-1']/table[2]/tbody/tr[15]/td/img"),
            ("住宅改修", "//div[@id='tableGroup-1']/table[2]/tbody/tr[16]/td/img")
        ]
        
        for service_name, xpath in service_elements:
            try:
                image_element = driver.find_element(By.XPATH, xpath)
                data[f"サービス提供_{service_name}"] = image_element.get_attribute('src')
            except:
                data[f"サービス提供_{service_name}"] = None
                
    except Exception as e:
        print(f"Error in tab1: {e}")
    
    return data

def scrape_tab2_location_info(driver):
    """タブ2: 所在地等の情報の取得"""
    data = {}
    try:
        # タブ2をクリック
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[2]/a'))
        ).click()
        
        # 所在地情報の取得
        data["事業所の名称"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[3]/td").text
        data["事業所のふりがな"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[2]/td").text
        data["郵便番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[4]/td").text
        data["市町村"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[4]/td[2]").text
        data["住所_番地まで"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[5]/td").text
        data["住所_番地以降"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[6]/td").text
        data["電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[7]/td").text
        data["FAX番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[8]/td").text
        
        # ホームページ（リンクの場合）
        try:
            data["ホームページ"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[9]/td[2]/a").get_attribute('href')
        except:
            data["ホームページ"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[9]/td[2]").text
            
        data["介護保険事業所番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[10]/td").text
        data["事業所の管理者の氏名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[11]/td").text
        data["管理者の職名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[12]/td").text
        data["事業の開始年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[14]/td").text
        data["指定の年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[15]/td").text
        data["指定の更新年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[16]/td").text
        
        # 生活保護法指定機関（画像）
        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[17]/td/img")
            data["生活保護法第54条の2指定機関"] = image_element.get_attribute('src')
        except:
            data["生活保護法第54条の2指定機関"] = None
            
        data["主な利用交通手段"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[19]/td").text
        data["ケアプランデータ連携システム利用登録"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[20]/td").text
        
    except Exception as e:
        print(f"Error in tab2: {e}")
    
    return data

def scrape_tab3_staff_info(driver):
    """タブ3: 従業者等の情報の取得"""
    data = {}
    try:
        # タブ3をクリック
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[3]/a'))
        ).click()
        
        # 主要な従業者情報の取得
        data["管理者_常勤_資格"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td").text
        data["管理者_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[2]").text
        data["管理者_非常勤_資格"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[3]").text
        data["管理者_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[4]").text
        data["管理者_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[5]").text
        data["管理者_常勤換算"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[6]").text
        
        # 介護支援専門員の情報
        data["介護支援専門員_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td").text
        data["介護支援専門員_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[2]").text
        data["介護支援専門員_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[3]").text
        data["介護支援専門員_常勤換算"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[4]").text
        
        # 事務員等の情報
        data["事務員等_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td").text
        data["事務員等_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td[2]").text
        data["事務員等_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td[3]").text
        
        # 資格・研修情報の取得（主要なもの）
        qualifications = [
            ("主任介護支援専門員", 14),
            ("介護支援専門員", 15),
            ("介護福祉士", 16),
            ("実務者研修", 17),
            ("初任者研修", 18),
            ("社会福祉士", 19),
            ("看護師", 20),
            ("准看護師", 21),
            ("保健師", 22),
            ("理学療法士", 23),
            ("作業療法士", 24),
            ("言語聴覚士", 25),
            ("栄養士", 26),
            ("管理栄養士", 27)
        ]
        
        for qual_name, row_num in qualifications:
            try:
                data[f"{qual_name}_常勤"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-4']/table/tbody/tr[{row_num}]/td").text
                data[f"{qual_name}_非常勤"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-4']/table/tbody/tr[{row_num}]/td[2]").text
                data[f"{qual_name}_合計"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-4']/table/tbody/tr[{row_num}]/td[3]").text
                data[f"{qual_name}_常勤換算"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-4']/table/tbody/tr[{row_num}]/td[4]").text
            except:
                continue
                
    except Exception as e:
        print(f"Error in tab3: {e}")
    
    return data

def scrape_tab4_service_info(driver):
    """タブ4: サービス内容の情報の取得"""
    data = {}
    try:
        # タブ4をクリック
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[4]/a'))
        ).click()
        
        # 基本情報
        data["事業所の運営に関する方針"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[2]/td").text
        
        # 営業時間
        data["平日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[4]/td").text
        data["土曜日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[5]/td").text
        data["日曜日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[6]/td").text
        data["祝日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[7]/td").text
        data["定休日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[8]/td").text
        data["留意事項"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[9]/td").text
        
        # 緊急時対応
        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[11]/td/img")
            data["緊急時の電話連絡の対応"] = image_element.get_attribute('src')
        except:
            data["緊急時の電話連絡の対応"] = None
            
        data["緊急時連絡先電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[12]/td").text
        data["通常のサービス提供地域"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[14]/td").text
        
        # 介護報酬加算状況（主要なもの）
        addons = [
            ("特定事業所加算Ⅰ", 17),
            ("特定事業所加算Ⅱ", 18),
            ("特定事業所加算Ⅲ", 19),
            ("特定事業所加算A", 20),
            ("特定事業所医療介護連携加算", 21),
            ("入院時情報連携加算Ⅰ", 22),
            ("入院時情報連携加算Ⅱ", 23),
            ("退院退所加算Ⅰイ", 24),
            ("退院退所加算Ⅰロ", 25),
            ("退院退所加算Ⅱイ", 26),
            ("退院退所加算Ⅱロ", 27),
            ("退院退所加算Ⅲ", 28),
            ("通院時情報連携加算", 29),
            ("緊急時等居宅カンファレンス加算", 30),
            ("ターミナルケアマネジメント加算", 31)
        ]
        
        for addon_name, row_num in addons:
            try:
                image_element = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[{row_num}]/td/img")
                data[f"加算_{addon_name}"] = image_element.get_attribute('src')
            except:
                data[f"加算_{addon_name}"] = None
        
        # 利用者数情報
        data["介護支援専門員一人当たりの利用者数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[32]/td").text
        
        # 要介護度別利用者数
        care_levels = ["要支援1", "要支援2", "要介護1", "要介護2", "要介護3", "要介護4", "要介護5", "合計"]
        for i, level in enumerate(care_levels):
            try:
                data[f"{level}_利用者数"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[35]/td[{i+1}]").text
                data[f"{level}_前年同月"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[36]/td[{i+1}]").text
            except:
                continue
        
        # 苦情対応窓口
        data["苦情対応窓口名称"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[38]/td").text
        data["苦情対応電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[39]/td").text
        
        # 損害賠償保険
        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[47]/td/img")
            data["損害賠償保険の加入状況"] = image_element.get_attribute('src')
        except:
            data["損害賠償保険の加入状況"] = None
            
        data["介護サービス提供内容の特色"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[49]/td").text
        
        # サービス利用割合
        services = ["訪問介護", "通所介護", "地域密着型通所介護", "福祉用具貸与"]
        for i, service in enumerate(services):
            try:
                data[f"ケアプラン_{service}_利用割合"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[{52+i}]/td").text
            except:
                continue
                
    except Exception as e:
        print(f"Error in tab4: {e}")
    
    return data

def scrape_tab5_user_info(driver):
    """タブ5: 利用者等の情報の取得"""
    data = {}
    try:
        # タブ5をクリック
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[5]/a'))
        ).click()
        
        # 利用者関連情報
        data["交通費の額及び算定方法"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[3]/td").text
        
        # キャンセル料の徴収状況
        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[4]/td/img")
            data["キャンセル料徴収状況"] = image_element.get_attribute('src')
        except:
            data["キャンセル料徴収状況"] = None
            
        data["キャンセル料の額・算定方法"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[5]/td").text
        
    except Exception as e:
        print(f"Error in tab5: {e}")
    
    return data

def scrape_website(driver, url):
    """1つのURLから全タブの情報を取得"""
    all_data = {}
    
    try:
        driver.get(url)
        # 最初のタブが読み込まれるまで待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="kihonItemTab"]/li[1]/a'))
        )
        
        # 各タブからデータを取得
        tab1_data = scrape_tab1_corporation_info(driver)
        tab2_data = scrape_tab2_location_info(driver)
        tab3_data = scrape_tab3_staff_info(driver)
        tab4_data = scrape_tab4_service_info(driver)
        tab5_data = scrape_tab5_user_info(driver)
        
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
