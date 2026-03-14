from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_priceoye_by_category():

    # url = "https://priceoye.pk/mobiles/samsung"
    url = "https://priceoye.pk/mobiles/apple"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Wait until products load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "product_list_scroll_identifier"))
    )

    products = driver.find_elements(By.CSS_SELECTOR, "div.productBox.b-productBox")

    data = []

    for p in products:
        name = p.find_element(By.TAG_NAME, "h4").text
        price = p.find_element(By.CSS_SELECTOR, "div.price-box span").text

        data.append({
            "name": name,
            "price": price
        })

    driver.quit()

    return data