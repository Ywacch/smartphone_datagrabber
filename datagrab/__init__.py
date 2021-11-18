import os
import datetime
import logging

mydate = datetime.datetime.now()
date_str = mydate.strftime("%B-%d-%Y").lower()

eBay_API_metrics = os.path.join(os.path.dirname(__file__), f'datasources/ebay/datafiles/api_metrics.json')
email_log = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/email_log-{date_str}.json')
temp_listings_store = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/temp_listings-{date_str}.json')

zeldr_log = logging.getLogger('zeldr')

# log handler
f_handler = logging.FileHandler(f'zeldr-{date_str}.log')
f_handler.setLevel(logging.DEBUG)

# log format
f_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
f_handler.setFormatter(f_format)
zeldr_log.addHandler(f_handler)
zeldr_log.setLevel(logging.DEBUG)
