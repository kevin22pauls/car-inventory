from selenium import webdriver

def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:3000/search.html")
    return driver
