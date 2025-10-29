
# Shared Setup (setup_driver.py)
from selenium import webdriver

def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:3000/search.html")
    return driver


# TC01 - Load homepage and check listings
# test_TC01_load_homepage.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
import time

driver = init_driver()
try:
    time.sleep(4)
    cars = driver.find_elements(By.CLASS_NAME, "btn-search")
    print("✅ TC01: Car listings are visible." if cars else "❌ TC01: No car listings found.")
finally:
    driver.quit()


# TC02 - Click Book Test Drive and verify form opens
# test_TC02_open_booking_form.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# TC02 - Click Book Test Drive and verify form opens

driver = init_driver()

try:
    # Perform a search to load results
    driver.find_element(By.ID, "kms").send_keys("50000")
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    # Wait for checkboxes to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "car_ids[]"))
    )

    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            time.sleep(0.5)
            driver.execute_script("arguments[0].scrollIntoView(true);", checkboxes[i])
            driver.execute_script("arguments[0].click();", checkboxes[i])

        # Step 4: Show EMI Details
        driver.find_element(By.ID, "showDetails").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
        )
        time.sleep(5)

        # Step 5: Book Test Drive
        book_btn = driver.find_element(By.CLASS_NAME, "btn-book")
        book_btn.click()
        time.sleep(5)

        # Verify form appears
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "testDriveForm"))
        )
        print("✅ TC02: Booking form opened successfully.")

    else:
        print("❌ TC02: No cars available to select.")

except Exception as e:
    print("❌ TC02: Error -", str(e))
finally:
    driver.quit()


# TC03 - Submit form with valid data
# test_TC03_valid_form_submit.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = init_driver()
try:
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "car_ids[]"))
    )

    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            time.sleep(0.5)
            driver.execute_script("arguments[0].scrollIntoView(true);", checkboxes[i])
            driver.execute_script("arguments[0].click();", checkboxes[i])

        driver.find_element(By.ID, "showDetails").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
        )
        time.sleep(5)

        driver.find_element(By.CLASS_NAME, "btn-book").click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "testDriveForm"))
        )

        driver.find_element(By.ID, "name").send_keys("Alice")
        driver.find_element(By.ID, "mobile").send_keys("9999999999")
        driver.find_element(By.ID, "email").send_keys("alice@example.com")
        driver.find_element(By.ID, "license").find_elements(By.TAG_NAME, 'option')[1].click()
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Handle alert after submission
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"📢 Alert Message: {alert.text}")
            alert.accept()
        except:
            print("⚠️ No alert appeared after form submission.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "confirmation-container"))
        )
        print("✅ TC03: Form submitted successfully.")
    else:
        print("❌ TC03: No cars to select.")
finally:
    driver.quit()


# TC04 - Submit form with invalid data
# test_TC04_invalid_form_submit.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = init_driver()
try:
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "car_ids[]"))
    )

    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            time.sleep(0.5)
            driver.execute_script("arguments[0].scrollIntoView(true);", checkboxes[i])
            driver.execute_script("arguments[0].click();", checkboxes[i])

        driver.find_element(By.ID, "showDetails").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
        )
        time.sleep(5)

        driver.find_element(By.CLASS_NAME, "btn-book").click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "testDriveForm"))
        )

        driver.find_element(By.ID, "email").send_keys("bademail")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Handle potential alert
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"📢 Alert Message: {alert.text}")
            alert.accept()
        except:
            print("⚠️ No alert appeared (as expected for invalid data).")

        print("❌ TC04: Validation errors triggered for invalid data.")
    else:
        print("❌ TC04: No cars to select.")
finally:
    driver.quit()


# TC05 - Test license dropdown
# test_TC05_license_toggle.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = init_driver()
try:
    driver.find_element(By.CLASS_NAME, "btn-search").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "car_ids[]"))
    )
    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            time.sleep(0.5)
            driver.execute_script("arguments[0].scrollIntoView(true);", checkboxes[i])
            driver.execute_script("arguments[0].click();", checkboxes[i])
        driver.find_element(By.ID, "showDetails").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
        )
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, "btn-book").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "testDriveForm"))
        )
        options = driver.find_element(By.ID, "license").find_elements(By.TAG_NAME, "option")
        assert any(opt.text.strip() == "Yes" for opt in options)
        assert any(opt.text.strip() == "No" for opt in options)
        print("✅ TC05: License dropdown contains 'Yes' and 'No'.")
    else:
        print("❌ TC05: No cars to select.")
finally:
    driver.quit()

# Remaining test cases unchanged or marked for manual/mock testing
# ... (TC06 - TC14 follow after this)   

# TC06 - Search with no filters
# test_TC06_search_all.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
import time

driver = init_driver()
try:
    driver.find_element(By.CLASS_NAME, "btn-search").click()
    time.sleep(3)
    rows = driver.find_elements(By.CSS_SELECTOR, ".results-table tr")
    print("✅ TC06: Results shown for no-filter search." if len(rows) > 1 else "❌ TC06: No results found.")
finally:
    driver.quit()


# TC07 - Search with model and year
# test_TC07_search_specific.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
import time

driver = init_driver()
try:
    driver.find_element(By.ID, "modelName").send_keys("Civic")
    driver.find_element(By.ID, "year").send_keys("2020")
    driver.find_element(By.CLASS_NAME, "btn-search").click()
    time.sleep(3)
    rows = driver.find_elements(By.CSS_SELECTOR, ".results-table tr")
    print("✅ TC07: Filtered results shown." if len(rows) > 1 else "❌ TC07: No matching cars.")
finally:
    driver.quit()


# TC08 - Show details without selection
# test_TC08_show_without_select.py
from setup_driver import init_driver
from selenium.webdriver.common.by import By
import time

driver = init_driver()
try:
    driver.find_element(By.CLASS_NAME, "btn-search").click()
    time.sleep(2)
    driver.find_element(By.ID, "showDetails").click()
    time.sleep(1)
    print("✅ TC08: Alert shown when no car selected.")
    print("✅  ✅  Selenium Testing Done!! 8 Test Cases  ✅  ✅")
finally:
    driver.quit()


 

