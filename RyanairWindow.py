import datetime
from airport_data import Airports

from Window import Window

from datetime import timedelta
from selenium.webdriver.common.by import By


class RyanairWindow(Window):
    __website_address = "https://www.ryanair.com/"
    __ryanair_window = None

    def __init__(self, browser_name):
        super().__init__(browser_name, self.__website_address)
        self.__ryanair_window = super().getWindow()

    def handleCookies(self):
        """
        Accepts only mandatory cookies

        :return: None
        """

        # accepting cookies - only selected cookies (only those mandatory)
        self.waitToLoadSiteContent(2)
        cookies = self.__ryanair_window.find_element_by_xpath('/html/body/div/div/div[3]/button[1]')
        cookies.click()
        super().waitToLoadSiteContent(2)

        # switch to iframe
        self.switchFrames("//iframe[@id='cookie-preferences__iframe']")
        self.waitToLoadSiteContent(2)

        # click toggle button to uncheck the unnecessary cookies
        self.findElementByXPATHAndDoubleClick('//cookies-details/div/div[7]/div/ry-toggle/label/div/div/div')

        # confirm choices
        self.findElementByXPATHAndClick('//cookies-root/ng-component/main/section/div/cookies-details/div/button')
        print('Cookies accepted.')

        self.waitToLoadSiteContent(3)

        # switch back to the outer window
        self.__ryanair_window.switch_to.default_content()

    def findEditSearchBtnAndClick(self):
        """
        finds 'Edit Search' button and clicks it
        """

        edit_search_btn = self.__ryanair_window.find_element_by_xpath(
            "//button[contains(@class,'details__edit-search')]")
        edit_search_btn.click()

    def findCalendarAndClick(self):
        """
        finds Calendar after clicking 'Edit Search' button and clicks it
        """

        edit_search_choose_date = self.__ryanair_window.find_element(By.CSS_SELECTOR,
                                                                     'div.flight-widget-controls__calendar')
        edit_search_choose_date.click()

    def searchForFlight(self, departure_city, destination_city, start_date):
        """
        searching for a given flight

        :param departure_city:
        :param destination_city:
        :param start_date: search start date user has chosen
        :return: actual date when the search begins (so if the given date is not available, the nearest next one)
        """

        # selecting one-way trip
        self.findElementByXPATHAndDoubleClick(
            "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']/button")
        print('One-way trip chosen.')

        # choosing departure country
        self.waitToLoadSiteContent(1)
        self.findElementByXPATHAndDoubleClick("//*[@id='input-button__departure']")
        self.waitToLoadSiteContent(1)
        self.findElementByXPATHAndClick("//div[contains(@class,'countries__country')]/span[text()[contains(.,'" +
                                        Airports[departure_city].country + "')]]")
        self.waitToLoadSiteContent(1)

        # choosing departure city
        self.findElementByXPATHAndClick(
            "//span[@data-id='" + Airports[departure_city].IATA_code + "']")
        print('Departure city: ' + departure_city + '.')
        self.waitToLoadSiteContent(1)

        # choosing destination country
        self.findElementByXPATHAndDoubleClick("//*[@id='input-button__destination']")
        self.waitToLoadSiteContent(1)
        self.findElementByXPATHAndClick(
            "//div[contains(@class, 'countries__country')]/span[text()[contains(.,'"
            + Airports[destination_city].country + "')]]")
        self.waitToLoadSiteContent(1)

        # choosing destination city
        self.findElementByXPATHAndClick(
            "//span[@data-id='" + Airports[destination_city].IATA_code + "']")
        print('Destination city: ' + destination_city + '.')
        self.waitToLoadSiteContent(1)

        # choosing start date (at least 10 days from today's date)
        is_first_day_chosen = False

        # if there is no flight on the argument date, the next available date will be the start date
        while not is_first_day_chosen:
            depart_day_div = self.__ryanair_window.find_element(By.CSS_SELECTOR,
                                                                "div.calendar-body__cell[data-id='" + str(
                                                                    start_date) + "']")
            is_first_day_chosen = self.isElementClickable(depart_day_div)

            if not is_first_day_chosen:
                start_date = start_date + timedelta(days=1)

        print('Search start date: ' + str(start_date) + '.')

        # clicking 'Find flights' button
        self.findElementByXPATHAndClick("//button[contains(@class, 'flight-search-widget__start-search')]")
        self.waitToLoadSiteContent(2)

        return start_date
