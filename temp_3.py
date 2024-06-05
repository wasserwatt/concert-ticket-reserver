# extra lib
import keyboard as kbd
import undetected_chromedriver as uc
# time lib
from time import sleep
# selenium lib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = uc.Chrome()
driver.maximize_window()
# driver.get('https://chat.openai.com/chat')  # my own test test site with max anti-bot protection
driver.get('https://www.thaiticketmajor.com/concert/')  # my own test test site with max anti-bot protection
sleep(2)
login_btn = driver.find_element(By.XPATH, "//*[@class='btn-signin item d-none d-lg-inline-block']").click()
username = driver.find_element(By.NAME, "username")
print("found username element by ID: ", username)

username.send_keys("pidpipa.s@gmail.com")
pwd = driver.find_element(By.NAME, "password")
pwd.send_keys("triplepea.22")
sleep(3)
# finding check box

# 1st method 
# NOT WORKING
# check_box = driver.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input')
# check_box.click()
# print("clicked on checkbox")

# 2nd method
# try:
#     iframe = driver.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input')  # Adjust XPath based on your site
#     driver.switch_to.frame(iframe)
#     print("switched to iframe")
# except:
#     pass    # If no iframe is found, proceed without switching

# 3rd method
sleep(5)
# find using xpath
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='Widget containing a Cloudflare security challenge']")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))).click()
# find using css selector
# WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()




# exit blocking 
sleep(5000) 