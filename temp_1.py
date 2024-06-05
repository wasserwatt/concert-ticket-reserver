from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# driver setup
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()


# login

driver.maximize_window()
driver.get("https://pace.coe.int/en/aplist/committees/9/commission-des-questions-politiques-et-de-la-democratie")
sleep(5)
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[1]/div/div[1]/div/div/iframe")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))).click()
sleep(5000)