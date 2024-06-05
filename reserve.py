from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from time import sleep
import sys
from selenium.webdriver.common.by import By

#driver = webdriver.Chrome(executable_path='C:\Python312\Scripts')
chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome()
base_url="https://www.thaiticketmajor.com/concert/"
userdetail_file="userdetail.json"
count=0
with open(userdetail_file, 'r') as f:
    user = json.load(f)
email=user["email"]
password=user["pwd"]
zone=user["zone"]
concert=user["concert"]
seat=int(user["seats"])
zone_list=0
show=int(user["show"])
next_zone_index=1

def setUp():
    driver.maximize_window()
    driver.get(base_url)
    driver.implicitly_wait(30)

def prepUserData():
    print("email=", email)
    print("password=", password)
    print("zone=", zone)
    print("concert=", concert)
    print("seat=", seat)
    print("show=", show)
    

def Login():
    # driver.find_element_by_xpath("//*[@class='btn-signin item d-none d-lg-inline-block']").click()
    print("login initiated")
    sleep(5)
    print("pass 100 seconds")
    login_btn = driver.find_element(By.XPATH, "//*[@class='btn-signin item d-none d-lg-inline-block']").click()
    print("found login button element by XPATH: ", login_btn)
    username = driver.find_element(By.NAME, "username")
    print("found username element by ID: ", username)
    username.send_keys(email)
    pwd = driver.find_element(By.NAME, "password")
    pwd.send_keys(password)
    sleep(5000)
    driver.find_element_by_xpath("//button[@class='btn-red btn-signin']").click()
    sleep(2)
    driver.implicitly_wait(50)
    cur_url=driver.current_url
    while cur_url == base_url:
        driver.find_element_by_partial_link_text(f"{concert}").click()
        driver.implicitly_wait(30)
        cur_url=driver.current_url
    driver.implicitly_wait(30)

def SelectShow():
    row=len(driver.find_elements_by_xpath("//div[@class='box-event-list']/div[2]/div"))
    #select round
    driver.find_element_by_xpath(f"//div[@class='box-event-list']/div[2]/div[{show}]/div[2]/span[1]/a[1]").click()
    driver.implicitly_wait(30)
        

    selected=driver.find_element_by_xpath(f"//*[@id='rdId']/option[1]").text
    # if after click and round is not selected
    if  selected=="เลือกรอบการแสดง / Select round":
        driver.find_element_by_id("rdId").click()
        driver.implicitly_wait(30)
        driver.find_element_by_xpath(f"//*[@div='select-date fix-me']/option[{show+1}]").click()
        driver.implicitly_wait(30)


def SelectZone(zone=zone):    
    global zone_list
    list_zone=driver.find_elements_by_xpath(f"//*[@name='uMap2Map']/area")
    row=zone_list=len(list_zone)
    index=0
    cur_url=nextUrl=driver.current_url
    print(f"Zone:{zone}")
    for i in range(1,row+1):
        result=find(zone,list_zone[i-1].get_attribute("href"))
        if result:
            index=i
            break
    while cur_url == nextUrl:
        driver.find_element_by_xpath(f"//*[@name='uMap2Map']/area[{index}]").click()
        driver.implicitly_wait(30)
        nextUrl=driver.current_url

def find(msg,link):
    get_zone=link.split('#')
    if msg == get_zone[2]:
        return True
    else:
        return False


        

def SelectSeat(number=seat):
    global count
    row=len(driver.find_elements_by_xpath("//*[@id='tableseats']/tbody[1]/tr"))
    for i in range(1,row+1):
        column=len(driver.find_elements_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td"))
        for j in range(2,column+1):
            text=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").text
            nrow=driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").get_attribute("title")
            if text==" ":
                print(f"seats:{nrow} not available")
            if text!=" " and count<number and text!="":
                driver.find_element_by_xpath(f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]").click()
                count+=1
            if count==number:
                break
        if count==number:
                break
    if count!=0:
        confirm_ticketprotect()

#if your zone not have any seat.
def go_to_next_zone():
    global next_zone_index
    while next_zone_index<=zone_list:
        driver.find_element_by_partial_link_text("ย้อนกลับ / Back").click()
        driver.implicitly_wait(40)
        driver.find_element_by_partial_link_text("ที่นั่งว่าง / Seats Available").click()
        driver.implicitly_wait(30)
        for j in range(2,zone_list+1):
            amount=driver.find_element_by_xpath(f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[2]").text
            i=driver.find_element_by_xpath(f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[1]").text
            if amount!="0" or amount=="Available":
                SelectZone(i)
                SelectSeat()
            next_zone_index+=1
    if count==0:
        print(f"Sorry, this concert don't have any seat for you.")
        sys.exit()


    

def confirm_ticketprotect():
    driver.find_element_by_partial_link_text("ยืนยันที่นั่ง / Book Now").click()
    driver.implicitly_wait(50)
    driver.find_element_by_partial_link_text("Continue").click()
    driver.implicitly_wait(40)
        

 

setUp()
prepUserData()
Login()
SelectShow()
SelectZone(zone)
SelectSeat()
if count==0:
    go_to_next_zone()
