from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import tempfile

temp_dir = tempfile.mkdtemp()

ua = UserAgent()
def get_random_user_agent():
    return ua.random

def gen_chrome_options():
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-cookies")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-popup-blocking")

    # chrome_options.add_argument("--disable-webgl-canvas")
    # chrome_options.add_argument("--disable-plugins")
    # chrome_options.add_argument("--disable-sync")
    
    return chrome_options