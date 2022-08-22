import datetime
import logging
import time
import traceback

from Notification import Notification
from Flight import Flight
from os.path import exists

from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            # create new web browser window
            if self.__browser == 'Chrome':

                # hiding bot from detecting by Chrome browser
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

                # running bot without 'opening' browser window
                options.add_argument('headless')

                window = webdriver.Chrome(executable_path=r'J:\chromedriver.exe', options=options)
                print('Ryanair Bot is running in ' + self.__browser + '...')
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
            print('Cookies accepted.')

            # selecting one-way trip
            one_way_btn = window.find_element_by_xpath(
                "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']")
            one_way_btn.click()
            print('One-way trip chosen.')

            # entering departure city
            departure_input = window.find_element_by_xpath("//*[@id='input-button__departure']")
            departure_input.click()
            self.__waitToLoadSiteContent(1)

            # choosing departure country
            country_depart = window.find_element_by_xpath(
                "//div[contains(@class,'countries__country')]/span[text()[contains(.,'" +
                self.__min_price_flight.getDepartureCountry() + "')]]")
            country_depart.click()
            self.__waitToLoadSiteContent(1)

            # choosing departure city
            self.__waitToLoadSiteContent(1)
            city_depart = window.find_element_by_xpath(
                "//span[@data-id='" + self.__min_price_flight.getDeparturePortIATACode() + "']")
            city_depart.click()
            print('Departure city: ' + self.__min_price_flight.getDepartureCity() + ' chosen.')
            self.__waitToLoadSiteContent(1)

            # entering destination city
            dest_input = window.find_element_by_xpath("//*[@id='input-button__destination']")
            dest_input.click()
            dest_input.click()
            self.__waitToLoadSiteContent(1)

            # choosing destination country
            country_dest = window.find_element_by_xpath(
                "//div[@class='countries__country b2 ng-star-inserted']/span[text()[contains(.,'" +
                self.__min_price_flight.getDestinationCountry() + "')]]")
            country_dest.click()
            self.__waitToLoadSiteContent(1)

            # choosing destination city
            city_dest = window.find_element_by_xpath(
                "//span[@data-id='" + self.__min_price_flight.getDestinationPortIATACode() + "']")
            city_dest.click()
            print('Destination city: ' + self.__min_price_flight.getDestinationCity() + ' chosen.')
            self.__waitToLoadSiteContent(1)

            # choosing start date (at least 10 days from today's date)
            search_start_date = datetime.date.today() + timedelta(days=10)
            is_first_day_chosen = False

            while not is_first_day_chosen:
                depart_day_div = window.find_element(By.CSS_SELECTOR,
                                                     "div.calendar-body__cell[data-id='" + str(
                                                         search_start_date) + "']")
                is_first_day_chosen = self.__isElementClickable(depart_day_div)

                if not is_first_day_chosen:
                    search_start_date = search_start_date + timedelta(days=1)

            print('Search start date: ' + str(search_start_date) + '.')

            # clicking 'Find flights' button
            find_button = window.find_element_by_xpath(
                "//button[contains(@class, 'flight-search-widget__start-search')]")
            find_button.click()

            self.__waitToLoadSiteContent(2)

            # downloading the price for the chosen day
            price = self.__downloadPrice(window)

            # updating the minimum price
            self.__updateMinPrice(int(price), search_start_date)

            # writing the flight data to file
            file_name = "ryanair-prices-" + self.__min_price_flight.getDepartureCity() + "-" + self.__min_price_flight.getDestinationCity() + "-" + str(
                datetime.date.today()) + "-" + str(datetime.datetime.now().strftime("%H%M%S")) +".txt"

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
            self.__findEditSearchBtnAndClick(window)
            self.__waitToLoadSiteContent(1)
            self.__findCalendarAndClick(window)

            # downloading prices for the next 30 days and writing them to the file
            self.__checkFlightPricesNDaysAhead(20, window, f, search_start_date)

            # closing file
            f.close()

            # windows notifications with the price and the date
            self.__sendNotification()
            print('Notification sent.')

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
            day_to_check = window.find_element(By.CSS_SELECTOR,
                                               "div.calendar-body__cell[data-id='" + str(start_date) + "']")

            # check if element with given day is clickable
            if self.__isElementClickable(day_to_check):
                print('Checked day: ' + str(number_of_days))
                number_of_days -= 1

                # clicking button 'search again'
                search_again_btn = window.find_element_by_xpath(
                    "//button[contains(@data-ref, 'flight-search-widget__cta')]")
                search_again_btn.click()

                # self.__waitToLoadSiteContent(1)

                # downloading the price for the chosen day
                price = self.__downloadPrice(window)

                # updating the minimum price
                self.__updateMinPrice(int(price), start_date)

                # writing flight data to the file
                self.__writeFlightToFile(file_pointer, self.__min_price_flight.getDepartureCity(),
                                         self.__min_price_flight.getDestinationCity(), start_date, price)

                self.__findEditSearchBtnAndClick(window)
                self.__waitToLoadSiteContent(1)
                self.__findCalendarAndClick(window)
            else:
                continue

    def __downloadPrice(self, window):
        """
        searching for the span with price
        """

        # price_span = window.find_element_by_xpath("//span[contains(@class, 'price__integers')]")

        # wait until element is loaded on the site
        price_span = self.__waitForElementToLoad(window, "//span[contains(@class, 'price__integers')]")
        price = price_span.get_attribute('innerHTML').strip()  # getting price inside the span

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
            self.__min_price) + " zlotych wspanialych polskich"
        win_not = Notification(title_msg, content_msg, 5)
        win_not.sendNotification()

    def __waitForElementToLoad(self, window, path):
        """
        waiting given time for an element to load on the site. After that time an exception is raised
        """

        delay = 5  # max time to wait
        element = WebDriverWait(window, delay).until(
            EC.presence_of_element_located((By.XPATH, path)))

        return element
