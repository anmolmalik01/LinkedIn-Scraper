from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv

class ProfileScraper:
    def __init__(self):
        self.index = 1 # Initialize the index at 1

    def scrape_profile(self, driver, profile_url):
        """Scrape required fields from LinkedIn URL and save to CSV"""
        driver.get(profile_url)

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

        # Click on Contact Info link
        driver.find_element(By.ID, "top-card-text-details-contact-info").click()

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

        with open( './data/data.txt', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header if the file is new
            if file.tell() == 0:
                writer.writerow(["Index", "Name", "Title", "Location", "Website", "Phone_number", "E-Mail"])
            # Write the scraped data
            writer.writerow([self.index, profile_name, profile_title, profile_location, website_link, phone_number, email])

        print("=================== Pushed ===================")

        self.index += 1 # Increment the index after each profile
