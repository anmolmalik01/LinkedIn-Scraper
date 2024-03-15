from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scroll_and_click(driver, num_scrolls):
    for _ in range(num_scrolls):
        # Scroll to the bottom of the page
        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # Allow time for the page to load new content
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

        # Click the "Show More" button
        try:
            show_more_button = driver.find_element(By.CSS_SELECTOR, '.T7sFge.sW9g3e.VknLRd')
            show_more_button.click()
            time.sleep(2) # Allow time for the new content to load
        except Exception as e:
            print(f"No 'Show More' button found: {e}")

# URL for Google search
url = "https://www.google.com/search?q=site:linkedin.com/in/ AND \"python developer\" AND \"London\""
num_scrolls = 1 # Number of times to scroll and click the button
linkedin_urls = set() # Use a set to store unique URLs

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)

# Scroll and click the button the specified number of times
scroll_and_click(driver, num_scrolls)


# Extract the LinkedIn URLs from the current page
current_urls = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')    
for url in current_urls:
    href = url.get_attribute('href')
    if href not in linkedin_urls: # Check if the URL is already in the set
        linkedin_urls.add(href) # Add the URL to the set

# Convert the set back to a list if needed
linkedin_urls = list(linkedin_urls)

# Print the extracted LinkedIn URLs
print(linkedin_urls)
