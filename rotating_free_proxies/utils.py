from __future__ import absolute_import

import logging

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy


logger = logging.getLogger(__name__)


def extract_proxy_hostport(proxy):
    """
    Return the hostport component from a given proxy:

    >>> extract_proxy_hostport('example.com')
    'example.com'
    >>> extract_proxy_hostport('http://www.example.com')
    'www.example.com'
    >>> extract_proxy_hostport('127.0.0.1:8000')
    '127.0.0.1:8000'
    >>> extract_proxy_hostport('127.0.0.1')
    '127.0.0.1'
    >>> extract_proxy_hostport('localhost')
    'localhost'
    >>> extract_proxy_hostport('zot:4321')
    'zot:4321'
    >>> extract_proxy_hostport('http://foo:bar@baz:1234')
    'baz:1234'
    """
    return _parse_proxy(proxy)[3]


def fetch_new_proxies(proxy_path, max_number_of_proxies):
    logger.warning(f"Fetching new proxies; dumping location = {proxy_path}")
    from selenium import webdriver

    # def get_soup(url):
    # return BeautifulSoup(requests.get(url).text)

    driver = webdriver.Firefox()

    # soup = get_soup("https://free-proxy-list.net/")
    # trs = soup.find_all("tr")

    proxies_set = set()

    not_enough_proxies = False
    last_num_proxies = 0
    while len(proxies_set) < max_number_of_proxies and not not_enough_proxies:
        proxies_set |= set(fetch_proxies_from_66pm(driver=driver))
        if len(proxies_set) == last_num_proxies:
            not_enough_proxies = True
            logger.warning(f'We can only get {len(proxies_set)} proxies.')
        last_num_proxies = len(proxies_set)
    driver.close()

    # for tr in trs:
    #     tds = tr.find_all("td")
    #     if tds:
    #         ip = tds[0].text
    #         if not validate_ip(ip):
    #             continue
    #         port = tds[1].text
    #         if not validate_port(port):
    #             continue
    #         if "elite" not in tds[4].text:
    #             continue
    #         if "minutes" in tds[-1].text:
    #             continue
    #         protocol = "https" if "yes" in tds[6].text.strip() else "http"
    #         proxy = f"{protocol}://{ip}:{port}"
    #         proxies.append(proxy)
    #         if len(proxies) > max_number_of_proxies:
    #             break

    proxies = list(proxies_set)[:max_number_of_proxies]

    with open(proxy_path, "w") as f:
        logger.warning(
            f"updating list of proxies ({len(proxies)}) to location {proxy_path}"
        )
        f.write("\n".join(proxies) + "\n")
    return proxies


def fetch_proxies_from_66pm(driver):
    import re
    import socket

    from bs4 import BeautifulSoup

    # get 300 http proxies each time 
    url_66_http = 'http://www.66ip.cn/mo.php?sxb=&tqsl=300&port=&export=&ktip=&sxa='
    driver.get(url=url_66_http)

    soup = BeautifulSoup(driver.page_source, features='lxml')
    r = re.compile('([0-9.:]+?)\n')
    trs = r.findall(soup.text)

    def validate_ip(addr):
        try:
            socket.inet_aton(addr)
            return True
        except socket.error:
            return False

    def validate_port(port):
        return str(port).isdigit() and 1000 < int(port) < 99999

    proxies = list()

    logger.warning(f"Total proxies listed in source webpage={len(trs)}")

    for tr in trs:
        ip, port = tr.split(':')
        if not validate_ip(ip):
            continue
        if not validate_port(port):
            continue
        proxy = f'{ip}:{port}'
        proxies.append(proxy)

    return proxies
