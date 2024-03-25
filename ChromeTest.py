
import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
from scrapy import Selector
import os
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://google.com")

print("end")