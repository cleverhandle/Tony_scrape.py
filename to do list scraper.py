import csv
import time
import re
import json
import urllib.request

# Web Browser independent Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

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


def get_dates():
    with open('C:\\Users\\12544\\Documents\\scrape dates.csv', 'r') as read_obj:  # read csv file as a list of lists
        csv_reader = csv.reader(read_obj)  # pass the file object to reader() to get the reader object
        list_of_dates = list(csv_reader)  # Pass reader object to list() to get a list of lists
    #make sure every month or day has two digits
    for date in list_of_dates:
        if len(date[0]) < 2:
            two_digit_month = "0" + date[0]
            date[0] = two_digit_month
        if len(date[1]) < 2:
            two_digit_day = "0" + date[1]
            date[1] = two_digit_day
    return(list_of_dates)


def prep_output_file(file_to_prep):
    open(file_to_prep, 'w').close()  # makes sure the writing starts at front of file
    f = open(file_to_prep, "a")
    f.write(f'Date,Title,Link,Location\n')
    f.close()
    return()


def clean_location(location):
    online_list = ['Apply online', 'Submit online', 'Virtual', 'Online via Zoom', 'Online', 'Livestream Event',
                   'PRE-RECORDED', 'Online', 'Webinar', 'Your Laptop', 'VIRTUAL MEETING', '(ONLINE EVENT)', 'ONLINE',
                   'Online-Zoom', 'Online - Zoom', 'Virtual Event', 'Virtual Zoom', 'Virtual Workshop',
                   'Virtual Event Only', 'Virtual Event [Online Only]', 'Online Event', 'ZOOM ONLINE', 'Zoom',
                   'Austin , Online', 'FREE Webinar', 'FREE WEBINAR', 'Virtual via Zoom']
    for word in online_list:
        if word == location:
            location = 'Delete'
    secret_list = ['For venue details', 'Link will be given', 'Secret Location', 'Provided upon Booking',
                   'sent in confirmation', 'upon registration', 'Address will be emailed', 'sent with RSVP',
                   'Private House', 'TBA', 'To be announced', 'TBD', 'To Be Determined']
    for word in secret_list:
        if word in location:
            location = 'Delete'
    library_list = ['Austin Central Library, Austin Public Library', 'Austin Public Library Central Library',
                    'Central Library', 'Austin Central Library, Creative Commons Room']
    for word in library_list:
        if word == location:
            location = 'Austin Public Library - Central'
    other_library_list = ['Austin Public Library Twin Oaks Branch', 'Twin Oaks Branch Library',
                          'Twin Oaks Branch, Austin Public Library']
    for word in other_library_list:
        if word == location:
            location = 'Austin Public Library - Twin Oaks'
    another_library_list = ['Windsor Park Branch, Austin Public Library', 'Windsor Park Branch Library']
    for word in another_library_list:
        if word == location:
            location = 'Austin Public Library - Windsor Park'
    dogwood_list = ['Dogwood (West Sixth)', 'Dogwood West 6th']
    for word in dogwood_list:
        if word == location:
            location = 'Dogwood (West 6th)'
    easy_tiger_south_list = ['Easy Tiger (S. Lamar)', 'Easy Tiger (South Lamar)']
    for word in easy_tiger_south_list:
        if word == location:
            location = 'Easy Tiger South'
    easy_tiger_east_list = ['Easy Tiger (East 7th)', 'Easy Tiger (East)']
    for word in easy_tiger_east_list:
        if word == location:
            location = 'Easy Tiger East'
    last_stand_list = ['Last Stand Brewing Company', 'Last Stand Brewing SoCo']
    for word in last_stand_list:
        if word == location:
            location = 'Last Stand Brewing'
    oasis_list = ['Oasis Brewing Company', 'Oasis Texas Brewing Company', 'Oasis Brewing']
    for word in oasis_list:
        if word == location:
            location = 'Oasis Texas Brewing Company'
    victory_grill_list = ['Historic Victory Grill', 'The Historic Victory Grill']
    for word in victory_grill_list:
        if word == location:
            location = 'Victory Grill'
    mohawk_list = ['Mohawk Austin', 'The Mohawk-Austin']
    for word in mohawk_list:
        if word == location:
            location = 'Mohawk'
    quackenbush_list = ['Soundspace at Captain Quacks', "Soundspace at Captain Quack's",
                        'Captain Quackenbushs Coffeehouse', "Captain Quackenbush's, 5326 Menchaca",
                        "Captain Quackenbush's Coffeehouse And Bakery"]
    for word in quackenbush_list:
        if word == location:
            location = "Captain Quackenbush's Coffeehouse"
    native_list = ['Native Bar + Cafe', "Native Hostel and Bar & Cafe", "The Native", "Native Hostel"]
    for word in native_list:
        if word == location:
            location = "Native Bar & Cafe"
    volstead_list = ['Hotel Vegas', "Volstead Lounge", "HOTEL VEGAS"]
    for word in volstead_list:
        if word == location:
            location = "Hotel Vegas & The Volstead Lounge"
    auditorium_list = ['Vic Mathias Shores', "Vic Mathias Shores (Auditorium Shores)"]
    for word in auditorium_list:
        if word == location:
            location = "Auditorium Shores"
    stubbs_list = ["Stubb's Bar-B-Q", "Stubbs Waller Creek Amphitheater", "Stubb's Waller Creek Amphitheater",
                   "Stubb's Barbeque", "Stubb's BBQ"]
    for word in stubbs_list:
        if word == location:
            location = "Stubb's"
    jester_list = ["Jester King Craft Brewery", "The Hall at Jester King", "The Hall At Jester King"]
    for word in jester_list:
        if word == location:
            location = "Jester King Brewery"
    paramount_list = ["Paramount And Stateside Theatres", "Paramount Theatre-Austin",
                      "Paramount Theatre for the Performing Arts", "Stateside at the Paramount"]
    for word in paramount_list:
        if word == location:
            location = "Paramount Theatre"
    emos_list = ["Emos", "Emos-Austin", "Emo's-Austin", "Emo's Austin"]
    for word in emos_list:
        if word == location:
            location = "Emo's"
    antones_list = ["Antone's Nightclub", "Antones"]
    for word in antones_list:
        if word == location:
            location = "Antone's"
    fourth_list = ["Fourth & Co", "fourth & co"]
    for word in fourth_list:
        if word == location:
            location = "Fourth & Co."
    three_ten_list = ["3ten Austin City Limits Live", "3TEN", "3TEN ACL Live"]
    for word in three_ten_list:
        if word == location:
            location = "3TEN Austin City Limits Live"
    scoot_inn_list = ["Historic Scoot Inn", "The Scoot Inn"]
    for word in scoot_inn_list:
        if word == location:
            location = "Scoot Inn"
    spiderhouse_list = ["The Ballroom", "Spider House Ballroom", "Spider House Cafe and Ballroom",
                        "The Ballroom @ Spiderhouse", "Ballroom at Spiderhouse", "The Ballroom @ Spider House"]
    for word in spiderhouse_list:
        if word == location:
            location = "The Ballroom At Spiderhouse"
    acl_list = ["Austin City Limits Live at The Moody Theater", "ACL Live", "ACL Live At The Moody Theater"]
    for word in acl_list:
        if word == location:
            location = "ACL Live at the Moody Theater"
    fsg_list = ["211 E Alpine", "Feels So Good Records"]
    for word in fsg_list:
        if word == location:
            location = "Feels So Good"
    cota_list = ["Circuit Of The Americas", "Circuit of The Americas", "Germania Insurance Amphitheater"]
    for word in cota_list:
        if word == location:
            location = "Circuit of the Americas"
    if location == "Oilcan's":
        location = "Oilcan Harry's"
    elif location == "C-Boy's Heart & Soul Bar":
        location = "C-Boy's Heart & Soul"
    elif location == "Come And Take It Live":
        location = "Come & Take It Live"
    elif location == "Regus Business Centre":
        location = "Delete"
    elif location == "Regus - Texas, Austin - 100 Congress":
        location = "Delete"
    elif location == "The Austin Beer Garden Brewing Co.":
        location = "The ABGB"
    elif location == "The Creek And The Cave":
        location = "The Creek and the Cave"
    elif location == "The Saxon Pub":
        location = "Saxon Pub"
    elif location == "Come and Take It Live":
        location = "Come & Take It Live"
    elif location == "Ballet Austin's Butler Center For Dance & Fitness":
        location = "Ballet Austin"
    elif location == "Big Medium":
        location = "Big Medium Gallery"
    elif location == "Central Machine Works Brewery & Beer Hall":
        location = "Central Machine Works"
    elif location == "Geraldine's Austin":
        location = "Geraldine's"
    elif location == "Hole In The Wall":
        location = "Hole in the Wall"
    elif location == "Link & Pin":
        location = "Link & Pin Gallery"
    elif location == "Lone Star Court":
        location = "Lone Star Court Hotel"
    elif location == "Meanwhile Brewing":
        location = "Meanwhile Brewing Co."
    elif location == "Shore Raw Bar And Grill":
        location = "Shore Raw Bar & Grill"
    elif location == "Trinity Street Theatre":
        location = "Trinity Street Playhouse"
    elif location == "Whitewater Music Amphitheater":
        location = "Whitewater Amphitheater"
    elif location == "Zach Theatre":
        location = "ZACH Theatre"
    elif location == "Flatbed Center For Contemporary Printmaking":
        location = "Flatbed Press"
    elif location == "Long Center For The Performing Arts":
        location = "Long Center for the Performing Arts"
    elif location == "St. Elmo Brewing Company":
        location = "St. Elmo Brewing Co."
    elif location == "LUXE Refill":
        location = "Luxe Refill"
    elif location == "Capital Factory Downtown":
        location = "Capital Factory"
    elif location == "Austin Eastciders Barton Springs - Restaurant":
        location = "Austin Eastciders Barton Springs"
    elif location == "Desert Door Distillery":
        location = "Desert Door"
    elif location == "Palmer Event Center":
        location = "Palmer Events Center"
    elif location == "Rio Rooftop":
        location = "RIO"
    elif location == "Rio Nightclub":
        location = "RIO"
    elif location == "The Buzz Mill":
        location = "Buzz Mill"
    elif location == "TIGER DEN":
        location = "Tiger Den"
    elif location == "Zilker Metropolitan Park":
        location = "Zilker Park"
    elif location == "Beverly S. Sheffield Zilker Hillside Theater":
        location = "Zilker Hillside Theater"
    elif location == "Dreamland Dripping Springs":
        location = "Dreamland"
    elif location == "Flow Yoga, 202 Walton Way #200, Cedar Park":
        location = "Flow Yoga Cedar Park"
    elif location == "Flow Yoga, 4477 S. Lamar":
        location = "Flow Yoga Westgate"
    elif location == "Friends Bar":
        location = "Friends"
    elif location == "George Washington Carver Museum and Cultural Center":
        location = "George Washington Carver Museum"
    elif location == "Mary Kyle Hartson City Square Park, 101 S. Burleson St., Kyle":
        location = "Mary Kyle Hartson City Square Park"
    elif location == "Shooters Billiards & Sports Bar - Cedar Park":
        location = "Shooters Billiards Cedar Park"
    elif location == "The Contemporary Austin":
        location = "The Contemporary Austin At The Jones Center"
    elif location == "711 Red River St":
        location = "The Green Jay"
    elif location == "The Continental Club":
        location = "Continental Club"
    elif location == "The Continental Club Gallery":
        location = "Continental Club Gallery"
    elif location == "H-E-B Center At Cedar Park":
        location = "H-E-B Center at Cedar Park"
    elif location == "Slackers Brewing, 12233 RR 620 N":
        location = "Slackers Brewing Co."
    elif location == "Round Rock Amp":
        location = "Round Rock Amphitheater"
    elif location == "Flow Yoga Westgate, 4477 S. Lamar":
        location = "Flow Yoga Westgate"
    elif location == "Aquaholics Watercraft Rental":
        location = "Aquaholics Watercraft Rentals"
    elif location == "Moody Amphitheater At Waterloo Park":
        location = "Moody Amphitheater"
    elif location == "Icosa Collective":
        location = "ICOSA"
    elif location == "The Community Cinema At Mobile Loaves And Fishes":
        location = "Community First! Village"
    elif location == "Empire Control Room":
        location = "Empire Control Room & Garage"
    elif location == "The Cathedral ATX":
        location = "The Cathedral"
    elif location == "Moxy Hotel Austin University":
        location = "Moxy Austin - University"
    elif location == "906 E. Fifth #202":
        location = "Sí Gallery"
    elif location == "820 Shelby #103":
        location = "Almost Real Things"
    elif location == "3509 Banton":
        location = "Really Small Museum"
    elif location == "Hearth & Soul, 2727 Exposition":
        location = "Hearth & Soul"
    elif location == "5606 Meadow Crest":
        location = "The Meadow Crest"
    elif location == "The Elephant Room":
        location = "Elephant Room"
    elif location == "Moody Center ATX":
        location = "Moody Center"
    elif location == "Long Play Lounge East":
        location = "The Long Play Lounge (East)"
    elif location == "Hideout Theatre & Coffeehouse":
        location = "The Hideout Theatre"
    elif location == "Emma S. Barrientos Mexican American Cultural Center":
        location = "Mexican American Cultural Center"
    elif location == "Little Longhorn Saloon":
        location = "The Little Longhorn Saloon"
    elif location == "1311 Harvey":
        location = "Really Small Museum"
    elif location == "Art For The People Gallery":
        location = "Art For The People"
    elif location == "Baker Street Pub & Grill":
        location = "Baker St. Pub & Grill"
    elif location == "8505 Dittmar Oaks Dr":
        location = "Rad House"
    elif location == "Austin Saengerrunde":
        location = "Saengerrunde Hall"
    elif location == "Four Seasons Hotel Austin":
        location = "Four Seasons Hotel"
    elif location == "Trace at the W Hotel":
        location = "TRACE At The W Hotel"
    elif location == "Blanton Museum Of Art":
        location = "The Blanton Museum of Art"
    elif location == "The Lucky Duck":
        location = "Lucky Duck"
    elif location == "Crashbox":
        location = "CRASHBOX"
    elif location == "Summit Rooftop Lounge":
        location = "Summit Rooftop And Lounge"
    elif location == "Summit Rooftop & Lounge":
        location = "Summit Rooftop And Lounge"
    elif location == "The Parish Room - TX":
        location = "Parish"
    elif location == "Kick Butt Coffee Music & Booze":
        location = "Kick Butt Coffee"
    elif location == "Sterling Event Center":
        location = "Sterling Events Center"
    elif location == "Cloud Tree Studios":
        location = "Cloud Tree Studios & Gallery"
    elif location == "Cloud Tree Studios And Gallery":
        location = "Cloud Tree Studios & Gallery"
    elif location == "Cloud Tree":
        location = "Cloud Tree Studios & Gallery"
    elif location == "Yard Dog":
        location = "Yard Dog Art Gallery"
    elif location == "7412 Albert Rd":
        location = "ĀTMA Church"
    elif location == "Pedernales Station":
        location = "Monks Jazz Club"
    elif location == "Pershing Hall":
        location = "The Pershing"
    elif location == "Batch Craft Beer + Kolaches":
        location = "Batch Craft Beer & Kolaches"
    elif location == "Darrell K. Royal-Texas Memorial Stadium":
        location = "Darrell K Royal - Memorial Stadium"
    elif location == "DKR Texas Memorial Stadium":
        location = "Darrell K Royal - Memorial Stadium"
    elif location == "Darrell K Royal - Texas Memorial Stadium":
        location = "Darrell K Royal - Memorial Stadium"
    elif location == "Family Business Beer Company":
        location = "Family Business Beer Co."
    elif location == "Independence Brewing Co":
        location = "Independence Brewing Company"
    elif location == "Hopsquad Brewing Co":
        location = "Hopsquad Brewing Co."
    elif location == "Lutie's Garden Restaurant":
        location = "Lutie's"
    elif location == "Metz Neighborhood Park":
        location = "Metz Park"
    elif location == "Pinballz Arcade Lake Creek":
        location = "Pinballz Lake Creek"
    elif location == "Wanderlust Wine Collective":
        location = "Wanderlust Wine Co."
    elif location == "Wanderlust Wine Collective (East)":
        location = "Wanderlust Wine Co."
    elif location == "Wanderlust Wine Co":
        location = "Wanderlust Wine Co."
    elif location == "THE FAR OUT LOUNGE":
        location = "The Far Out Lounge & Stage"
    elif location == "Butterfly Bar at the Vortex":
        location = "Butterfly Bar"
    elif location == "The Butterfly Bar @ The VORTEX":
        location = "Butterfly Bar"
    elif location == "The Line Hotel Austin":
        location = "The LINE Hotel Austin"
    elif location == "LifeAustin Amphitheater":
        location = "LifeAustin Amphitheatre"
    return(location)


def scrape_do512(list_of_dates, output_file):
    for date in list_of_dates:
        readable_date = (date[0] + '/' + date[1] + '/' + date[2])
        new_url = 'https://do512.com/events/' + date[2] + '/' + date[0] + '/' + date[1]

        dailyurls = []
        dailyurls.append(new_url)

        # is there a next page for that date
        browser.get(new_url)
        next_page = 'y'
        while next_page == 'y':
            pagesource = browser.page_source
            if 'next page' in pagesource.lower():
                next_page_element = browser.find_element(By.CSS_SELECTOR, 'a[class="ds-next-page"]')
                dailyurls.append(next_page_element.get_attribute('href'))
                nextpagebutton = browser.find_element(By.CSS_SELECTOR, 'a[class="ds-next-page"]')
                nextpagebutton.click()
                pagesource = browser.page_source
            else:
                next_page = 'n'

        #Get data for every page
        for url in dailyurls:
            browser.get(url)
            time.sleep(1)

            titlelist = []
            titleelements = browser.find_elements(By.CSS_SELECTOR, 'span[class="ds-listing-event-title-text"]')
            for title in titleelements:
                try:
                    titlelist.append(title.get_attribute('innerText'))
                except StaleElementReferenceException:
                    time.sleep(3)
                    titlelist.append(title.get_attribute('innerText'))
                    print('getting title second time worked') 

            urllist = []
            urlelements = browser.find_elements(By.CSS_SELECTOR, 'a[class="ds-listing-event-title url summary"]')
            for url in urlelements:
                urllist.append(url.get_attribute('href'))

            locationlist = []
            locationelements = browser.find_elements(By.CSS_SELECTOR, 'div[class="ds-venue-name"]')
            for location in locationelements:
                location_with_space = location.get_attribute('innerText')
                location_no_space = location_with_space.strip()
                location_no_space = clean_location(location_no_space)
                locationlist.append(location_no_space)

            datelist = []
            for event in titlelist:
                datelist.append(readable_date)

            finallist = list(zip(datelist, titlelist, urllist, locationlist))

            for event in finallist:  # Removes duplicates
                finallist.remove(event)

            for event in list(finallist):  # Removes all events are supposed to be deleted
                if event[3] == 'Delete':
                    finallist.remove(event)

            for event in finallist:
                print(f'{event[0]}, {event[1]}, {event[2]}, {event[3]}\n')

            # Writes to a file
            try:
                with open(output_file, "a") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
            except:
                print(f'This didnt write to file - {event[0]}, {event[1]}, {event[2]}, {event[3]}\n')
                with open(output_file, "a", encoding="utf-8") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
    return


def scrape_chronicle(list_of_dates, output_file):
    no_check_urls = []  # Chronicle makes sure we only have to check the many dumb events once. This list tracks them
    for date in list_of_dates:
        readable_date = (date[0] + '/' + date[1] + '/' + date[2])
        new_url = 'https://www.austinchronicle.com/events/' + date[2] + '-' + date[0] + '-' + date[1] + '/'

        # figure out how many pages per day
        dailyurls = []
        dailyurls.append(new_url)
        browser.get(new_url)
        pagesource = browser.page_source
        nextpage = 'y'
        while nextpage == 'y':
            if 'page-button page-next page-dead' not in pagesource.lower():
                next_page_element = browser.find_element(By.CSS_SELECTOR, 'a[title="next"]')
                dailyurls.append(next_page_element.get_attribute('href'))
                nextpagebutton = browser.find_element(By.CSS_SELECTOR, 'div[class="page-button page-next"]')
                nextpagebutton.click()
                pagesource = browser.page_source
            else:
                nextpage = 'n'

        #go get all the data for everything
        for url in dailyurls:
            browser.get(url)
            titlelist = []
            titleelements = browser.find_elements(By.CSS_SELECTOR, 'h2')
            gallery_list = ['Big Medium: ', 'Butridge Gallery: ', 'Cloud Tree Gallery: ', 'ICOSA: ', 'MACC: ',
                            'ART Ahead: ', 'Camiba Gallery: ', 'Davis Gallery: ', 'Elisabet Ney Museum: ',
                            'Flatbed Press: ', 'Hyde Park Bar & Grill: ', 'Link & Pin Gallery: ',
                            'Lora Reynolds Gallery: ', 'Neill-Cochran House: ', 'Northern-Southern: ', 'RSM: ',
                            'Sí Gallery: ', 'The Blanton: ', 'The Contemporary Austin: ', 'Wild Basin: ',
                            'Women & Their Work: ', 'Artworks Gallery: ', 'Carver Museum: ', 'Wally Workman Gallery: ',
                            'Art for the People: ', 'Really Small Museum: ', 'GrayDUCK Gallery: ',
                            'Lydia Street Gallery: ', 'Sage Studio: ', 'ACC Art Galleries: ',
                            'Art for the People Gallery: ', 'Hyde Park Grill: ', 'Ivester Contemporary: ',
                            'West Chelsea Contemporary: ', 'Yard Dog: ', 'Cloud Tree: ', 'HPB&G: ',
                            'Modern Rocks Gallery: ', 'Austin Art Space: ', 'Canvas: ', 'Goodluckhavefun Gallery: ',
                            'Prizer Arts & Letters: ']
            for title in titleelements:
                raw_title = title.get_attribute('innerText')
                one_time = re.sub("\([0-9]*:[a-z,A-Z,0-9]*\)", " ", raw_title)
                two_times = re.sub("\([0-9]*:[a-z,A-Z,0-9]*, [0-9]*:[a-z,A-Z,0-9]*\)", " ", one_time)
                clean_title = two_times
                for gallery in gallery_list:
                    if gallery in two_times:
                        clean_title = two_times.replace(gallery, "")
                titlelist.append(clean_title)

            urllist = []
            urlelements = browser.find_elements(By.CSS_SELECTOR, 'h2')
            for url in urlelements:
                rawurl = url.get_attribute('innerHTML')
                cleanfront = rawurl.replace("<a href=", " ")
                nosponsor = re.sub(" target[a-z,A-Z,0-9,\s\S]*", " ", cleanfront)
                cleanback = re.sub(">[a-z,A-Z,0-9,\s\S]*", " ", nosponsor)
                noquotes = cleanback.replace('"', " ")
                nospaces = noquotes.join(noquotes.split())
                if "http" in nospaces:
                    finalurl = nospaces
                else:
                    finalurl = (f"https://www.austinchronicle.com{nospaces}")
                urllist.append(finalurl)

            locationlist = []
            for url in urllist:
                if 'out-of-town' in url:
                    location = 'Delete'
                elif 'civic-events' in url:
                    location = 'Delete'
                elif 'seasonal-jobs' in url:
                    location = 'Delete'
                elif 'donate-blood' in url:
                    location = 'Delete'
                elif 'we-are-blood' in url:
                    location = 'Delete'
                elif url in no_check_urls:
                    location = 'Delete'
                elif 'chronicle' in url:
                    try:
                        browser.get(url)
                        browser.set_page_load_timeout(15)
                        time.sleep(1)
                        locationelements = browser.find_element(By.CSS_SELECTOR, 'div[class="venue"]')
                        location = locationelements.get_attribute('innerText')
                        if len(location) < 1:
                            location = 'Delete'
                        location = clean_location(location)
                        if location != 'Delete':
                            pagesource = browser.page_source
                            if 'no events scheduled.' in pagesource.lower():
                                location = 'Delete'
                    except NoSuchElementException:
                        print(f'{url} no venue listed.')
                        location = 'Check location'
                    except TimeoutException:
                        print(f'{url} took too long.')
                        location = 'Check location'
                        time.sleep(3)
                    except WebDriverException:
                        print(f'{url} Webdriver exception whatever that means.')
                        location = 'Check location'
                else:
                    location = 'Check location'
                locationlist.append(location)

            datelist = []
            for event in titlelist:
                datelist.append(readable_date)

            finallist = list(zip(datelist, titlelist, urllist, locationlist))

            for event in list(finallist):  # Removes all events are supposed to be deleted
                if event[3] == 'Delete':
                    finallist.remove(event)
                    if event[2] not in no_check_urls:
                        no_check_urls.append(event[2])

            # prints so you can see progress
            for event in finallist:
                print(f'{event[0]}, {event[1]}, {event[2]}, {event[3]}\n')

            # Writes to a file
            try:
                with open(output_file, "a") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
            except:
                print(f'This didnt write to file - {event[0]}, {event[1]}, {event[2]}, {event[3]}\n')
                with open(output_file, "a", encoding="utf-8") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
    return()


def scrape_eventbrite(list_of_dates, output_file):
    for date in list_of_dates:
        readable_date = (date[0] + '/' + date[1] + '/' + date[2])
        category_list = ['business', 'food-and-drink', 'health', 'music', 'auto-boat-and-air', 'charity-and-causes',
                         'community', 'family-and-education', 'fashion', 'film-and-media', 'hobbies',
                         'home-and-lifestyle', 'arts', 'government', 'spirituality', 'school-activities',
                         'science-and-tech', 'holiday', 'sports-and-fitness', 'travel-and-outdoor', 'other']
        bad_city_list = ['San Antonio', 'Charlotte', 'New Braunfels', 'Florence', 'Hutto', 'Seguin',
                         'Belton', 'Temple', 'Killeen', 'Arlington', 'Fort Hood', 'San Marcos',
                         'Bandera', 'Bankersmith', 'Dallas', 'Schulenburg', 'McDade', 'Boerne', 'Leander',
                         'Spring Branch', 'College Station', 'Harper', 'Selma', 'Salado', 'Cibolo', 'Converse',
                         'Floresville', 'Bulverde', 'Belton', 'Gatesville', 'Bastrop', 'Driftwood', 'Harker Heights',
                         'Allentown', 'Columbus', 'Lubbock']
        for category in category_list:
            try:
                new_url = 'https://www.eventbrite.com/d/tx--austin/' + category + '--events/?end_date=' + date[
                    2] + '-' + date[0] + '-' + date[1] + '&page=1&start_date=' + date[2] + '-' + date[0] + '-' + date[1]
                browser.get(new_url)
                time.sleep(1)
                pagesource = browser.page_source

                if 'Nothing matched your search' not in pagesource:
                    titlelist = []
                    titleelements = browser.find_elements(By.CSS_SELECTOR,
                                                          'div[class="eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy"]')
                    for title in titleelements:
                        titlelist.append(title.get_attribute('innerText'))

                    urllist = []
                    urlelements = browser.find_elements(By.CSS_SELECTOR, 'a[tabindex="-1"]')
                    for url in urlelements:
                        urllist.append(url.get_attribute('href'))

                    locationlist = []
                    locationelements = browser.find_elements(By.CSS_SELECTOR, 'div[data-subcontent-key="location"]')
                    for location in locationelements:
                        location = location.get_attribute('innerText')
                        for city in bad_city_list:
                            if city in location:
                                location = 'Delete'
                        online_list = ['austin, texas • austin, tx', 'austin • austin, tx', 'webinar', 'online session']
                        for word in online_list:
                            if word in location.lower():
                                location = 'Delete'
                        location = re.sub(" •[a-z,A-Z,0-9,\s\S]*", "", location)
                        location = clean_location(location)
                        locationlist.append(location)

                    datelist = []
                    for event in titlelist:
                        datelist.append(readable_date)

                    finallist = list(zip(datelist, titlelist, urllist, locationlist))

                    for event in finallist:  # Removes duplicates
                        finallist.remove(event)


                    for event in list(finallist):  # Removes all events are supposed to be deleted
                        if event[3] == 'Delete':
                            finallist.remove(event)

                    for event in finallist:
                        print(f'{event[0]}, {event[1]}, {event[2]}, {event[3]}\n')

                    # Writes to a file
                    try:
                        with open(output_file, "a") as f:
                            for event in finallist:
                                f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
                    except:
                        print(f'This didnt write to file - {event[0]}, {event[1]}, {event[2]}, {event[3]}\n')
                        with open(output_file, "a", encoding="utf-8") as f:
                            for event in finallist:
                                f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
                else:
                    pass
            except:
                print('You got some kind of error on some category. Just skipping it.')
                pass
    return ()


def scrape_ticketmaster(list_of_dates, output_file):
    for date in list_of_dates:
        readable_date = (date[0] + '/' + date[1] + '/' + date[2])
        json_url = 'https://app.ticketmaster.com/discovery/v2/events.json?dmaId=222&radius=10&localStartDateTime=' + date[2] + '-' + date[0] + '-' + date[1] + 'T01:00:00,' + date[2] + '-' + date[0] + '-' + date[1] + 'T23:59:00&apikey=cCreliEDRmv42AfhoIdQOVPB1q9zD2L4'

        with urllib.request.urlopen(json_url) as url:
            data = json.loads(url.read().decode())
            titlelist = []
            urllist = []
            locationlist = []
            datelist = []
            try:
                for i in data['_embedded']['events']:
                    titlelist.append(i['name'])
                    urllist.append(i['url'])
                    location = (i['_embedded']['venues'][0]['name'])
                    location = clean_location(location)
                    san_antonio_location = ['221 Burleson Street', 'Laugh Out Loud Comedy Club', 'AT&T Center',
                                            'Alamodome', 'Majestic Theatre San Antonio', 'Aztec Theatre ',
                                            'Toyota Field', 'Freeman Coliseum', 'Alamodome Theater', 'Jo Long Theatre',
                                            'Charline McCombs Empire Theatre', 'Lila Cockrell Theatre']
                    for word in san_antonio_location:
                        if location == word:
                            location = 'Delete'
                    locationlist.append(location)
                    datelist.append(readable_date)
                    finallist = list(zip(datelist, titlelist, urllist, locationlist))

                for event in list(finallist):  # Removes all events are supposed to be deleted
                    if event[3] == 'Delete':
                        finallist.remove(event)

                for event in finallist:
                    print(f'{event[0]}, {event[1]}, {event[2]}, {event[3]}\n')

                # Writes to a file
                with open(output_file, "a") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
            except:
                print(f'Something went wrong with {json_url}')
                pass
    return()


def scrape_meetup(list_of_dates, output_file):
    for date in list_of_dates:
        readable_date = (date[0] + '/' + date[1] + '/' + date[2])
        if (date[0] == '01' and date[1] == '31'):
            next_month = '02'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '02' and date[1] == '28'):
            next_month = '03'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '03' and date[1] == '31'):
            next_month = '04'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '04' and date[1] == '30'):
            next_month = '05'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '05' and date[1] == '31'):
            next_month = '06'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '06' and date[1] == '30'):
            next_month = '07'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '07' and date[1] == '31'):
            next_month = '08'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '08' and date[1] == '31'):
            next_month = '09'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '09' and date[1] == '30'):
            next_month = '10'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '10' and date[1] == '31'):
            next_month = '11'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '11' and date[1] == '30'):
            next_month = '12'
            next_day = '01'
            next_year = date[2]
        elif (date[0] == '12' and date[1] == '31'):
            next_month = '01'
            next_day = '01'
            next_year = str(int(date[2]) + 1)
        else:
            next_month = date[0]
            next_day = str(int(date[1]) + 1)
            next_year = date[2]

        if len(next_day) < 2:
            next_day = "0" + next_day

        category_id = ['521', '405', '604', '612', '535', '511', '571', '622', '642', '395', '673', '701', '593', '436', '652', '482', '449', '546', '684', '467']
        for category in category_id:
            new_url = 'https://www.meetup.com/find/?location=us--tx--Austin&source=EVENTS&customStartDate=' + date[2] + '-' + date[0] + '-' + date[1] + 'T01%3A00%3A00-04%3A00&customEndDate=' + next_year + next_month + next_day + 'T00%3A59%3A00-04%3A00&eventType=inPerson&categoryId=' + category + '&distance=twentyFiveMiles'
            browser.get(new_url)
            time.sleep(1)
            pagesource = browser.page_source
            print(new_url)

            if 'Nothing matched your search' not in pagesource:
                titlelist = []
                titleelements = browser.find_elements(By.CSS_SELECTOR, 'div[class="eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy"]')
                for title in titleelements:
                    titlelist.append(title.get_attribute('innerText'))

                urllist = []
                urlelements = browser.find_elements(By.CSS_SELECTOR, 'a[tabindex="-1"]')
                for url in urlelements:
                    urllist.append(url.get_attribute('href'))

                locationlist = []
                locationelements = browser.find_elements(By.CSS_SELECTOR, 'div[data-subcontent-key="location"]')
                for location in locationelements:
                    location = location.get_attribute('innerText')
                    bad_city_list = ['San Antonio', 'Charlotte', 'New Braunfels', 'Florence', 'Hutto', 'Seguin', 'Belton', 'Temple', 'Killeen', 'Arlington', 'Fort Hood', 'San Marcos']
                    for city in bad_city_list:
                        if city in location:
                            location = 'Delete'
                    online_list = ['online', 'austin, texas • austin, tx', 'austin • austin, tx', 'virtual', 'webinar']
                    for word in online_list:
                        if word in location.lower():
                            location = 'Delete'
                    location = re.sub(" •[a-z,A-Z,0-9,\s\S]*", "", location)
                    location = clean_location(location)
                    locationlist.append(location)

                datelist = []
                for event in titlelist:
                    datelist.append(readable_date)

                finallist = list(zip(datelist, titlelist, urllist, locationlist))

                for event in finallist:  # Removes duplicates
                    finallist.remove(event)

                for event in list(finallist):  # Removes all events are supposed to be deleted
                    if event[3] == 'Delete':
                        finallist.remove(event)

                for event in finallist:
                    print(f'{event[0]}, {event[1]}, {event[2]}, {event[3]}\n')

                # Writes to a file
                with open(output_file, "a") as f:
                    for event in finallist:
                        f.write(f'{event[0]},"{event[1]}",{event[2]},"{event[3]}"\n')
            else:
                pass
    return ()

# program actually starts here
list_of_dates = get_dates()
prep_output_file("C:\\Users\\12544\\Documents\\Known Locations.csv")
scrape_do512(list_of_dates, "C:\\Users\\12544\\Documents\\Known Locations.csv")
scrape_eventbrite(list_of_dates, "C:\\Users\\12544\\Documents\\Known Locations.csv")
scrape_ticketmaster(list_of_dates, "C:\\Users\\12544\\Documents\\Known Locations.csv")
scrape_chronicle(list_of_dates, "C:\\Users\\12544\\Documents\\Known Locations.csv")

# scrape_meetup(list_of_dates, "C:\\Users\\12544\\Documents\\Known Locations.csv")