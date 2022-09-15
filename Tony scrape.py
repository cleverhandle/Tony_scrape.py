import csv
import time
import re

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

f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a")
f.write(f'Starting Price,Cash Flow,Location\n')
f.close()

dailyurls = []
dailyurls.append('https://www.bizquest.com/fedex-businesses-for-sale/')

browser.get('https://www.bizquest.com/fedex-businesses-for-sale/')
next_page = 'y'
print('were starting')
while next_page == 'y':
    next_page_element = browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
    next_page_url = next_page_element.get_attribute('href')
    if '#' in next_page_url:
        next_page = 'n'
    else:
        dailyurls.append(next_page_url)
        nextpagebutton = browser.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
        nextpagebutton.click()

print(dailyurls)

for url in dailyurls:
    browser.get(url)
    chunk_info = browser.find_elements(By.CSS_SELECTOR, 'span[class="price"]')
    final_list = []
    for element in chunk_info:
        chunk = element.get_attribute('innerText')
        if "Cash Flow:" in chunk:
            final_list.append(chunk)
            cleaned_up = chunk.replace("\n", " ")
            starting_price = re.sub(" Cash Flow:[a-z,A-Z,0-9,\s\S]*", " ", cleaned_up)
            starting_price = starting_price.strip()
            back_half = cleaned_up.replace(starting_price, "")
            back_half = back_half.replace("Cash Flow: ", "")
            cash_flow_list = re.findall("[\$(\d*,)+(\d*)]", back_half)
            cash_flow = ''.join(cash_flow_list)
            if cash_flow[-1] == ',':
                cash_flow = cash_flow[:-1]
            location = back_half.replace(cash_flow, "")
            location = location.replace(" View Details", "")
            location = location.strip()

            print(f'{starting_price}, {cash_flow}, {location}\n')
            f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a")
            f.write(f'"{starting_price}","{cash_flow}","{location}"\n')
            f.close()