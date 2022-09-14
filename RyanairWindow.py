import datetime
from airport_data import Airports

from Window import Window

from datetime import timedelta
from selenium.webdriver.common.by import By


class RyanairWindow(Window):
    __website_address = "https://www.ryanair.com/pl/pl"
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
        toggle = self.__ryanair_window.find_element_by_xpath(
            '//cookies-details/div/div[7]/div/ry-toggle/label/div/div/div')
        toggle.click()

        # confirm choices
        confirm_cookies = self.__ryanair_window.find_element_by_xpath(
            '//cookies-root/ng-component/main/section/div/cookies-details/div/button')
        confirm_cookies.click()
        print('Cookies accepted.')

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

    def findElementByXPATHAndClick(self, xpath):
        """
        Finding an element by the given xpath and clicking it

        :param xpath: path to the given element
        :return: None
        """
        element = self.__ryanair_window.find_element_by_xpath(xpath)
        element.click()

    def findElementByXPATHAndDoubleClick(self, xpath):
        """
        Finding an element by the given xpath and double-clicking it

        :param xpath: path to the given element
        :return: None
        """
        element = self.__ryanair_window.find_element_by_xpath(xpath)
        element.click()
        element.click()

    def searchForFlight(self, departure_city, destination_city):
        """
        searching for a given flight

        :param departure_city:
        :param destination_city:
        :return: date when the search begins
        """

        # selecting one-way trip
        self.findElementByXPATHAndClick(
            "//fsw-trip-type-button[@data-ref='flight-search-trip-type__one-way-trip']")
        print('One-way trip chosen.')

        # choosing departure country
        self.findElementByXPATHAndClick("//*[@id='input-button__departure']")
        self.waitToLoadSiteContent(1)
        self.findElementByXPATHAndClick("//div[contains(@class,'countries__country')]/span[text()[contains(.,'" +
                                        Airports[departure_city].country + "')]]")
        self.waitToLoadSiteContent(1)

        # choosing departure city
        self.findElementByXPATHAndClick(
            "//span[@data-id='" + Airports[departure_city].IATA_code + "']")
        print('Departure city: ' + departure_city + ' chosen.')
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
        print('Destination city: ' + destination_city + ' chosen.')
        self.waitToLoadSiteContent(1)

        # choosing start date (at least 10 days from today's date)
        search_start_date = datetime.date.today() + timedelta(days=10)
        is_first_day_chosen = False

        while not is_first_day_chosen:
            depart_day_div = self.__ryanair_window.find_element(By.CSS_SELECTOR,
                                                                "div.calendar-body__cell[data-id='" + str(
                                                                    search_start_date) + "']")
            is_first_day_chosen = self.isElementClickable(depart_day_div)

            if not is_first_day_chosen:
                search_start_date = search_start_date + timedelta(days=1)

        print('Search start date: ' + str(search_start_date) + '.')

        # clicking 'Find flights' button
        self.findElementByXPATHAndClick("//button[contains(@class, 'flight-search-widget__start-search')]")
        self.waitToLoadSiteContent(2)

        return search_start_date
