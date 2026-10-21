import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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

# --------------------- Functions ----------------------------

def retry(func, retries=7, description=None):
    for attempt in range(retries):
        try:
            print(f"Trying {description}... Attempt {attempt+1}")
            func()
            print(f"{description} Successful ✅")
            return

        except TimeoutException:
            print(f"{description} Failed ⛔")

            if attempt == retries-1:
                print(f"{description} Failed after {retries} attempts.")
                raise
            time.sleep(2)

def login():
    driver.refresh()
    login_page = driver.find_element(By.ID, "login-button")
    login_page.click()
    time.sleep(0.5)

    email = driver.find_element(By.ID, "email-input")
    password = driver.find_element(By.ID, "password-input")
    login_btn = driver.find_element(By.ID, "submit-button")

    email.send_keys(ACCOUNT_EMAIL)
    password.send_keys(ACCOUNT_PASSWORD)
    login_btn.click()

    # Wait for schedule page to load
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

def book_class(booking_button):
    booking_button.click()
    wait.until(lambda d: booking_button.text == "Booked")

# ---------------------  Attempt Login  -----------------------------

wait = WebDriverWait(driver, 2)
retry(login, retries=7, description="Login")

# ---------------- Class Booking: Book Upcoming Tuesday Class  ----------------

booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for booking in class_cards:
    day_group = booking.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        # Check if this is a 6pm classis
        time_text = booking.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = booking.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            book_btn = booking.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            # ---------------- Class Booking ----------------
            class_info = f"{class_name} {day_title}"

            if book_btn.text == "Booked":
                print(f"✓ Already Booked: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_info}")
            elif book_btn.text == "Waitlisted":
                print(f"✓ Already on WaitListed: {class_name} on {day_title}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_info}")
            elif book_btn.text == "Book Class":
                retry(lambda: book_class(book_btn), description="Booking")
                if book_btn.text == "Booked":
                    booked_count += 1
                    print(f"✓ Booked: {class_name} on {day_title}")
                    processed_classes.append(f"[New Booking] {class_info}")
                else:
                    print("Booking Failed ⛔")
                time.sleep(0.5)

            elif book_btn.text == "Join Waitlist":
                retry(lambda: book_class(book_btn), description="Waitlisting")
                if book_btn.text == "Waitlisted":
                    waitlist_count += 1
                    print(f"✓ Joined waitlist for: {class_name} on {day_title}")
                    processed_classes.append(f"[New Waitlist] {class_info}")
                else:
                    print("Booking Failed ⛔")
                time.sleep(0.5)


# ---------------- Check Class Booking: Book Upcoming Tuesday Class  ----------------

my_bookings_page = driver.find_element(By.ID, "my-bookings-link")
my_bookings_page.click()

total_bookings = 2
verified_count = 0

confirm_bookings = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
print("\n\nVerifying...")
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
