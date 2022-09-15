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

with open('C:\\Users\\12544\\Documents\\Unknown locations.csv', 'r') as read_obj: # read csv file as a list of lists
  csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
  list_of_rows = list(csv_reader) # Pass reader object to list() to get a list of lists

#turns the list of lists into lists of strings
urllist = []
urllist = [''.join(ele) for ele in list_of_rows]

bad_paragraphs = ['Ports & Slots', 'Dimensions & Weight', 'Essential accessories', 'Accessories',
                  'High-performance gaming accessories', 'Dimensions & weight', 'High-performance accessories',
                  'PORTS & SLOTS', 'HIGH-PERFORMANCE GAMING ACCESSORIES', 'PERFORMANCE-ENHANCING PERIPHERALS',
                  'Essential desk accessories', 'Essential mobile accessories', 'Ports & slots',
                  'Dimensions and Weight', 'Essential work accessories', 'Essential on-the-go accessories',
                  'Essential specialized accessories', 'Essential office accessories', 'Specialized accessories',
                  'Spec Sheet', 'essential accessories']
# For every URL on the list
for page in urllist:
    # Get all the Feature paragraphs
    browser.get(page)
    api_search = browser.find_element(By.CSS_SELECTOR, 'div[class="product-features-content"]')
    api_url = api_search.get_attribute('data-product-features-api')
    browser.get(api_url)
    feature_elements = browser.find_elements(By.CSS_SELECTOR, 'div[class="pd-feature-item"]')
    # Print and Write URL to file
    print(f'{page},')
    f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a", encoding="utf-8")
    f.write(f'{page},')
    for feature in feature_elements:
        #  Print and write paragraph to file, followed by a Comma
        paragraph = feature.get_attribute('innerText')
        no_comma = paragraph.replace(",", "")
        no_newline_para = no_comma.replace("\n", " ")
        for phrase in bad_paragraphs:
            if phrase in no_newline_para:
                no_newline_para = ""
        if no_newline_para == "" or no_newline_para == "  ":
            pass
        else:
            print(f'"{no_newline_para}",')
            f.write(f'"{no_newline_para}",')
    # Print line break and close file
    print(f'\n')
    f.write(f'\n')
    f.close()