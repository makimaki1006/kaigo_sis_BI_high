from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(driver):
    """タブ3: 従業者等の情報の取得"""
    data = {}
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="kihonItemTab"]/li[3]/a'))
        ).click()

        data["管理者_常勤_資格"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td").text
        data["管理者_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[2]").text
        data["管理者_非常勤_資格"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[3]").text
        data["管理者_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[4]").text
        data["管理者_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[5]").text
        data["管理者_常勤換算"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[4]/td[6]").text

        data["介護支援専門員_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td").text
        data["介護支援専門員_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[2]").text
        data["介護支援専門員_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[3]").text
        data["介護支援専門員_常勤換算"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[5]/td[4]").text

        data["事務員等_常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td").text
        data["事務員等_非常勤_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td[2]").text
        data["事務員等_合計_実人数"] = driver.find_element(By.XPATH, "//div[@id='tableGroup-4']/table/tbody/tr[6]/td[3]").text

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
            except Exception:
                continue

    except Exception as e:
        print(f"Error in tab3: {e}")

    return data
