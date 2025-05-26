from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(driver):
    """タブ4: サービス内容の情報の取得"""
    data = {}
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[4]/a'))
        ).click()

        data["事業所の運営に関する方針"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[2]/td").text

        data["平日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[4]/td").text
        data["土曜日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[5]/td").text
        data["日曜日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[6]/td").text
        data["祝日の営業時間"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[7]/td").text
        data["定休日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[8]/td").text
        data["留意事項"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[9]/td").text

        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[11]/td/img")
            data["緊急時の電話連絡の対応"] = image_element.get_attribute('src')
        except Exception:
            data["緊急時の電話連絡の対応"] = None

        data["緊急時連絡先電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[12]/td").text
        data["通常のサービス提供地域"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[14]/td").text

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
            except Exception:
                data[f"加算_{addon_name}"] = None

        data["介護支援専門員一人当たりの利用者数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[32]/td").text

        care_levels = ["要支援1", "要支援2", "要介護1", "要介護2", "要介護3", "要介護4", "要介護5", "合計"]
        for i, level in enumerate(care_levels):
            try:
                data[f"{level}_利用者数"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[35]/td[{i+1}]").text
                data[f"{level}_前年同月"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[36]/td[{i+1}]").text
            except Exception:
                continue

        data["苦情対応窓口名称"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[38]/td").text
        data["苦情対応電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[39]/td").text

        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[47]/td/img")
            data["損害賠償保険の加入状況"] = image_element.get_attribute('src')
        except Exception:
            data["損害賠償保険の加入状況"] = None

        data["介護サービス提供内容の特色"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-5']/table/tbody/tr[49]/td").text

        services = ["訪問介護", "通所介護", "地域密着型通所介護", "福祉用具貸与"]
        for i, service in enumerate(services):
            try:
                data[f"ケアプラン_{service}_利用割合"] = driver.find_element(By.XPATH, f"//div[@id='tableGroup-5']/table/tbody/tr[{52+i}]/td").text
            except Exception:
                continue

    except Exception as e:
        print(f"Error in tab4: {e}")

    return data
