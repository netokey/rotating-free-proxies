scrapy-rotating-free-proxies
=======================
This is forked from this_

.. _this: https://pypi.python.org/pypi/scrapy-rotating-free-proxies with very minor changes.

You don't need to specify any proxy list anywhere. This library automatically fetches freely available lists from here_

.. _here: https://free-proxy-list.net/

Installation
------------

    pip install scrapy-rotating-free-proxies

Usage
-----

Add the following two variables in settings.py of scrapy project

1.
   ROTATING_PROXY_LIST_PATH = '/my/path/proxies.txt'


2.

    DOWNLOADER_MIDDLEWARES = {
        # ...
        'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        # ...
    }


For further details on using this library, refer to the original repo's _readme file.

.. _readme: https://github.com/TeamHG-Memex/scrapy-rotating-proxies/blob/master/README.rst

