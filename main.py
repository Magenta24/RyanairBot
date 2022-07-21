import datetime
import time

from os.path import exists

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier

''' TO-DO
1. Making the date dynamic(not hard-coded)
2. Downloading prices of flights in 2 weeks to 1 month+2weeks
3. Creating client-server
    - the app will run on server
    - whenever the client will connect, the app will download report with flights data and there will be system notification
4. Checking flights' prices from all polish airports
'''

# create new webrowser window
window = webdriver.Firefox(executable_path=r'J:\geckodriver.exe')

# open a ryanair site
window.get("https://www.ryanair.com/pl/pl")

# accepting cookies
time.sleep(2)
cookies = window.find_element_by_xpath('/html/body/div/div/div[3]/button[2]')
cookies.click()

# selecting one-way trip
one_way_btn = window.find_element_by_xpath(
    "/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/fsw-trip-type-container/fsw-trip-type/fsw-trip-type-button[2]/button")
one_way_btn.click()

### entering departure city
departure_input = window.find_element_by_xpath("//*[@id='input-button__departure']")
departure_input.click()
time.sleep(1)

# choosing country - Poland
country_depart = window.find_element_by_xpath(
    "/html/body/ry-tooltip/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-origin-container/fsw-airports/fsw-countries/div[4]/div[8]/span")
country_depart.click()
time.sleep(1)

# choosing city - Krakow
city_depart = window.find_element_by_xpath(
    "/html/body/ry-tooltip/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-origin-container/fsw-airports/div/fsw-airports-list/div[2]/div[1]/fsw-airport-item[4]/span/span")
depart_city_name = city_depart.text
print(depart_city_name)
city_depart.click()
time.sleep(1)

### entering destination city
dest_input = window.find_element_by_xpath("//*[@id='input-button__destination']")
dest_input.click()
dest_input.click()
time.sleep(1)

# choosing country - Wielka Brytania
country_dest = window.find_element_by_xpath(
    "/html/body/ry-tooltip/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/fsw-countries/div[5]/div[8]/span")
country_dest.click()
time.sleep(1)

# # choosing city - Leeds
city_dest = window.find_element_by_xpath(
    "/html/body/ry-tooltip/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/div/fsw-airports-list/div[2]/div[1]/fsw-airport-item[8]")
dest_city_name = city_dest.text.split('/')[0]
print(dest_city_name)
city_dest.click()
time.sleep(1)

# choosing dates - now hard-coded
day_of_month = datetime.datetime.today().day
print(day_of_month)
depart_day = window.find_element(By.CSS_SELECTOR, "div.calendar-body__cell[data-id='2022-07-28']")
depart_day.click()

# clicking 'Find flights' button
find_button = window.find_element_by_xpath(
    "/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/div/div/button")
find_button.click()

# downloading the price for the chosen day
price_div = window.find_element_by_xpath(
    "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/flight-list/div/flight-card/div/div/div[3]/flight-price/div/span[3]/flights-price-simple")
price = price_div.get_attribute('innerHTML').strip()
print(price)

# writing the flight data to file
file_name = "flight-" + depart_city_name + "-" + dest_city_name + "-" + str(datetime.date.today()) + ".txt"

# check if file with such a name exists
if not exists(file_name):
    f = open(file_name, "w")
    f.write("Check date\tFlight\t\t\tdate\tPrice\n")
    f.close()

# writing data to the file
f = open(file_name, "a")
flight_to_write = str(datetime.date.today()) + "\t" + depart_city_name + "-" + dest_city_name + "\t\t\t" + str(
    datetime.date.today()) + "\t" + str(
    price) + '\n'
f.write(flight_to_write)
f.close()

# windows notifications with the price and the date
noti = ToastNotifier()
noti.show_toast("Ryanair Krakow-Leeds", "Flight on the day: " + str(datetime.date.today()) + "The price: " + str(price),
                icon_path=None, duration=5)

# close window
window.quit()
