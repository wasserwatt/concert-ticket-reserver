from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import UnexpectedAlertPresentException

opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)

url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"


print("Checking for browser alert")
try:
    # Wait for the alert to be present
    WebDriverWait(driver, 10).until(EC.alert_is_present())

    # Switch to the alert and accept it
    alert = driver.switch_to.alert
    alert.accept()
    print("Alert found and accepted")
except NoAlertPresentException:
    # If no alert is present, do nothing
    print("Alert not found")

 