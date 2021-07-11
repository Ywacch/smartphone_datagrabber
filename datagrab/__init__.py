import os
import datetime

mydate = datetime.datetime.now()
date_str = mydate.strftime("%B-%d-%Y").lower()

eBay_API_metrics = os.path.join(os.path.dirname(__file__), f'datasources/ebay/datafiles/api_metrics.json')
email_log = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/email_log-{date_str}.json')
temp_listings_store = os.path.join(os.path.dirname(__file__), f'datafiles/temp_files/temp_listings-{date_str}.json')
