from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("http://localhost:3000/search.html")

try:
    # Step 1: Fill the search form
    driver.find_element(By.ID, "kms").send_keys("50000")
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    # Step 2: Wait for search results
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".results-table"))
    )
    time.sleep(5)

    # Step 3: Select checkboxes for cars
    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            time.sleep(0.5)

            checkboxes[i].click()

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

        # Step 6: Fill out the booking form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "testDriveForm"))
        )

        driver.find_element(By.ID, "name").send_keys("John Doe")
        driver.find_element(By.ID, "mobile").send_keys("9876543210")
        driver.find_element(By.ID, "email").send_keys("john@example.com")
        time.sleep(5)

        license_dropdown = driver.find_element(By.ID, "license")
        for option in license_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text.strip() == "Yes":
                option.click()
                break

        # Step 7: Submit the form
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Step 8: Handle JS alert
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"📢 Alert Message: {alert.text}")
            alert.accept()
        except:
            print("⚠️ No alert appeared after form submission.")

        # Step 9: Confirm booking
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "confirmation-container"))
        )
        confirmation_msg = driver.find_element(By.TAG_NAME, "h1").text
        if "booked successfully" in confirmation_msg.lower():
            print("🎯 Test drive successfully booked and confirmed.")
        else:
            print("❌ Unexpected confirmation message.")

        # Step 10: Click Back to Search
        driver.find_element(By.LINK_TEXT, "Back to Search").click()
        print("🔁 Returned to search page.")

    else:
        print("❌ No car results found to select.")

except Exception as e:
    print("🔥 Test failed with error:", str(e))

finally:
    time.sleep(5)
    driver.quit()
