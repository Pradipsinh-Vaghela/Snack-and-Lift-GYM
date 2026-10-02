import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# ---------------- Setup, Chrome Profile and Basic Navigation -------------

# Create Chrome Profile and create account manually. Put YOUR email and password here
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

# ---------------- Automated Login ----------------

wait = WebDriverWait(driver, 2)

login_page = driver.find_element(By.ID, "login-button")
login_page.click()

email = driver.find_element(By.ID, "email-input")
password = driver.find_element(By.ID, "password-input")
login = driver.find_element(By.ID, "submit-button")

email.send_keys(ACCOUNT_EMAIL)
password.send_keys(ACCOUNT_PASSWORD)
login.click()

# Wait for schedule page to load
wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# ---------------- Class Booking: Book Upcoming Tuesday Class  ----------------

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    # Check if this is a Tuesday
    if "Tue" in day_title:
        # Check if this is a 6pm class
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            # Get the class name
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text

            # Find and click the book button
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

# ---------------- Class Booking: Checking if a class is already booked ----------------
            if button.text == "Booked":
                print(f"✓ Already Booked: {class_name} on {day_title}")
            elif button.text == "Waitlisted":
                print(f"✓ Already on WaitListed: {class_name} on {day_title}")
            elif button.text == "Book Class":
                button.click()
                print(f"✓ Booked: {class_name} on {day_title}")
            elif button.text == "Join Waitlist":
                button.click()
                print(f"✓ Joined waitlist for: {class_name} on {day_title}")
            break
