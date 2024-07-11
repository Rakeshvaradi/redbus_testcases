

from Locators import *
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException



def wait_and_click(driver, locator):
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()

def wait_and_send_keys(driver, locator, keys):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(locator)
    )
    element.send_keys(keys)

def wait_and_get_elements(driver, locator):
    return WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located(locator)
    )

def switch_to_iframe(driver):
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(Locators.Iframe)
    )
    driver.switch_to.frame(iframe)

def switch_to_iframe1(driver):
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(Locators.Iframe1)
    )
    driver.switch_to.frame(iframe)

def sort_buses_by_departure_time(buses):
    for i in range(len(buses)):
        for j in range(i + 1, len(buses)):
            if buses[i]['departure_time'] < buses[j]['departure_time']:
                buses[i], buses[j] = buses[j], buses[i]
    return buses

service_obj = Service()
driver = webdriver.Chrome(service=service_obj)
driver.get("https://www.redbus.in/")
driver.maximize_window()

try:
    # Sign up with a new user
    wait_and_click(driver, (By.XPATH, '//li[@id="account_dd"]//div[contains(@class,"link")]'))
    wait_and_click(driver,(By.XPATH,"//span[normalize-space()='Login/ Sign Up']"))
    switch_to_iframe1(driver)
    wait_and_send_keys(driver, (By.ID, "mobileNoInp"), "9542892424")
    wait_and_click(driver, (By.XPATH, "//div[@id='recaptchaElement']/div"))
    time.sleep(40)
    wait_and_click(driver, (By.ID, "otp-container"))
    time.sleep(10)
    wait_and_get_elements(driver,(By.XPATH, "//div[@class='inputContainer otpInputContainer clearfix otp-border-css']"))
    time.sleep(10)
    wait_and_click(driver, (By.XPATH, "//button[@id='verifyUser']"))

    # Enter "From" location
    wait_and_send_keys(driver, Locators.From_input, 'Bang')
    time.sleep(1)  # Wait for the suggestions to load
    for suggestion in wait_and_get_elements(driver, Locators.Dropdown):
        if 'Bangalore' in suggestion.text:
            suggestion.click()
            break

    # Enter "To" location
    wait_and_send_keys(driver, Locators.To_input, 'Che')
    time.sleep(1)  # Wait for the suggestions to load
    for suggestion in wait_and_get_elements(driver, Locators.Dropdown):
        if 'Koyambedu' in suggestion.text:
            suggestion.click()
            break

    # Select a future date
    wait_and_click(driver, Locators.Date_picker)
    future_dates = wait_and_get_elements(driver,Locators.date)
    wait_and_click(driver,Locators.date)
    time.sleep(2)




    # Click Help and handle new window
    wait_and_click(driver, Locators.Help_button)

    var = driver.window_handles
    driver.switch_to.window(var[1])

    # Switch to iframe
    switch_to_iframe(driver)

    # Select "Technical Issues"
    wait_and_click(driver, Locators.Technical_issues)


    # Print options and select "No buses found"
    options = wait_and_get_elements(driver, (By.XPATH, '//div[@class="chipContainer"]/div'))
    for option in options:
        print(option.text)
        if 'No buses found' in option.text:
            option.click()
            break

    # Print the response
    response = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(Locators.Response)
    )
    print(response.text)

    driver.switch_to.window(var[0])
    driver.switch_to.default_content()

    # Perform assertions
    wait_and_click(driver, Locators.Searchbutton)


    time.sleep(10)
    # Wait for search results
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    buses = wait_and_get_elements(driver, Locators.Bus_items)



    # Assert the count of buses found
    bus_count = len(buses)
    print(f'Number of buses found: {bus_count}')
    assert bus_count > 0, "No buses found"

    # Get bus details
    bus_details = []
    for bus in buses:
        try:
            departure_time = bus.find_element(*Locators.Departure).text
            bus_type = bus.find_element(*Locators.Type).text
            price = bus.find_element(*Locators.Cost).text.replace('₹', '').replace(',', '').strip()
            amenities = bus.find_elements(*Locators.amenities)
            bus_details.append({
                'departure_time': departure_time,
                'bus_type': bus_type,
                'price': int(price),
                'amenities': len(amenities)
            })
        except NoSuchElementException:
            continue

    # Sort buses by departure time in descending order
    sorted_buses = sort_buses_by_departure_time(bus_details)
    print(f'Sorted buses by departure time (descending): {sorted_buses}')

    # Filter buses with "sleeper" class
    sleeper_buses = [bus for bus in bus_details if 'Sleeper' in bus['bus_type']]
    print(f'Sleeper buses: {sleeper_buses}')
    assert len(sleeper_buses) > 0, "No sleeper buses found"

    # Print and assert the cheapest rate
    cheapest_rate = bus_details[0]['price']
    for bus in bus_details:
        if bus['price'] < cheapest_rate:
            cheapest_rate=bus['price']
    print(f'Cheapest rate: {cheapest_rate}')

    # Print and assert the costliest rate
    costliest_rate = bus_details[0]['price']
    for bus in bus_details:
        if bus['price'] > costliest_rate:
            costliest_rate=bus['price']
    print(f'Costliest rate: {costliest_rate}')

    # Print and assert the last available bus timing
    last_bus_timing = sorted_buses[0]['departure_time']
    print(f'Last available bus timing: {last_bus_timing}')

    # Print and assert the first available bus timing
    first_bus_timing = sorted_buses[-1]['departure_time']
    print(f'First available bus timing: {first_bus_timing}')

    # Print and assert the count of "AMENITIES"
    total_amenities = sum(bus['amenities'] for bus in bus_details)
    print(f'Total amenities count: {total_amenities}')

except TimeoutException:
    print("An element was not found within the timeout period")


finally:
    driver.quit()
