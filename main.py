from selenium import webdriver
from selenium.common import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.support.wait import WebDriverWait

# Constants
ERRORS = [NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException]
RUNTIME = 300
SELECT_TIME = 5

# Keep browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Scrape
driver = webdriver.Chrome(options=chrome_options)

# Maximize size
driver.maximize_window()
driver.get("https://ozh.github.io/cookieclicker/")

# Wait for elements to load
wait = WebDriverWait(driver, timeout=5, poll_frequency=0.2, ignored_exceptions=ERRORS)

# Select English language
wait.until(ec.element_to_be_clickable((By.ID, "langSelect-EN"))).click()

# Click the cookie
wait.until(ec.element_to_be_clickable((By.ID, "bigCookie")))

# Click the cookies button
wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Got it!"))).click()

# Main button
cookie_btn = driver.find_element(By.ID, "bigCookie")

# Add a timeout
timeout_start = time.time()
prod_select_time = timeout_start + 5
total_cookies = 0.0


# Keep going until the time limit

while time.time() < timeout_start + RUNTIME:
    cookie_btn.click()

    if time.time() >= prod_select_time:
        products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled")

        if len(products) > 0:
            last_prod = products[-1]
            last_prod_price = last_prod.find_element(By.ID, f"productPrice{len(products) - 1}").text
            last_prod_price = int(last_prod_price.replace(",", ""))
            total_cookies += last_prod_price

            last_prod.click()

            prod_select_time += SELECT_TIME

remaining_cookies = driver.find_element(By.ID, "cookies").text
remaining_cookies_count = remaining_cookies.split(" ", 1)[0]
total_cookies += int(remaining_cookies_count.replace(",", ""))

print(f"cookies/second : {round(total_cookies / RUNTIME, 1)}")

driver.close()


