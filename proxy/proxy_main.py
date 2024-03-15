import requests
import threading

from geonodeProxy import GeoNodeProxyManager
from sslproxiesProxy import SSLProxiesProxyManager

# ssl proxy -> country, url='https://www.sslproxies.org/, ip_index=0, port_index=1, country_index=3
# geonode   -> api


working_proxies = []
non_working_proxies = []
combined_proxy = []

lock = threading.Lock()
threads = []


# ====================== working proxy function =======================
def is_proxy_working(proxy, lock, working_proxies, non_working_proxies):
    try:
        response = requests.get('http://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            with lock:
                working_proxies.append(proxy)
                print(f'-> Working proxy: {proxy}')
        else:
            with lock:
                non_working_proxies.append(proxy)
                print(f'# Not Working proxy: {proxy}')
    except requests.exceptions.RequestException:
        with lock:
            non_working_proxies.append(proxy)
            print(f'# Not Working proxy: {proxy}')    



# =================== collecting proxies ===================
def collect_ssl_proxies(country, combined_proxy):
    ssl_manager = SSLProxiesProxyManager()
    ssl_manager.make_proxy_list(country)
    proxy1 = ssl_manager.get_working_proxies()
    with lock:
        combined_proxy.extend(proxy1)


def collect_geonode_proxies(country_code, limit, combined_proxy):
    api = f'https://proxylist.geonode.com/api/proxy-list?country={country_code}&filterLastChecked=60&limit={limit}&page=1&sort_by=lastChecked&sort_type=desc'
    geonode_manager = GeoNodeProxyManager()
    geonode_manager.make_proxy_list(api)
    proxy2 = geonode_manager.get_working_proxies()
    with lock:
        combined_proxy.extend(proxy2)


# Create threads for collecting proxies
ssl_thread = threading.Thread(target=collect_ssl_proxies, args=('country_name', combined_proxy))
geonode_thread = threading.Thread(target=collect_geonode_proxies, args=('country_code', 100, combined_proxy))

# Start the threads
ssl_thread.start()
geonode_thread.start()

# Wait for both threads to complete
ssl_thread.join()
geonode_thread.join()



# Now that we have collected proxies, start checking them
for proxy in combined_proxy:
    thread = threading.Thread(target=is_proxy_working, args=(proxy, lock, working_proxies, non_working_proxies))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print(f'Proxy list {len(combined_proxy)}')
print(f'Working Proxies {len(working_proxies)}')
print(f'Non-Working Proxies {len(non_working_proxies)}')
