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
possible_blog = ['/blog', '/news', '/press', 'posts', '/media', 'links']
possible_list = ['sign up','subscribe','newsletter','mailing list','e-mail']
possible_gift_card = ['gift card', 'gift certificate']

for page in urllist:
    try:
        driver.get(page)  # go to the page
        time.sleep(2)  # Wait for the entire web page to download and display.
        pagesource = driver.page_source
        blog = 'Nope'
        list = 'Nope'
        gift_card = 'Nope'
        for word in possible_blog:
            if word in pagesource.lower():
                blog = 'Yup'
        for word in possible_list:
            if word in pagesource.lower():
                list = 'Yup'
        for word in possible_gift_card:
            if word in pagesource.lower():
                gift_card = 'Yup'
        print(f'{page} : blog = {blog} : list = {list} : gift card = {gift_card}')

        # Writes to a file
        f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a")
        f.write(f'{page} ,{blog} ,{list} ,{gift_card}\n')
        f.close()
    except:
        blog = '???'
        list = '???'
        gift_card = '???'
        print(f'{page} : blog = {blog} : list = {list} : gift card = {gift_card}')
        # Writes to a file
        f = open("C:\\Users\\12544\\Documents\\Known Locations.csv", "a")
        f.write(f'{page} ,{blog} ,{list} ,{gift_card}\n')
        f.close()
