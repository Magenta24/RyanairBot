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

