from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.get("http://localhost:3000/search.html")  # Update if your server runs at a different port/path

# Fill the search form
# driver.find_element(By.ID, "modelName").send_keys("Civic")
# driver.find_element(By.ID, "make").send_keys("Honda")
driver.find_element(By.ID, "year").send_keys("2015")
# driver.find_element(By.ID, "kms").send_keys("50000")
# driver.find_element(By.ID, "mileage").send_keys("15")

# Submit the form
driver.find_element(By.CLASS_NAME, "btn-search").click()

# Wait for search results to be displayed
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".results-table"))
)

# Select first available checkbox (if any)
checkboxes = driver.find_elements(By.NAME, "car_ids[]")
if checkboxes:
    for i in range(10):
        checkboxes[i].click()

    driver.find_element(By.ID, "showDetails").click()
else:
    print("No results to select.")
    driver.quit()
    exit()

# Wait for EMI page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "emiDetailsContainer"))
)

# Allow jQuery and AJAX to populate table
time.sleep(3)

# Check that EMI table is shown
emi_table = driver.find_element(By.CLASS_NAME, "emi-table")
rows = emi_table.find_elements(By.TAG_NAME, "tr")

if len(rows) > 1:
    print("✅ EMI Details loaded successfully.")
    # Optionally click "Book Test Drive" for first available car
    try:
        book_btn = driver.find_element(By.CLASS_NAME, "btn-book")
        book_btn.click()

        # Wait for redirect or alert
        time.sleep(5)
        print("🚗 Test Drive Booking Clicked.")
    except Exception as e:
        print("No bookable car available or booking failed.", str(e))
else:
    print("❌ No EMI details found.")

driver.quit()
