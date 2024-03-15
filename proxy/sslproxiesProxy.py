import requests
from bs4 import BeautifulSoup
import random

# header example
# ['159.89.238.24', '8000', 'US', 'United States', 'anonymous', 'no', 'yes', '2 hours 40 mins ago']

class SSLProxiesProxyManager:
    def __init__(self):
        self.proxies = []
        self.proxiesInFormat = []

    def fetch_free_proxies(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            if cols:
                self.proxies.append(cols)
                

    def make_proxy_list(self, country, url='https://www.sslproxies.org/', ip_index=0, port_index=1, country_index=3):
        self.fetch_free_proxies(url)

        country_proxies = [proxy for proxy in self.proxies if proxy[country_index].lower() == country.lower()]

        for proxy in country_proxies:
            if ( proxy[ip_index] == 'SOCKS4' or proxy[ip_index] == 'SOCKS4'  ):
                pp = f"SOCKS4://{proxy['ip']}:{proxy['port']}"
                self.proxiesInFormat.append(pp)

            else:
                pp = f"{proxy[ip_index]}:{proxy[port_index]}"
                self.proxiesInFormat.append(pp)

        return self.proxiesInFormat
    

    def get_working_proxies(self):
        return self.workingProxy