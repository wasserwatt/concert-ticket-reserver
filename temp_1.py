from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import sys

# set up
url = "https://booking.thaiticketmajor.com/booking/3m/zones.php?query=999&rdId=77811"
opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)
zone_list=0
# Constants
base_url = "https://www.thaiticketmajor.com/concert/"
userdetail_file = "userdetail.json"
count = 0

# Load user details
with open(userdetail_file, 'r') as f:
    user = json.load(f)
email = user["email"]
password = user["pwd"]
zone = user["zone"]
concert = user["concert"]
seat = int(user["seats"])
zone_list = 0
show = int(user["show"])
next_zone_index = 1

def setUp():
    #driver.maximize_window()
    #driver.get(base_url)
    #driver.implicitly_wait(30)
    pass

def Login():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@class='btn-signin item d-none d-lg-inline-block']"))
    ).click()
    sleep(1)
    username = driver.find_element(By.ID, "username")
    username.send_keys(email)
    pwd = driver.find_element(By.ID, "password")
    pwd.send_keys(password)
    driver.find_element(By.XPATH, "//button[@class='btn-red btn-signin']").click()
    sleep(2)
    driver.implicitly_wait(50)
    cur_url = driver.current_url
    while cur_url == base_url:
        driver.find_element(By.PARTIAL_LINK_TEXT, concert).click()
        driver.implicitly_wait(30)
        cur_url = driver.current_url
    driver.implicitly_wait(30)

def SelectShow():
    row = len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
    # Select round
    driver.find_element(By.XPATH, f"//div[@class='box-event-list']/div[2]/div[{show}]/div[2]/span[1]/a[1]").click()
    driver.implicitly_wait(30)

    selected = driver.find_element(By.XPATH, "//*[@id='rdId']/option[1]").text
    # If round is not selected after click
    if selected == "เลือกรอบการแสดง / Select round":
        driver.find_element(By.ID, "rdId").click()
        driver.implicitly_wait(30)
        driver.find_element(By.XPATH, f"//*[@div='select-date fix-me']/option[{show + 1}]").click()
        driver.implicitly_wait(30)

def open_and_go_to_site():
    driver.get(url)
    round=len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
    print("\n")
    print("round:====================", round)
    print("\n")

def SelectZone(zone=zone):    
    global zone_list
    list_zone = driver.find_elements(By.XPATH, "//*[@name='uMap2Map']/area")
    # Get zone numbers
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

def SelectSeat(number=seat):
    global count
    row = len(driver.find_elements(By.XPATH, "//*[@id='tableseats']/tbody[1]/tr"))
    for i in range(1, row + 1):
        column = len(driver.find_elements(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td"))
        for j in range(2, column + 1):
            text = driver.find_element(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").text
            nrow = driver.find_element(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").get_attribute("title")
            if text == " ":
                print(f"seats: {nrow} not available")
            if text != " " and count < number and text != "":
                driver.find_element(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").click()
                count += 1
            if count == number:
                break
        if count == number:
            break
    if count != 0:
        confirm_ticketprotect()

# If your zone does not have any seat.
def go_to_next_zone():
    global next_zone_index
    while next_zone_index <= zone_list:
        driver.find_element(By.PARTIAL_LINK_TEXT, "ย้อนกลับ / Back").click()
        driver.implicitly_wait(40)
        driver.find_element(By.PARTIAL_LINK_TEXT, "ที่นั่งว่าง / Seats Available").click()
        driver.implicitly_wait(30)
        for j in range(2, zone_list + 1):
            amount = driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[2]").text
            i = driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[1]").text
            if amount != "0" or amount == "Available":
                SelectZone(i)
                SelectSeat()
            next_zone_index += 1
    if count == 0:
        print(f"Sorry, this concert doesn't have any seat for you.")
        sys.exit()

def confirm_ticketprotect():
    driver.find_element(By.PARTIAL_LINK_TEXT, "ยืนยันที่นั่ง / Book Now").click()
    driver.implicitly_wait(50)
    driver.find_element(By.PARTIAL_LINK_TEXT, "Continue").click()
    driver.implicitly_wait(40)

# Run the functions
setUp()
#Login()
#SelectShow()
open_and_go_to_site()
SelectZone(zone)
#SelectSeat()
if count == 0:
    go_to_next_zone()
