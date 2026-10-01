import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

ACCOUNT_EMAIL = "cipher@test.com"
ACCOUNT_PASSWORD = "cglider@143"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
# Generate Script to store password, preferences and settings on chrome.
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(chrome_options)

driver.get(GYM_URL)

wait = WebDriverWait(driver, 2)

login_page = driver.find_element(By.ID, "login-button")
login_page.click()

email = driver.find_element(By.ID, "email-input")
email.send_keys(ACCOUNT_EMAIL)

password = driver.find_element(By.ID, "password-input")
password.send_keys(ACCOUNT_PASSWORD)

login = driver.find_element(By.ID, "submit-button")
login.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))
