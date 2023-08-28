import datetime
import logging
import time
import traceback

from Notification import Notification
from Flight import Flight
from airport_data import Airports
from RyanairWindow import RyanairWindow
from os.path import exists

from datetime import timedelta
from selenium.webdriver.common.by import By


class RyanairBot:


    def __init__(self, browser, departure_city, destination_city, start_date, end_date):

        # class attributes with default values
        self.__today_date = datetime.date.today()
        self.__min_price = 2147483647
        self.__browser = None
        self.__min_price_flight = None
        self.__search_start_date = None
        self.__search_end_date = None

        # dates validation
        if datetime.datetime.strptime(start_date, '%d-%m-%Y').date() < self.__today_date:
            print("You cannot provide date in the past!")
            exit(1)
        elif datetime.datetime.strptime(start_date, '%d-%m-%Y').date() > datetime.datetime.strptime(end_date,
                                                                                                    '%d-%m-%Y').date():
            print("You cannot provide start date older than end_date!")
        else:
            self.__search_start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()
            self.__search_end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()

        # departure and destination cities validation
        if not self.__isThereACity(departure_city):
            print("Sorry, there is no city: " + departure_city)
            print("All cities available:")
            for city in Airports.keys():
                print(city)
            exit(1)

        if not self.__isThereACity(destination_city):
            print("Sorry, there is no city: " + destination_city)
            print("All cities available:")
            for city in Airports.keys():
                print(city)
            exit(1)

        # connection validation
        if not self.__isThereConnection(departure_city, destination_city):
            print("There is no connection between these two cities!")
            print("All connections available from this departure city:")
            for city in Airports[departure_city].connections:
                print(city)
            exit(1)

        self.__browser = browser
        self.__min_price_flight = Flight(departure_city, destination_city)

        self.run()

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

            # downloading prices for the next 30 days and writing them to the file
            self.__checkFlightPrices2(window, f, self.__search_start_date, self.__search_end_date)

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

    def __isThereConnection(self, departure_city, destination_city):
        """
        Checks if there is a connection between given cities

        :param departure_city:
        :param destination_city:
        :return: True - there is, False - otherwise
        """

        for connection in Airports[departure_city].connections:
            if connection == destination_city:
                return True

        return False

    def __isThereACity(self, city):
        """
        Check if there is such city in the data

        :param city: city to check
        :return: True - there is a city, False - otherwise
        """

        for key in Airports.keys():
            if city == key:
                return True

        return False

    def __checkFlightPrices(self, window, file_pointer, start_date, end_date):
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

    def __checkFlightPrices2(self, window, file_pointer, start_date, end_date):
        """
        alternative function to check and write to the file flight prices for given number of days
        """

        current_date = start_date
        current_date += timedelta(days=1)

        while current_date != (end_date + timedelta(days=1)):

            if window.doesElementExists("//li/carousel-item/button[@data-ref='" + str(current_date) + "']"):
                day_to_check = window.getWindow().find_element(By.XPATH, "//li/carousel-item/button[@data-ref='" + str(
                    current_date) + "']")
            else:
                window.findElementByXPATHAndClick("//button[contains(@class, 'carousel-next')]")
                continue

            # check if element with given day is clickable
            if (window.isElementClickable(day_to_check)) and (window.doesElementChildExists(day_to_check,
                                                                                            ".//div[contains(@class, 'date-item__price')]")):
                print('Checked day: ' + str(current_date))
                day_to_check.click()

                # downloading the price for the chosen day
                price = self.__downloadPrice(window)

                # updating the minimum price
                self.__updateMinPrice(int(price), current_date)

                # writing flight data to the file
                self.__writeFlightToFile(file_pointer, self.__min_price_flight.getDepartureCity(),
                                         self.__min_price_flight.getDestinationCity(), current_date, price)

            current_date += timedelta(days=1)

    def __downloadPrice(self, window):
        """
        searching for the span with price
        """

        # wait until element is loaded on the site
        window.waitToLoadSiteContent(2)
        price_span = window.getWindow().find_element(By.XPATH, "//span[contains(@class, 'price__integers')]")
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
