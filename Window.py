import logging
import time
import traceback

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


class Window:
    __driver_path = None
    __window = None

    def __init__(self, browser_name, website_address):
        try:
            # create new web browser window
            if browser_name == 'Chrome':

                # hiding bot from detecting by Chrome browser
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

                # running bot without 'opening' browser window
                # options.add_argument('headless')

                self.__window = webdriver.Chrome(executable_path=r'J:\chromedriver_win32_v_109\chromedriver.exe', options=options)
                print('Ryanair Bot is running in ' + browser_name + '...')
            elif browser_name == 'Mozilla':
                options = webdriver.FirefoxOptions()
                options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
                self.__window = webdriver.Firefox(executable_path=r'J:\geckodriver.exe', options=options)
            else:
                print('There is no webdriver for this browser')
                exit(-1)

            self._openWebPage(website_address)


        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(5)
            self.__window.quit()
            exit(-1)

    def getWindow(self):
        """
        Returns window with browser's session

        :return: window
        """

        return self.__window

    def _openWebPage(self, web_page_address):
        """
        Navigates to a give web page

        :param web_page_address: web-page address, user wish to open
        :return: None
        """

        self.__window.get(web_page_address)

    def switchFrames(self, xpath):
        self.__window.switch_to.frame(self.__window.find_element_by_xpath(xpath))

    def waitToLoadSiteContent(self, time_in_sec):
        """
        pausing the program to wait for loading site content

        :param timeInSec: time in seconds we wish to pause the code execution
        :return: None
        """

        time.sleep(time_in_sec)

    def waitForElementToLoad(self, xpath):
        """
        waiting given time for an element to load on the site. After that time an exception is raised
        Returns an element obtained from the given xpath

        :param xpath: xPath to the element we are wairing for to load
        :return: element we waited for to load
        """

        delay = 5  # max time to wait
        element = WebDriverWait(self, delay).until(
            ec.presence_of_element_located((By.XPATH, xpath)))

        return element

    def isElementClickable(self, element):
        """
        checking if the given element is clickable and if so it's clicked

        :param element: website element to check
        :return: True is clickable, False otherwise
        """

        try:
            element.click()
            return True
        except WebDriverException:
            return False

    def findElementByXPATHAndClick(self, xpath):
        """
        Finds an element by the given xpath and clicks it

        :param xpath: path to the given element
        :return: None
        """
        element = self.__window.find_element(By.XPATH, xpath)
        self.__window.execute_script("arguments[0].click();", element)

    def findElementByXPATHAndDoubleClick(self, xpath):
        """
        Finds an element by the given xpath and double-clicks it

        :param xpath: path to the given element
        :return: None
        """

        element = self.__window.find_element(By.XPATH, xpath)
        self.__window.execute_script("arguments[0].click();", element)
        self.__window.execute_script("arguments[0].click();", element)

    def findElementByCSSSelectorAndClick(self, css_path):
        """
        Finds an element by the given css_path and clicks it

        :param css_path: path to the given element
        :return: None
        """

        element = self.__window.find_element(By.CSS_SELECTOR, css_path)
        self.__window.execute_script("arguments[0].click();", element)

    def doesElementChildExists(self, parent_element, xpath):
        """
        Checks if given element has a child with given path

        :param parent_element:
        :param xpath:
        :return:
        """
        if len(parent_element.find_elements(By.XPATH, xpath)) == 0:
            return False
        else:
            return True

    def doesElementExists(self, xpath):
        """
        Checks if there is an element under given xpath

        :param xpath:
        :return: True if exists, False otherwise
        """
        if len(self.__window.find_elements(By.XPATH, xpath)) == 0:
            return False
        else:
            return True

    def closeWindow(self):
        self.__window.quit()
