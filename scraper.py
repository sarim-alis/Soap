from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_priceoye_by_category():

    url = "https://priceoye.pk/mobiles/vivo"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.ID,"product_list_scroll_identifier"))
    )

    products = driver.find_elements(By.CSS_SELECTOR,"div.productBox.b-productBox")

    data = []

    for p in products:

        try:
            name = p.find_element(By.TAG_NAME,"h4").text
            price = p.find_element(By.CSS_SELECTOR,"div.price-box span").text
            link = p.find_element(By.TAG_NAME,"a").get_attribute("href")

            driver.get(link)

            # wait for specs to load
            WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"ul.bullet-specs"))
            )

            specs = {}
            specs["name"] = name
            specs["price"] = price

            bullets = driver.find_elements(By.CSS_SELECTOR,"ul.bullet-specs li")

            for b in bullets:
                key = b.find_element(By.TAG_NAME,"span").text.strip()
                value = b.find_element(By.TAG_NAME,"strong").text.strip()

                specs[key.lower().replace(" ","_")] = value

            data.append(specs)

            driver.back()

            WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.ID,"product_list_scroll_identifier"))
            )

        except Exception as e:
            print("Error:",e)

    driver.quit()

    return data