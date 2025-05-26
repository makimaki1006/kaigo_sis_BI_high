from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(driver):
    """タブ2: 所在地等の情報の取得"""
    data = {}
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[2]/a'))
        ).click()

        data["事業所の名称"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[3]/td").text
        data["事業所のふりがな"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[2]/td").text
        data["郵便番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[4]/td").text
        data["市町村"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[4]/td[2]").text
        data["住所_番地まで"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[5]/td").text
        data["住所_番地以降"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[6]/td").text
        data["電話番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[7]/td").text
        data["FAX番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[8]/td").text

        try:
            data["ホームページ"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[9]/td[2]/a").get_attribute('href')
        except Exception:
            data["ホームページ"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[9]/td[2]").text

        data["介護保険事業所番号"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[10]/td").text
        data["事業所の管理者の氏名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[11]/td").text
        data["管理者の職名"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[12]/td").text
        data["事業の開始年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[14]/td").text
        data["指定の年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[15]/td").text
        data["指定の更新年月日"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[16]/td").text

        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[17]/td/img")
            data["生活保護法第54条の2指定機関"] = image_element.get_attribute('src')
        except Exception:
            data["生活保護法第54条の2指定機関"] = None

        data["主な利用交通手段"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[19]/td").text
        data["ケアプランデータ連携システム利用登録"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-3']/table/tbody/tr[20]/td").text

    except Exception as e:
        print(f"Error in tab2: {e}")

    return data
