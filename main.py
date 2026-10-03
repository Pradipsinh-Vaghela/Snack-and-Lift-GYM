import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException

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
time.sleep(0.5)

email = driver.find_element(By.ID, "email-input")
password = driver.find_element(By.ID, "password-input")
login = driver.find_element(By.ID, "submit-button")

email.send_keys(ACCOUNT_EMAIL)
password.send_keys(ACCOUNT_PASSWORD)
login.click()

# Wait for schedule page to load
wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

# ---------------- Class Booking: Book Upcoming Tuesday Class  ----------------

booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

for Booking in class_cards:
    day_group = Booking.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        # Check if this is a 6pm classis
        time_text = Booking.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = Booking.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = Booking.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            # ---------------- Class Booking ----------------
            class_info = f"{class_name} {day_title}"

            if button.text == "Booked":
                print(f"✓ Already Booked: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_info}")
            elif button.text == "Waitlisted":
                print(f"✓ Already on WaitListed: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_info}")
            elif button.text == "Book Class":
                button.click()
                booked_count += 1
                print(f"✓ Booked: {class_name} on {day_title}")
                processed_classes.append(f"[New Booking] {class_info}")
            elif button.text == "Join Waitlist":
                button.click()
                waitlist_count += 1
                print(f"✓ Joined waitlist for: {class_name} on {day_title}")
                processed_classes.append(f"[New Waitlist] {class_info}")
                time.sleep(0.5)

my_bookings_page = driver.find_element(By.ID, "my-bookings-link")
my_bookings_page.click()

total_bookings = booked_count+waitlist_count+already_booked_count
verified_count = 0

confirm_bookings = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
for booking in confirm_bookings:
    try:
        when_paragraph = booking.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = booking.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {class_name}")
            verified_count += 1
    except NoSuchElementException:
        pass

print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_bookings} bookings")
print(f"Found: {verified_count} bookings")

if total_bookings == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_bookings - verified_count} bookings")
