import csv
import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ProfileScraper:
    def __init__(self):
        self.data = [] # Initialize an empty list to store scraped data

    def scrape_profile(self, driver, profile_url):
        """Scrape required fields from LinkedIn URL and save to CSV"""

        driver.get(profile_url)
        wait = WebDriverWait(driver, 20)

        # Click on Contact Info link
        contact_locator = (By.ID, "top-card-text-details-contact-info")
        wait.until(EC.visibility_of_element_located(contact_locator))
        
        try:
            profile_name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").get_attribute("innerText")
        except NoSuchElementException:
            profile_name = "Not Available"

        try:
            profile_title = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").get_attribute("innerText")
        except NoSuchElementException:
            profile_title = "Not Available"

        try:
            profile_location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").get_attribute("innerText")
        except NoSuchElementException:
            profile_location = "Not Available"


        contact_element = driver.find_element(*contact_locator)
        contact_element.click()

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(2)
        
        # Extracting website
        website_link_element = soup.find('a', {'class': 'pv-contact-info__contact-link'})
        website_link = website_link_element['href'] if website_link_element else 'Not Available'

        # Extracting phone number
        phone_number_element = soup.find('span', {'class': 't-14 t-black t-normal'})
        phone_number = phone_number_element.text if phone_number_element else 'Not Available'

        # Use CSS selector to find the email link
        email_link_elements = soup.select('a[href^="mailto:"]')

        # Check if any elements were found and extract the email address
        if email_link_elements:
            email_link = email_link_elements[0]['href']
            email = email_link.replace('mailto:', '')
        else:
            email = 'Not Available'

        print("=================== Extracted info ===================")
        profile_data = {
            "name": profile_name,
            "title": profile_title,
            "location": profile_location,
            "website": website_link,
            "phone_number": phone_number,
            "email": email
        }
        self.data.append(profile_data)


    def get_data(self):
        """Return the scraped data"""
        return self.data