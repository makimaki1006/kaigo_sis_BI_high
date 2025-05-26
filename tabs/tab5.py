from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(driver):
    """タブ5: 利用者等の情報の取得"""
    data = {}
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[5]/a'))
        ).click()

        data["交通費の額及び算定方法"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[3]/td").text

        try:
            image_element = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[4]/td/img")
            data["キャンセル料徴収状況"] = image_element.get_attribute('src')
        except Exception:
            data["キャンセル料徴収状況"] = None

        data["キャンセル料の額・算定方法"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-6']/table/tbody/tr[5]/td").text

    except Exception as e:
        print(f"Error in tab5: {e}")

    return data
