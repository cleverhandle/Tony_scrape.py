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
options.headless = True
options.add_argument("--window-size=1920,1080")

# Connect to the Selenium web driver.
service = Service(GeckoDriverManager().install())
browser = webdriver.Firefox(service=service, options=options)

def prep_output_file(file_to_prep):
    open(file_to_prep, 'w').close()  # makes sure the writing starts at front of file
    f = open(file_to_prep, "a")
    f.write(f'places to check\n')
    f.close()
    return()

def check_venues(first_number, last_number):
    index_number = first_number
    while index_number <= last_number:
        browser.get('https://www.austinchronicle.com/locations/' + str(index_number) + '/')
        # venue_info = browser.find_elements(By.CSS_SELECTOR, 'div[class="body"]')
        venue_info = browser.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][title*=".com"]')
        for element in venue_info:
            venue_link = (element.get_attribute('href'))
            print(f'{index_number} has {venue_link}')
            # Writes to a file
            f = open('C:\\Users\\12544\\Documents\\Unknown locations.csv', "a")
            f.write(f'{venue_link}\n')
            f.close()
        index_number = index_number + 1
        print(index_number)
    print('all done')


prep_output_file('C:\\Users\\12544\\Documents\\Unknown locations.csv')
check_venues(533654, 540000)