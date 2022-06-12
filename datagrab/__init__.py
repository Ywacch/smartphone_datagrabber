import os
import datetime
import logging
from logging import Logger


mydate = datetime.datetime.now()
date_str = mydate.strftime("%B-%d-%Y").lower()

eBay_API_metrics = os.path.join(os.path.dirname(__file__), f'datafiles/ebay/ebay_api_metrics.json')
temp_listings_store = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/temp_listings-{date_str}.json')
temp_listings_location = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/')
email_config = os.path.join(os.path.dirname(__file__), f'datafiles/email_config.yaml')

datagrab_log = logging.getLogger('datagrab')
email_log = logging.getLogger('smartphones')


def setup_logger(logger:Logger, log_name):
    f_handler = logging.FileHandler(f'{log_name}-{date_str}.log')
    f_handler.setLevel(logging.DEBUG)

    f_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)  # duplication


setup_logger(datagrab_log, "datagrab")
setup_logger(email_log, "smartphones")
