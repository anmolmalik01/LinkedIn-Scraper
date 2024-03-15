from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from utils.pprofile import ProfileScraper
import time
import csv


options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://www.linkedin.com/login')
driver.find_element(By.ID, 'username').send_keys('garimamalik1011@gmail.com')
driver.find_element(By.ID,'password').send_keys('Anmol@123')
driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
print(" =================== Successful login =================== ")



#*********** Search Result ***************#
search_key = "hr gurgoan" # Enter your Search key here to find people
key = search_key.split()
keyword = ""
for key1 in key:
    keyword = keyword + str(key1).capitalize() +"%20"
keyword = keyword.rstrip("%20")
            
global data
data = []

for no in range(1,2):
    start = "&page={}".format(no) 
    search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
    driver.get(search_url)
    print(search_url)
    
    # for scroll in range(2):
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    time.sleep(2)

    # Save page_source to a file
    with open("./data/page_source.html", "w", encoding='utf-8') as file:
        file.write(page_source)

    # Save soup to a file
    with open("./data/soup.html", "w", encoding='utf-8') as file:
        file.write(str(soup))


    

#     ul_elements = soup.find_all('ul', class_='reusable-search__entity-result-list')
#     ul_element = ul_elements[1]
    
#     if ul_elements:
        
#         li_elements = ul_element.find_all('li', class_='reusable-search__result-container')


#         for li in li_elements:
#             a_tag = li.find('a')

#             if a_tag and a_tag.get('href'):
#                 href = a_tag.get('href')
#                 text_before_question_mark = href.split('?')[0]
#                 data.append(text_before_question_mark)
#                 # print(text_before_question_mark)
#             else:
#                 print("a tag not found within the span")
#     else:
#         print("ul not found.")


# print(data)

print("=================== data fetched ===================")

# csv_file = './data/links.txt'
# # Write data to CSV file
# with open(csv_file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)

print("========================= data pushed ====================")

# scraper = ProfileScraper()
# for person in data:
#     scraper.scrape_profile(driver, person)