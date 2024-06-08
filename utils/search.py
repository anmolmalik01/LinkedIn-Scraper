from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


class SearchOnGoogle:
    
    def __init__(self, driver):

        self.driver = driver
        self.linkedin_urls = set()


    def scroll_and_click(self, num_scrolls):
        
        for _ in range(num_scrolls):
            prev_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == prev_height:
                    break
                prev_height = new_height

            try:
                show_more_button = self.driver.find_element(By.CSS_SELECTOR, '.T7sFge.sW9g3e.VknLRd')
                show_more_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"No 'Show More' button found: {e}")


    def collect_urls(self):
        current_urls = self.driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        for url in current_urls:
            href = url.get_attribute('href')
            if href not in self.linkedin_urls:
                self.linkedin_urls.add(href)


    def get_data(self):
        return self.linkedin_urls


    def save_urls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        with open('data/linkedin_urls.txt', 'w') as file:
            for url in self.linkedin_urls:
                file.write(f'{url}\n')


    def start(self, url, num_scrolls):
        
        self.driver.get(url)
        self.scroll_and_click(num_scrolls)
        self.collect_urls()
        self.save_urls()
        
        print(f'Collected LinkedIn URLs: {len(self.linkedin_urls)}')