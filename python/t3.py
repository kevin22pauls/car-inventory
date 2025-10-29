from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("http://localhost:3000/search.html")

try:
    # Fill search form
    driver.find_element(By.ID, "kms").send_keys("50000")
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    # Wait for results
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".results-table"))
    )
    time.sleep(3)

    # Select checkboxes
    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        for i in range(min(len(checkboxes), 20)):
            checkboxes[i].click()

        driver.find_element(By.ID, "showDetails").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
        )

        time.sleep(3)

        emi_table = driver.find_element(By.CLASS_NAME, "emi-table")
        rows = emi_table.find_elements(By.TAG_NAME, "tr")

        if len(rows) > 1:
            print("✅ EMI Details loaded.")

            try:
                book_btn = driver.find_element(By.CLASS_NAME, "btn-book")
                book_btn.click()
                time.sleep(2)

                # Try browser alert
                try:
                    alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert.accept()
                    print("✅ JS alert accepted.")
                except:
                    print("No JS alert shown.")

                # Wait for confirmation page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "confirmation-container"))
                )
                time.sleep(3)

                # Verify message
                heading = driver.find_element(By.TAG_NAME, "h1").text
                if "booked successfully" in heading:
                    print("🎉 Booking confirmation shown.")

                # Optionally click "Back to Search"
                back_btn = driver.find_element(By.LINK_TEXT, "Back to Search")
                back_btn.click()
                print("🔁 Returned to search page.")

            except Exception as e:
                print("⚠️ Booking failed:", str(e))
        else:
            print("❌ EMI table is empty.")
    else:
        print("❌ No results to select.")

except Exception as e:
    print("🔥 Error:", str(e))

finally:
    driver.quit()
