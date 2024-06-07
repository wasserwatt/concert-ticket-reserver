from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By

opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)

url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"


print("Checking for pop-up error")
try:
        # Check if the error message is displayed
        error_message = driver.find_element(By.ID, 'alertmessage')
        if error_message.is_displayed():
                # Click the close button
                close_button = driver.find_element(By.XPATH, '//button[text()="Close"]')
                close_button.click()
                print("Error message found and closed")
                # Select other seats and try to confirm again
                # go_to_next_zone()
                # confirm_seats()
except NoSuchElementException:
        # If the error message is not found, do nothing
        print("Error message not found")
        pass



