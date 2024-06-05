# PYTHON Example
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"

opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)
driver.get(url)
row=len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
print('row:====================', row)
selected = driver.find_element(By.XPATH, "//*[@id=\"section-event-round\"]/div/div[2]/div[3]/div[2]/div/div[2]/span/a").text
print('selected:====================', selected)
if selected == "เลือกรอบการแสดง / Select round":
    driver.find_element(By.ID, "rdId").click()
    driver.implicitly_wait(30)
    driver.find_element(By.XPATH, f"//*[@div='select-date fix-me']/option[{1 + 1}]").click()
    driver.implicitly_wait(30)