import datetime
import logging
import time
import traceback

from Notification import Notification
from Flight import Flight
from RyanairWindow import RyanairWindow
from os.path import exists

from datetime import timedelta
from selenium.webdriver.common.by import By


class RyanairBot:
    # class attributes with default values
    __todays_date = datetime.date.today()
    __min_price = 2147483647
    __browser = None
    __min_price_flight = None
    __search_start_date = None
    __search_end_date = None

    def __init__(self, browser, departure_city, destination_city, start_date, end_date):
        self.__browser = browser
        self.__min_price_flight = Flight(departure_city, destination_city)

        # dates validation
        if datetime.datetime.strptime(start_date, '%d-%m-%Y').date() < self.__todays_date:
            print("You cannot provide date in the past!")
            exit(1)
        elif datetime.datetime.strptime(start_date, '%d-%m-%Y').date() > datetime.datetime.strptime(end_date,
                                                                                                    '%d-%m-%Y').date():
            print("You cannot provide start date older than end_date!")
        else:
            self.__search_start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()
            self.__search_end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()

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

            # search for flight
            self.__search_start_date = window.searchForFlight(self.__min_price_flight.getDepartureCity(),
                                                              self.__min_price_flight.getDestinationCity(),
                                                              self.__search_start_date)

            # downloading the price for the chosen day
            price = self.__downloadPrice(window)

            # updating the minimum price
            self.__updateMinPrice(int(price), self.__search_start_date)

            # writing the flight data to file
            file_name = "ryanair-prices-" + self.__min_price_flight.getDepartureCity() + "-" + self.__min_price_flight.getDestinationCity() + "-" + str(
                datetime.date.today()) + "-" + str(datetime.datetime.now().strftime("%H%M")) + ".txt"

            # check if file with such a name exists
            if not exists(file_name):
                f = open(("search-reports/" + file_name), "w")
                f.write("CheckDate,FlightCourse,FlightDate,Price\n")
                f.close()
                print('File with name: ' + file_name + ' created.')

            # writing data to the file - from the first search
            f = open(("search-reports/" + file_name), "a")
            self.__writeFlightToFile(f, self.__min_price_flight.getDepartureCity(),
                                     self.__min_price_flight.getDestinationCity(), self.__search_start_date, price)

            # find 'Edit Search' button and then Calendar
            window.findEditSearchBtnAndClick()
            window.waitToLoadSiteContent(1)
            window.findCalendarAndClick()

            # downloading prices for the next 30 days and writing them to the file
            self.__checkFlightPricesNDaysAhead(window, f, self.__search_start_date, self.__search_end_date)

            # closing file
            f.close()

            # windows notifications with the price and the date
            self.__sendNotification()
            print('Notification sent.')

            # close the window
            window.closeWindow()

        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
            window.closeWindow()

    def __checkFlightPricesNDaysAhead(self, window, file_pointer, start_date, end_date):
        """
        checks and writes to the file flight prices for given number of days
        """

        current_date = start_date

        while current_date != (end_date + timedelta(days=1)):
            current_date += timedelta(days=1)
            day_to_check = window.getWindow().find_element(By.CSS_SELECTOR,
                                                           "div.calendar-body__cell[data-id='" + str(
                                                               current_date) + "']")

            # check if element with given day is clickable
            if window.isElementClickable(day_to_check):
                print('Checked day: ' + str(current_date))

                # click button 'search again'
                window.findElementByXPATHAndClick("//button[contains(@data-ref, 'flight-search-widget__cta')]")

                # downloading the price for the chosen day
                price = self.__downloadPrice(window)

                # updating the minimum price
                self.__updateMinPrice(int(price), current_date)

                # writing flight data to the file
                self.__writeFlightToFile(file_pointer, self.__min_price_flight.getDepartureCity(),
                                         self.__min_price_flight.getDestinationCity(), current_date, price)

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

        title_msg = "Ryanair " + self.__min_price_flight.getDepartureCity() + "-" \
                    + self.__min_price_flight.getDestinationCity()
        content_msg = "Flight on the day: " + str(self.__min_price_flight.getFlightDate()) \
                      + "\nThe price: " + str(self.__min_price) + " " \
                      + self.__min_price_flight.getPriceCurrency()
        win_not = Notification(title_msg, content_msg, 5)
        win_not.sendNotification()
