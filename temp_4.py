from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

# set up
url = "https://www.thaiticketmajor.com/concert/bouncy-boun-concert.html"
opts = Options()
opts.add_experimental_option('debuggerAddress', 'localhost:1111')
driver = webdriver.Chrome(options=opts)
# Global variable to store available zones and seats
available_seats = {}
preferred_zones = ['A1', 'A2', 'A3']
preferred_seats = 4

def open_and_go_to_site():
    driver.get(url)
    round=len(driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div"))
    print("\n")
    print("round:====================", round)
    print("\n")

def zone_selection():
    # Zone selection
    # Wait until the buttons are present
    wait = WebDriverWait(driver, 0.5)
    buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn']")))
    buttons[1].click()
    #sleep(2)
    # find wanted zone by css selector 
    # dynamic finding

    zone_number = "A1"  # Change this to the seat number you want
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'area[href="#fixed.php#{zone_number}"]')))
    zone = driver.find_element(By.CSS_SELECTOR, f'area[href="#fixed.php#{zone_number}"]')
    # seat = driver.find_element(By.CSS_SELECTOR, 'area[href="#fixed.php#A1"]')
    # find element by xpath
    # seat = driver.find_element(By.XPATH, '//*[@id="Map4"]/area[5]')
    print("\n")
    print(f'Element found: {zone}')
    zone.click()
    
def SelectSeat(number):
    count = 0
    max_seats_per_buy = 4
    
    # Ensure the number of seats requested doesn't exceed the maximum allowed
    if number > max_seats_per_buy:
        number = max_seats_per_buy

    rows = driver.find_elements(By.XPATH, "//*[@id='tableseats']/tbody[1]/tr")
    
    for i in range(1, len(rows) + 1):
        columns = driver.find_elements(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td")
        consecutive_seats = []
        
        for j in range(2, len(columns) + 1):
            cell = driver.find_element(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]")
            text = cell.text
            
            if text != " " and text != "":
                consecutive_seats.append(cell)
            else:
                consecutive_seats = []
                
            if len(consecutive_seats) == number:
                for seat in consecutive_seats:
                    seat.click()
                    count += 1
                
                if count == number:
                    break
                
        if count == number:
            break
    
    if count != 0:
        print("call confirm_ticketprotect()")
        #confirm_ticketprotect()
    else:
        print("Sorry, not enough consecutive seats are available.")

zone_list = 0
list_zone = driver.find_elements(By.XPATH, "//*[@name='uMap2Map']/area")
row=zone_list=len(list_zone)

def get_free_zone():
    global available_seats
    rows = driver.find_elements(By.XPATH, '//table[@class="table"]/tbody/tr')
    for row in rows:
        # Find the zone and number of seats in each row
        zone = row.find_element(By.XPATH, './td[1]').text
        seats = int(row.find_element(By.XPATH, './td[2]').text)

        # If the number of seats is greater than 0, print the zone and number of seats
        if seats >= preferred_seats:
            #available_seats[zone] = seats
            available_seats[zone] = {'seats': seats, 'row': row}
            #print(f"Zone {zone} has {seats} available seats.")

def go_to_next_zone():
    print("entered go_to_next_zone()")
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "popup-avail").click()
    driver.implicitly_wait(30)
    get_free_zone()
    # Try to find a preferred zone first
    for zone in preferred_zones:
        # If the zone is available, click the row and break the loop
        if zone in available_seats:
            available_seats[zone]['row'].click()
            SelectSeat(preferred_seats)
            break
    # If no preferred zone is available, go to the next available zone
    for zone, info in available_seats.items():
        info['row'].click()
        SelectSeat(preferred_seats)
        break
    

    # for j in range(2, row + 1):
    #     amount = driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[2]").text
    #     zone_id = driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{j}]/td[1]").text
    #     if amount != "0" or amount == "Available":
    #         zone_number = "H"  # Change this to the seat number you want
    #         zone = driver.find_element(By.CSS_SELECTOR, f'area[href="#fixed.php#{zone_number}"]')
    #         # seat = driver.find_element(By.CSS_SELECTOR, 'area[href="#fixed.php#A1"]')
    #         # find element by xpath
    #         # seat = driver.find_element(By.XPATH, '//*[@id="Map4"]/area[5]')
    #         print("\n")
    #         print(f'Element found: {zone}')
    #         zone.click()
    #         SelectSeat(4)
    #     next_zone_index += 1


def check_zone_availibility():
    # Find all elements with the class 'txt-label'
    elements = driver.find_elements(By.CSS_SELECTOR, 'span.txt-label')

    # Loop through the elements and print their text
    print("\n")
    for element in elements:
        print(f'Found element: {element}')
        print(f'The text is: {element.text}')

    if element.text == "NOT AVAILABLE":
        print("Seat not available")
        print("Switching to next zone")
        # Click the back button
        driver.back()
        go_to_next_zone()

    else:
        print("Seat available")
        print("Proceeding to seat selection")
        SelectSeat(preferred_seats)
        print("called select_seat()")


open_and_go_to_site()
zone_selection()
check_zone_availibility()
print(available_seats)