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
driver = webdriver.Firefox(service=service, options=options)

with open('C:\\Users\\12544\\Documents\\Unknown locations.csv', 'r') as read_obj: # read csv file as a list of lists
  csv_reader = csv.reader(read_obj) # pass the file object to reader() to get the reader object
  list_of_rows = list(csv_reader) # Pass reader object to list() to get a list of lists

#turns the list of lists into lists of strings
urllist = []
urllist = [''.join(ele) for ele in list_of_rows]

#makes a list of words to check for
possible_words = ['bats', 'hike and bike', 'greenbelt', 'lady bird', 'cathedral', 'apartment']

for page in urllist:
    driver.get(page) #go to the page
    time.sleep(5) # Wait for the entire web page to download and display.
    pagesource = driver.page_source
    possible_links = []
    for word in possible_words:
        if word in pagesource.lower():
            possible_links.append(word)
    print(f'{page}', end =" ")
    print(': '.join(possible_links))
    # Writes to a file
    f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a")
    f.write(f'{page} ,')
    f.write(', '.join(possible_links))
    f.write('\n')
    f.close()