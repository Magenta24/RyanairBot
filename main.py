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
from RyanairBot import RyanairBot

''' TO-DO
3. Creating client-server
    - the app will run on server
    - whenever the client will connect, the app will download report with flights data and there will be system notification
4. Checking flights' prices from all polish airports
'''

botek = RyanairBot('Chrome')
botek.run()

