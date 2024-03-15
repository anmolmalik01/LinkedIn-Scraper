import requests
from requests.exceptions import ProxyError


class GeoNodeProxyManager:
    
    def __init__(self):        
        self.proxiesInFormat = []


    def fetch_free_proxies(self, api):
        try:
            response = requests.get(api)
            proxy_list = response.json()
            return proxy_list
        except requests.exceptions.RequestException as e:
            print(f"Error fetching proxies: {e}")
            return []
        finally:
            print("-> GeoNode fetch complete ===")

            
    def make_proxy_list(self, api):
        proxy_list = self.fetch_free_proxies(api)
        
        for proxy in proxy_list['data']:
            
            if ( (proxy['protocols'][0] == 'SOCKS4') or (proxy['protocols'][0] == 'SOCKS5') ):
                pp = f"{proxy['protocols'][0]}://{proxy['ip']}:{proxy['port']}"
                self.proxiesInFormat.append(pp)
            
            else:
                pp = f"{proxy['ip']}:{proxy['port']}"
                self.proxiesInFormat.append(pp)
        
        return self.proxiesInFormat
    
    def get_working_proxies(self):
        return self.proxiesInFormat


# if __name__ == "__main__":
#     country = 'US'
#     limit = '5'
#     api = f'https://proxylist.geonode.com/api/proxy-list?country={country}&filterLastChecked=60&limit={limit}&page=1&sort_by=lastChecked&sort_type=desc'
    
#     proxy_manager = GeoNodeProxyManager()
#     proxy_manager.make_proxy_list(api)
    
#     print(proxy_manager.get_working_proxies())
