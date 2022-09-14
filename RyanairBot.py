import datetime
import logging
import time
import traceback

from Notification import Notification
from Flight import Flight
from RyanairWindow import RyanairWindow
from os.path import exists

from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class RyanairBot:
    # class attributes with default values
    __todays_date = datetime.date.today()
    __search_start_date = __todays_date + timedelta(days=10)
    __min_price = 2147483647
    __browser = None
    __min_price_flight = None

    def __init__(self, browser, departure_city, destination_city, ):
        self.__browser = browser
        self.__min_price_flight = Flight(departure_city, destination_city)

    def run(self):
        try:
            # create Ryanair website window
            if self.__browser == 'Chrome':
                window = RyanairWindow('Chrome')
            elif self.__browser == 'Mozilla':
                window = RyanairWindow('Mozilla')
            else:
                print('There is no webdriver for this browser')
                exit(-1)

            # accepting only mandatory cookies
            window.handleCookies()

            # selecting one-way trip
            window.findElementByXPATHAndClick(
                "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']")
            print('One-way trip chosen.')

            # choosing departure country
            window.findElementByXPATHAndClick("//*[@id='input-button__departure']")
            window.waitToLoadSiteContent(1)
            window.findElementByXPATHAndClick("//div[contains(@class,'countries__country')]/span[text()[contains(.,'" +
                                              self.__min_price_flight.getDepartureCountry() + "')]]")
            window.waitToLoadSiteContent(1)

            # choosing departure city
            window.findElementByXPATHAndClick(
                "//span[@data-id='" + self.__min_price_flight.getDeparturePortIATACode() + "']")
            print('Departure city: ' + self.__min_price_flight.getDepartureCity() + ' chosen.')
            window.waitToLoadSiteContent(1)

            # choosing destination country
            window.findElementByXPATHAndDoubleClick("//*[@id='input-button__destination']")
            window.waitToLoadSiteContent(1)
            window.findElementByXPATHAndClick(
                "//div[contains(@class, 'countries__country')]/span[text()[contains(.,'"
                + self.__min_price_flight.getDestinationCountry() + "')]]")
            window.waitToLoadSiteContent(1)

            # choosing destination city
            window.findElementByXPATHAndClick(
                "//span[@data-id='" + self.__min_price_flight.getDestinationPortIATACode() + "']")
            print('Destination city: ' + self.__min_price_flight.getDestinationCity() + ' chosen.')
            window.waitToLoadSiteContent(1)

            # choosing start date (at least 10 days from today's date)
            search_start_date = datetime.date.today() + timedelta(days=10)
            is_first_day_chosen = False

            while not is_first_day_chosen:
                depart_day_div = window.getWindow().find_element(By.CSS_SELECTOR,
                                                                 "div.calendar-body__cell[data-id='" + str(
                                                                     search_start_date) + "']")
                is_first_day_chosen = window.isElementClickable(depart_day_div)

                if not is_first_day_chosen:
                    search_start_date = search_start_date + timedelta(days=1)

            print('Search start date: ' + str(search_start_date) + '.')

            # clicking 'Find flights' button
            window.findElementByXPATHAndClick("//button[contains(@class, 'flight-search-widget__start-search')]")
            window.waitToLoadSiteContent(2)

            # downloading the price for the chosen day
            price = self.__downloadPrice(window)

            # updating the minimum price
            self.__updateMinPrice(int(price), search_start_date)

            # writing the flight data to file
            file_name = "ryanair-prices-" + self.__min_price_flight.getDepartureCity() + "-" + self.__min_price_flight.getDestinationCity() + "-" + str(
                datetime.date.today()) + "-" + str(datetime.datetime.now().strftime("%H%M%S")) + ".txt"

            # check if file with such a name exists
            if not exists(file_name):
                f = open(file_name, "w")
                f.write("CheckDate,FlightCourse,FlightDate,Price\n")
                f.close()
                print('File with name: ' + file_name + ' created.')

            # writing data to the file - from the first search
            f = open(file_name, "a")
            self.__writeFlightToFile(f, self.__min_price_flight.getDepartureCity(),
                                     self.__min_price_flight.getDestinationCity(), search_start_date, price)

            # find 'Edit Search' button and then Calendar
            window.findEditSearchBtnAndClick()
            window.waitToLoadSiteContent(1)
            window.findCalendarAndClick()

            # downloading prices for the next 30 days and writing them to the file
            self.__checkFlightPricesNDaysAhead(window, 20, f, search_start_date)

            # closing file
            f.close()

            # windows notifications with the price and the date
            self.__sendNotification()
            print('Notification sent.')

            # close the window
            window.getWindow().quit()

        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
            window.getWindow().quit()

    def __checkFlightPricesNDaysAhead(self, window, number_of_days, file_pointer, start_date):
        """
        checks and writes to the file flight prices for given number of days
        """

        while number_of_days > 0:
            start_date = start_date + timedelta(days=1)
            day_to_check = window.getWindow().find_element(By.CSS_SELECTOR,
                                                           "div.calendar-body__cell[data-id='" + str(
                                                               start_date) + "']")

            # check if element with given day is clickable
            if window.isElementClickable(day_to_check):
                print('Checked day: ' + str(number_of_days))
                number_of_days -= 1

                # click button 'search again'
                window.findElementByXPATHAndClick("//button[contains(@data-ref, 'flight-search-widget__cta')]")

                # downloading the price for the chosen day
                price = self.__downloadPrice(window)

                # updating the minimum price
                self.__updateMinPrice(int(price), start_date)

                # writing flight data to the file
                self.__writeFlightToFile(file_pointer, self.__min_price_flight.getDepartureCity(),
                                         self.__min_price_flight.getDestinationCity(), start_date, price)

                window.findEditSearchBtnAndClick()
                window.waitToLoadSiteContent(1)
                window.findCalendarAndClick()
            else:
                continue

    def __downloadPrice(self, window):
        """
        searching for the span with price
        """

        # wait until element is loaded on the site
        window.waitToLoadSiteContent(1.5)
        price_span = window.getWindow().find_element_by_xpath("//span[contains(@class, 'price__integers')]")
        price = price_span.get_attribute('innerHTML').strip()  # getting price inside the span

        # replacing the hard-breaking space with regular one if there is one
        if price.find('&nbsp;') > -1:
            price = price.replace('&nbsp;', '')

        return price

    def __writeFlightToFile(self, file, depart_city_name, dest_city_name, flight_date, flight_price):
        """
        writing flight details to already open csv file
        """

        flight_to_write = str(datetime.date.today()) + "," + depart_city_name + "-" + dest_city_name + "," + str(
            flight_date) + "," + str(
            flight_price) + '\n'
        file.write(flight_to_write)

    def __updateMinPrice(self, price, date):
        """
        if given price is smaller than the self.__min_price then self.__min_price = price
        """

        if price < self.__min_price:
            self.__min_price = price
            self.__min_price_flight.setPrice(price)
            self.__min_price_flight.setDate(date)

    def __sendNotification(self):
        """
        windows notifications with the price and the date
        """

        title_msg = "Ryanair " + self.__min_price_flight.getDepartureCity() + "-" + self.__min_price_flight.getDestinationCity()
        content_msg = "Flight on the day: " + str(self.__min_price_flight.getFlightDate()) + "\nThe price: " + str(
            self.__min_price) + " " + self.__min_price_flight.getPriceCurrency()
        win_not = Notification(title_msg, content_msg, 5)
        win_not.sendNotification()
