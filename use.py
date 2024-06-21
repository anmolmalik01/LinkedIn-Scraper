import os
import json
import pickle
import time
from selenium import webdriver
from fake_useragent import UserAgent

from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.linkedin_profile import ProfileScraper
from utils.search import SearchOnGoogle

# --- format ---
# page_number ,occupation, location_searched, profile_name, profile_title, profile_location, website_link, phone_number, email


class use():
    _finger_print_defender_ext = './extensions/finger_print_defender.crx'

    def __init__(self, create_cookies=False, use_links=False, occupation=None, location=None, count=None):
        
        self.create_cookies = create_cookies
        
        self.use_links = use_links
        
        self.occupation = occupation
        self.location = location
        self.count = count


    def run(self):
        driver = self.create_driver()

        try:
            if(self.create_cookies):
                self.generate_cookies(driver)

            else:
                self.add_cookies(driver)
                print("-> LOGIN AND ADDED cookies")
                time.sleep(30)

            # --------------------------------
                links_list = []
                
                if self.use_links:
                    with open('./data/linkedin_urls.txt', 'r') as file:
                        for line in file:
                            link = line.strip()
                            if link:
                                links_list.append(link)

                else:
                    num_scrolls = 1
                    links_list = self.search_on_google(driver, self.occupation, self.location, num_scrolls)
                    print("-> Collected the names from google")
                    time.sleep(5)


                for link in links_list:
                    try:
                        self.scrape(driver, url=link)
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        break
                print("SAVED")

        except Exception as e:
            print(f"## ERROR {e}")

        finally:
            self.clean()
            self.quit(driver)


    def get_random_user_agent(self):
        ua = UserAgent()
        return ua.random


    def create_driver(self):
        options = Options()

        # Basic configurations
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

        # Disable unwanted features for fingerprinting prevention and data leakage
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Set window size and position to prevent fingerprinting
        options.add_argument("--window-size=1366,768")
        options.add_argument("--window-position=0,0")

        options.add_extension(self._finger_print_defender_ext)

        # Set the user agent to a random one to prevent fingerprinting
        options.add_argument(f"--user-agent={self.get_random_user_agent()}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)        
        stealth(
            driver=driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32"
        )

        return driver


    def search_on_google(self, driver, occupation, location, num_scrolls):
        url = f'https://www.google.com/search?q=site:linkedin.com/in/ AND \"{occupation}\" AND \"{location}\"'

        scraper = SearchOnGoogle(driver)
        scraper.start(url, num_scrolls)
        links = scraper.get_data()

        return links


    def add_cookies(self, driver):
        driver.get('https://www.linkedin.com/login')

        cookies_file = "cookies.pkl"

        # print("Cokkies FOUND")
        if (os.path.getsize(cookies_file) == 0):
           os.remove(cookies_file)
        else:
            cookies = pickle.load(open(cookies_file, "rb"))

            for cookie in cookies:
                driver.add_cookie(cookie)
        
        driver.get('https://www.linkedin.com')


    def generate_cookies(self, driver):
        
        files_cwd = [f for f in os.listdir('.') if os.path.isfile(f)]
        for file in files_cwd:
            if os.path.exists('cookies.pkl'):
                # Attempt to delete the file
                os.remove('cookies.pkl')
                print(f"File deleted successfully.")

        driver.get('https://www.linkedin.com/login')

        input("Login and press ENTER")
        cookies = driver.get_cookies()

        cookies_filename = os.path.join(os.getcwd(), f"cookies.pkl")

        with open(cookies_filename, "wb") as file:
            pickle.dump(cookies, file)


    def scrape(self, driver, url):
        profile_scrape = ProfileScraper()
        profile_scrape.scrape_profile(driver, url)
        data = profile_scrape.get_data()

        self.save(data)


    def save(self, data):
        try:
            with open('./data/scraped.json', 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        existing_data.append(data)

        with open('./data/scraped.json', 'w') as file:
            json.dump(existing_data, file, indent=4)


    def clean(self):
        with open('./data/scraped.json', 'r') as file:
            existing_data = json.load(file)

        unique_people = []
        for person in existing_data:

            if person["email"]!= 'Not Available':
                unique_people.append(person)
                print('## Keeping people')

        with open('./data/scraped.json', 'w') as file:
            json.dump(unique_people, file, indent=4)


    def quit(self, driver):
        driver.quit()