from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(driver):
    """タブ1: 法人情報の取得"""
    data = {}
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[1]/a'))
        ).click()

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
            except Exception:
                data[f"サービス提供_{service_name}"] = None

    except Exception as e:
        print(f"Error in tab1: {e}")

    return data
