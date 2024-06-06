from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

zone = "A1"
url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"

opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)
driver.get(url)
round=len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
print("\n")
print("round:====================", round)
print("\n")

def SelectZone(zone=zone):    
    global zone_list
    list_zone = driver.find_elements(By.XPATH, "//*[@name='uMap2Map']/area")
    # get zone numbers
    row = zone_list = len(list_zone)
    index = 0
    cur_url = nextUrl = driver.current_url
    print(f"Zone: {zone}")
    for i in range(1, row + 1):
        result = find(zone, list_zone[i - 1].get_attribute("href"))
        if result:
            index = i
            break
    while cur_url == nextUrl:
        driver.find_element(By.XPATH, f"//*[@name='uMap2Map']/area[{index}]").click()
        driver.implicitly_wait(30)
        nextUrl = driver.current_url

def find(msg, link):
    get_zone = link.split('#')
    if msg == get_zone[2]:
        return True
    else:
        return False
    

SelectZone()