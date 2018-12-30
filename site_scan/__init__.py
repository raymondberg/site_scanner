import requests
from selenium import webdriver

class SiteScanner:
    HTTPS_PORTS = [443, 8443, 9443]
    def __init__(self, config):
        self.config = config
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def __del__(self):
        self.driver.quit()

    def scan(self):
      for host in self.config.hosts:
          for port in self.config.ports:
                url = '{}://{}:{}'.format(
                        'https' if port in self.HTTPS_PORTS else 'http' ,
                        host,
                        port,
                       )
                print('Scanning {}'.format(url))
                result = self._request(url)
                self._screenshot(url)

    def _screenshot(self, url):
        self.driver.get(url)
        safe_name = url.replace('/', '_').replace(':', '__')
        screenshot = self.driver.save_screenshot('{}.png'.format(safe_name))

    def _request(self, url):
       result = requests.get(url, verify=False)
       return result


class ScanConfig:
    def __init__(self):
        self.hosts = []
        self.ports = []

    def add_text_hosts(self, host_string):
        self.hosts += host_string.split(',')

    def add_text_ports(self, port_string):
        self.ports += [int(p) for p in port_string.split(',')]

