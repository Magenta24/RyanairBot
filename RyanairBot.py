import datetime
import logging
import time
import traceback

from Notification import Notification
from os.path import exists

from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


class RyanairBot:
    # class attributes with default values
    __departure_country = 'Polska'
    __departure_city = 'Kraków'
    __destination_country = 'Wielka Brytania'
    __destination_city = 'Leeds'
    __todays_date = datetime.date.today()
    __search_start_date = __todays_date + timedelta(days=10)
    __min_price = 2147483647
    __browser = None

    def __init__(self, browser):
        self.__browser = browser

    # def __init__(self, depart_city, dest_city):
    #     self.__departure_city = depart_city
    #     self.__destination_city = dest_city
    #     # flight = Flight(depart_city, dest_city)

    def run(self):
        try:
            # create new web browser window
            if self.__browser == 'Chrome':
                window = webdriver.Chrome(executable_path=r'J:\chromedriver.exe')
            elif self.__browser == 'Mozilla':
                window = webdriver.Firefox(executable_path=r'J:\geckodriver.exe')
            else:
                print('There is no webdriver for this browser')
                exit(-1)

            # open a ryanair site
            window.get("https://www.ryanair.com/pl/pl")

            # accepting cookies
            self.__waitToLoadSiteContent(2)
            cookies = window.find_element_by_xpath('/html/body/div/div/div[3]/button[2]')
            cookies.click()

            # selecting one-way trip
            one_way_btn = window.find_element_by_xpath(
                "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']")
            one_way_btn.click()

            # entering departure city
            departure_input = window.find_element_by_xpath("//*[@id='input-button__departure']")
            departure_input.click()
            self.__waitToLoadSiteContent(1)

            # choosing departure country  - Poland
            country_depart = window.find_element_by_xpath(
                "//div[contains(@class,'countries__country')]/span[text()[contains(.,'Polska')]]")
            country_depart.click()
            self.__waitToLoadSiteContent(1)

            # choosing departure city - Krakow
            city_depart = window.find_element_by_xpath(
                "//span[@data-id='KRK']")
            depart_city_name = city_depart.text
            city_depart.click()
            self.__waitToLoadSiteContent(1)

            # entering destination city
            dest_input = window.find_element_by_xpath("//*[@id='input-button__destination']")
            dest_input.click()
            dest_input.click()
            self.__waitToLoadSiteContent(1)

            # choosing country - United Kingdom
            country_dest = window.find_element_by_xpath(
                "//div[@class='countries__country b2 ng-star-inserted']/span[text()[contains(.,'Wielka Brytania')]]")
            country_dest.click()
            self.__waitToLoadSiteContent(1)

            # choosing city - Leeds
            city_dest = window.find_element_by_xpath(
                "//span[@data-id='LBA']")
            dest_city_name = city_dest.text.split('/')[0]
            city_dest.click()
            self.__waitToLoadSiteContent(1)

            # choosing date(10 days from today's date)
            ten_days_from_now = datetime.date.today() + timedelta(days=10)
            is_first_day_chosen = False

            while not is_first_day_chosen:
                depart_day_div = window.find_element(By.CSS_SELECTOR,
                                                     "div.calendar-body__cell[data-id='" + str(
                                                         ten_days_from_now) + "']")
                is_first_day_chosen = self.__isElementClickable(depart_day_div)

                if not is_first_day_chosen:
                    ten_days_from_now = ten_days_from_now + timedelta(days=1)

            # clicking 'Find flights' button
            find_button = window.find_element_by_xpath(
                "//button[contains(@class, 'flight-search-widget__start-search')]")
            find_button.click()

            self.__waitToLoadSiteContent(2)

            # downloading the price for the chosen day
            price = self.__downloadPrice(window)

            # updating the minimum price
            self.__updateMinPrice(int(price))

            # writing the flight data to file
            file_name = "ryanair-prices-" + depart_city_name + "-" + dest_city_name + "-" + str(
                datetime.date.today()) + ".csv"

            # check if file with such a name exists
            if not exists(file_name):
                f = open(file_name, "w")
                f.write("CheckDate,FlightCourse,FlightDate,Price\n")
                f.close()

            # writing data to the file - from the first search
            f = open(file_name, "a")
            self.__writeFlightToFile(f, self.__departure_city, self.__destination_city, ten_days_from_now, price)

            # find 'Edit Search' button and then Calendar
            self.__findEditSearchBtnAndClick(window)
            self.__waitToLoadSiteContent(2)
            self.__findCalendarAndClick(window)

            # downloading prices for the next 30 days and writing them to the file
            self.__checkFlightPricesNDaysAhead(30, window, f, ten_days_from_now)

            # closing file
            f.close()

            # windows notifications with the price and the date
            self.__sendNotification()

            # close the window
            window.quit()

        except Exception as e:
            logging.error(traceback.format_exc())
            # time.sleep(5)
            # window.quit()

    def __isElementClickable(self, element):
        """
        checking if the given element is clickable and if so it's clicked
        """

        try:
            element.click()
            return True
        except WebDriverException:
            return False

    def __writeFlightToFile(self, file, depart_city_name, dest_city_name, flight_date, flight_price):
        """
        writing flight details to already open csv file
        """

        flight_to_write = str(datetime.date.today()) + "," + depart_city_name + "-" + dest_city_name + "," + str(
            flight_date) + "," + str(
            flight_price) + '\n'
        file.write(flight_to_write)

    def __waitToLoadSiteContent(self, timeInSec):
        """
        pausing the program to wait for loading site content
        """

        time.sleep(timeInSec)

    def __checkFlightPricesNDaysAhead(self, number_of_days, window, file_pointer, start_date):
        """
        checks and writes to the file flight prices for given number of days
        """

        while number_of_days > 0:
            start_date = start_date + timedelta(days=1)
            self.__waitToLoadSiteContent(1.5)
            day_to_check = window.find_element(By.CSS_SELECTOR,
                                               "div.calendar-body__cell[data-id='" + str(start_date) + "']")

            # check if element with given day is clickable
            if self.__isElementClickable(day_to_check):
                number_of_days -= 1

                # clicking button 'search again'
                search_again_btn = window.find_element_by_xpath(
                    "//button[contains(@data-ref, 'flight-search-widget__cta')]")
                search_again_btn.click()

                self.__waitToLoadSiteContent(1.5)

                # downloading the price for the chosen day
                price = self.__downloadPrice(window)

                # updating the minimum price
                self.__updateMinPrice(int(price))

                # writing flight data to the file
                self.__writeFlightToFile(file_pointer, self.__departure_city, self.__destination_city, start_date,
                                         price)

                self.__findEditSearchBtnAndClick(window)
                self.__waitToLoadSiteContent(1)
                self.__findCalendarAndClick(window)
            else:
                continue

    def __downloadPrice(self, window):
        """
        searching for the span with price
        """

        price_span = window.find_element_by_xpath("//span[contains(@class, 'price__integers')]")
        price = price_span.get_attribute('innerHTML').strip()

        # replacing the hard-breaking space with regular one if there is one
        if price.find('&nbsp;') > -1:
            price = price.replace('&nbsp;', '')

        return price

    def __findEditSearchBtnAndClick(self, window):
        """
        finds 'Edit Search' button and clicks it
        """

        edit_search_btn = window.find_element_by_xpath("//button[contains(@class,'details__edit-search')]")
        edit_search_btn.click()

    def __findCalendarAndClick(self, window):
        """
        finds Calendar after clicking 'Edit Search' button and clicks it
        """

        edit_search_choose_date = window.find_element(By.CSS_SELECTOR, 'div.flight-widget-controls__calendar')
        edit_search_choose_date.click()

    def __updateMinPrice(self, price):
        """
        if given price is smaller than the self.__min_price then self.__min_price = price
        """

        if price < self.__min_price:
            self.__min_price = price

    def __sendNotification(self):
        """
        windows notifications with the price and the date
        """

        title_msg = "Ryanair " + self.__departure_city + "-" + self.__destination_city
        content_msg = "Flight on the day: " + str(self.__search_start_date) + "\nThe price: " + str(
            self.__min_price) + " zlotych wspanialych polskich"
        win_not = Notification(title_msg, content_msg, 5)
        win_not.sendNotification()
