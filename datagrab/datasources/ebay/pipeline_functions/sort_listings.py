import datetime
from datagrab.datasources.ebay.pipeline_functions import listingprocessor
from datagrab.database import database_ops
import json
from dateutil import parser
from datagrab import temp_listings_location
from os import listdir
from os.path import isfile, join


'''def get_proccess_dates():
    with open('./processed_dates.json', 'r') as jfile:
        date_dict = json.load(jfile)
        return date_dict.get('last_dates_sorted')


def add_processed_dates(date):
    dates = get_proccess_dates()
    dates.append(date)
    with open('./processed_dates.json', 'w') as jfile:
        json.dump({'last_dates_sorted': dates}, jfile)'''


def get_oldlistings(file):
    listings = []
    with open(file, 'r') as jfile:
        store = json.load(jfile)

    for k, v in store.items():
        if k == 'store':
            for k1, v1, in store[k].items():
                for k2, v2 in store[k][k1].items():
                    for k3, v3 in store[k][k1][k2].items():
                        for k4, v4 in store[k][k1][k2][k3].items():
                            listings.extend(store[k][k1][k2][k3][k4]['listings'])
        else:
            listings.extend(v)
    return listings


def load_listing(file):
    with open(file, 'r') as jfile:
        listing_file = json.load(jfile)
        listings = listing_file['listings']
        return listings


def load_listings():  # slow function
    """
     loop through the listings json files in 'datagrab/datafiles/temp_files', get each file and the date on the file's
     name
    :return: a list of tuples holding a date string and the listings collected on that date [(date_str, [listings]), ()]
    """

    listings_by_date = []
    mypath = temp_listings_location
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files_parsed = 0
    for file in onlyfiles:
        date = parser.parse(file, fuzzy=True)
        # change logic
        #if date.strftime("%Y-%m-%d") not in processed_dates and files_parsed < 1:
        date_str = date.strftime("%Y-%m-%d")
        listings = load_listing(file=join(mypath, file))
        listings_by_date.append((date_str, listings))
        files_parsed += 1
    return listings_by_date


def run(ebay_phones):
    sorter = listingprocessor.ListingProcessor()
    sorter.load_phone_objs(ebay_phones)
    listings_by_date = load_listings()
    for listing_date in listings_by_date:
        print(f"sorting listings for {listing_date[0]}", end='\n')  # remove
        listings = sorter.clean_listings(listing_date[1], listing_date[0])

        database_ops.add_listings(listings)

        sorter.match_phone_listings(listings)
        for phone in ebay_phones:
            database_ops.add_phonelistings(phone.get_phone_listings())
            phone.clear_listings()
        sorter.load_phone_objs(ebay_phones)
