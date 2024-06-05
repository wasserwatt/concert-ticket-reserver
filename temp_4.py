# PYTHON Example
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"

opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)
driver.get(url)
row=len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
print('row:====================', row)
selected = driver.find_element(By.XPATH, "//*[@id=\"section-event-round\"]/div/div[2]/div[3]/div[2]/div/div[2]/span/a").text
print("type of selected", type(selected))


# Zone selection
# Wait until the buttons are present
wait = WebDriverWait(driver, 10)
buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn']")))
buttons[1].click()
sleep(2)

seat = driver.find_element(By.XPATH, '//*[@id="Map4"]/area[5]')
print(f'Element found: {seat}')
seat.click()






# buy_btn = element = driver.find_element(By.ID, "rdId")
# buy_btn.click()
# print("buy_btn clicked")

# if selected == "15:00":
#     driver.find_element(By.TAG_NAME, "a").click()
#     driver.implicitly_wait(30)
#     driver.find_element(By.XPATH, f"//*[@div='select-date fix-me']/option[{1 + 1}]").click()
#     driver.implicitly_wait(30)

# Wait for the element to be present
# wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
# buy_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='https://booking.thaiticketmajor.com/booking/3m/zones.php?query=999&amp;rdId=77811']")))
