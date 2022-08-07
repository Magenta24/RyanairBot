import datetime
import logging
import time
import traceback

from os.path import exists

from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from win10toast import ToastNotifier

''' TO-DO
2. Downloading prices of flights in 2 weeks to 1 month+2weeks
3. Creating client-server
    - the app will run on server
    - whenever the client will connect, the app will download report with flights data and there will be system notification
4. Checking flights' prices from all polish airports
'''


def isElemClickable(element):
    try:
        element.click()
        return True
    except WebDriverException:
        return False


def writeFlightToFile(file, depart_city_name, dest_city_name, flight_date, flight_price):
    flight_to_write = str(datetime.date.today()) + "\t" + depart_city_name + "-" + dest_city_name + "\t\t\t" + str(
        flight_date) + "\t" + str(
        flight_price) + '\n'
    file.write(flight_to_write)


try:
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
        "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']")
    one_way_btn.click()

    ### entering departure city
    departure_input = window.find_element_by_xpath("//*[@id='input-button__departure']")
    departure_input.click()
    time.sleep(1)

    ### choosing departure country  - Poland
    country_depart = window.find_element_by_xpath(
        "//div[@class='countries__country b2 ng-star-inserted']/span[text()[contains(.,'Polska')]]")
    country_depart.click()
    time.sleep(1)

    ### choosing departure city - Krakow
    city_depart = window.find_element_by_xpath(
        "//span[@data-id='KRK']")
    depart_city_name = city_depart.text
    print(depart_city_name)
    city_depart.click()
    time.sleep(1)

    ### entering destination city
    dest_input = window.find_element_by_xpath("//*[@id='input-button__destination']")
    dest_input.click()
    dest_input.click()
    time.sleep(1)

    # choosing country - United Kingdom
    country_dest = window.find_element_by_xpath(
        "//div[@class='countries__country b2 ng-star-inserted']/span[text()[contains(.,'Wielka Brytania')]]")
    country_dest.click()
    time.sleep(1)

    # # choosing city - Leeds
    city_dest = window.find_element_by_xpath(
        "//span[@data-id='LBA']")
    dest_city_name = city_dest.text.split('/')[0]
    print(dest_city_name)
    city_dest.click()
    time.sleep(1)

    # choosing date(10 days from today's date)
    ten_days_from_now = datetime.date.today() + timedelta(days=10)
    is_first_day_checked = False

    while not is_first_day_checked:
        depart_day = window.find_element(By.CSS_SELECTOR,
                                         "div.calendar-body__cell[data-id='" + str(ten_days_from_now) + "']")
        is_first_day_checked = isElemClickable(depart_day)

        if not is_first_day_checked:
            ten_days_from_now = ten_days_from_now + timedelta(days=1)

    # clicking 'Find flights' button
    find_button = window.find_element_by_xpath(
        "//button[@class='flight-search-widget__start-search ng-tns-c81-3 ry-button--gradient-yellow']")
    find_button.click()

    # downloading the price for the chosen day
    price_div = window.find_element_by_xpath(
        "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/div/div[2]/div/carousel-container/carousel/div/ul/li[3]/carousel-item/button/div[2]/flights-price/ry-price/span[2]")
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
    writeFlightToFile(f, depart_city_name, dest_city_name, ten_days_from_now, price)

    # searching for the next day
    edit_search_btn = window.find_element_by_xpath("//button[@class='details__edit-search']")
    edit_search_btn.click()
    time.sleep(2)
    edit_search_choose_date = window.find_element(By.CSS_SELECTOR, 'div.flight-widget-controls__calendar')
    edit_search_choose_date.click()

    # downloading prices for the next 30 days and writing them to the file
    day_counter = 0
    while day_counter < 30:
        ten_days_from_now = ten_days_from_now + timedelta(days=1)
        time.sleep(2)
        day_to_check = window.find_element(By.CSS_SELECTOR,
                                           "div.calendar-body__cell[data-id='" + str(ten_days_from_now) + "']")
        if isElemClickable(day_to_check):
            day_counter += 1
            # clicking button 'search again'
            search_again_btn = window.find_element_by_xpath(
                "//button[@class='flight-search-widget__start-search ng-tns-c203-13 ry-button--flat-blue']").click()
            time.sleep(2)
            price_div = window.find_element(By.TAG_NAME, "flights-price-simple")
            price = price_div.get_attribute('innerHTML').strip()
            writeFlightToFile(f, depart_city_name, dest_city_name, ten_days_from_now, price)

            edit_search_btn = window.find_element_by_xpath(
                "//button[@class='flight-search-widget__start-search ng-tns-c203-13 ry-button--flat-blue']")
            edit_search_btn.click()
            time.sleep(2)
            edit_search_choose_date = window.find_element(By.CSS_SELECTOR, 'div.flight-widget-controls__calendar')
            edit_search_choose_date.click()
        else:
            continue

    f.close()

    # windows notifications with the price and the date
    noti = ToastNotifier()
    noti.show_toast("Ryanair Krakow-Leeds",
                    "Flight on the day: " + str(ten_days_from_now) + "\nThe price: " + str(price),
                    icon_path=None, duration=5)

    # close the window
    window.quit()
except Exception as e:
    logging.error(traceback.format_exc())
    time.sleep(5)
    window.quit()
