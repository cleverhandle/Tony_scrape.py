import csv
import time

# Web Browser independent Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.by import By

# Web Browser dependent Selenium code
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Selenium options.
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1080")

# Connect to the Selenium web driver.
service = Service(GeckoDriverManager().install())
browser = webdriver.Firefox(service=service, options=options)

# Open Web Page
browser.get("https://techstepacademy.com/trial-of-the-stones")

# find first riddle and answer it
## find input path
stoneanswerinputpath = "input[id='r1Input']"
## find the actual field
stoneanswerinput = browser.find_element(By.CSS_SELECTOR, stoneanswerinputpath)
## type in answer
stoneanswerinput.send_keys("rock")
## find button path
answerbuttonpath = "button[id='r1Btn']"
##Get actual button
answerbutton = browser.find_element(By.CSS_SELECTOR, answerbuttonpath)
##Click button
answerbutton.click()
