from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open your local or hosted webpage
driver.get("http://localhost:3000/search.html")  # Change this to your actual URL

try:
    # Wait until the form is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "searchForm"))
    )

    # Fill the form fields
    driver.find_element(By.ID, "modelName").send_keys("innova")
    # driver.find_element(By.ID, "make").send_keys("Honda")
    # driver.find_element(By.ID, "year").send_keys("2015")
    # driver.find_element(By.ID, "kms").send_keys("50000")
    # driver.find_element(By.ID, "mileage").send_keys("18")

    # Submit the form
    driver.find_element(By.CLASS_NAME, "btn-search").click()

    # Wait for results to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "resultsContainer"))
    )

    # Select a car checkbox if available
    checkboxes = driver.find_elements(By.NAME, "car_ids[]")
    if checkboxes:
        checkboxes[0].click()  # Select the first result

        # Click 'Show Details' button
        driver.find_element(By.ID, "showDetails").click()
    else:
        print("No car results found.")

    time.sleep(3)  # Wait to visually inspect if needed

finally:
    driver.quit()
