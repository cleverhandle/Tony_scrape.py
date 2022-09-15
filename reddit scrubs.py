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

def blockpeople (dirtysubreddit, triggerwords):
    #open the page
    browser.get(dirtysubreddit)
    number_blocked = 0

    #Get webelement list of authors
    authors = "a[class^='author ']"
    authorlist = browser.find_elements(By.CSS_SELECTOR, authors)
    #Convert webelement list to string list
    authorstringlist = []
    for author in authorlist:
        authorstringlist.append(author.get_attribute('href')) #whitelist myself and Chloee_Mae

    #go to each author homepage, see if they have any keywords and then block them
    for author in authorstringlist:
        browser.get(author)
        pagesource = browser.page_source
        for word in triggerwords:
            if word in pagesource.lower():
                #print(f'{author} for {word}')
                try:
                    blockbutton = browser.find_element(By.CSS_SELECTOR, 'a[class="togglebutton access-required"]')
                    confirmbutton = browser.find_element(By.CSS_SELECTOR, 'a[class="yes"]')
                    blockbutton.click()
                    confirmbutton.click()
                    number_blocked = number_blocked + 1
                    print(f'blocked #{number_blocked} - {author} for {word}')
                except:
                    continue
    print(f'All done with {dirtysubreddit}')
    return

perverts = ['hentai', 'anime', '/rape', 'incest']
professionals = ['join my', 'onlyfans.com', 'my of', 'my onlyfans', 'camsoda', 'fansly', 'follow my', 'custom video', 'link in comments']

# Open reddit and login
browser.get("https://old.reddit.com/")
username = browser.find_element(By.CSS_SELECTOR, "input[name='user']")
password = browser.find_element(By.CSS_SELECTOR, "input[name='passwd']")
loginbutton = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")

username.send_keys("guyinaustin")
password.send_keys("!!Reddit00")
loginbutton.click()
time.sleep(3)

print("Logged In. We're blocking now.")

# blockpeople('https://old.reddit.com/user/guyinaustin/m/story/top/', perverts)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/whoknows/top/', professionals)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/video/top/', professionals)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/group/top/', professionals)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/milf/top/', professionals)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/amateur/top/', professionals)
# blockpeople('https://old.reddit.com/user/guyinaustin/m/boobs/top/', professionals)
blockpeople('https://old.reddit.com/r/Harem/', professionals)
blockpeople('https://old.reddit.com/r/Harem/', perverts)
