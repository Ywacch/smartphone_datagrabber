import time
from queue import PriorityQueue

from datagrab.phone_metadata import Phone
from datagrab.datasources.ebay import ebay_caller
from datagrab.database import mongo_reads, mongo_writes
from datagrab.utils import file_read_write, emailer, phone_stats_calc
from datagrab.utils.file_read_write import write_listings, get_temp_listings
from datagrab.datasources.phones_listongs_matcher import match_phone_listing


def call(phone_items, search_length, page_size, recursive_get=True):
    """

    :param phone_items:
    :param search_length:
    :param page_size:
    :param recursive_get:
    :return:
    """
    phones = []
    for phone_item in phone_items:
        phone = Phone(phone_item, search_length=search_length, page_size=page_size, recursive_get=recursive_get)
        phones.append(phone)
        phone.get_daily_data()
        phone.send_listings_to_tray()
    return phones


def filter_duplicates():
    """

    :return:
    """
    listings_store = get_temp_listings()
    tray_listings = listings_store['listing_tray']

    filtered_list = []
    duplicate_count = 0

    for listing1 in tray_listings:
        if listing1 not in filtered_list:
            filtered_list.append(listing1)
        else:
            duplicate_count += 1

    tray_listings.clear()
    tray_listings.extend(filtered_list)

    file_read_write.set_discarded_listings(duplicate_count)
    write_listings(listings_store)


def priority_sort(phones):
    """

    :param phones:
    :return:
    """
    priority_dict = {'priority_one': [], 'priority_two': [], 'priority_three': []}
    phone_queue = PriorityQueue()

    # 1
    for phone in phones:
        if phone.priority == 1:
            priority_dict['priority_one'].append(phone)
        if phone.priority == 2:
            priority_dict['priority_two'].append(phone)
        if phone.priority == 3:
            priority_dict['priority_three'].append(phone)

    phone_queue.put((1, priority_dict['priority_one']))
    phone_queue.put((2, priority_dict['priority_two']))
    phone_queue.put((3, priority_dict['priority_three']))

    listings_store = get_temp_listings()
    tray_listings = listings_store['listing_tray']

    # 2
    while not phone_queue.empty():
        for phone in phone_queue.get()[1]:  # get each priority list
            for silo in phone.iterate_silos():
                for listing in tray_listings:
                    if match_phone_listing(silo.search_data, listing):
                        silo.eBay_listings.append(tray_listings.pop(tray_listings.index(listing)))
                        file_read_write.set_sample_size(silo, len(silo.eBay_listings))

    listings_store['listing_tray'] = tray_listings
    write_listings(listings_store)


def jsonify_listings(phones):
    """

    :param phones:
    :return:
    """
    for phone in phones:
        phone.process_filtered_listings()


def start_pipeline(delete_temp_files=True, send_mail=True, send_to_mongo=True, ebay_page_reach=35, listings_per_page=100, recursive_get=True):
    """
    This is where the pipeline functions are set off.

    (1) Get the list of phones along with the necessary filter data for each

    (2) create files to hold data. Email file to send as an email log and a temp file to hold listings data sorted by phone

    (3) 4 main steps of the ebay data pipeline:
        call - where the calls to the ebay API are made
        filter_duplicates - iterates through the list of phone listing dictionaries and filters out the duplicates
        priority_sort - match listings accurately to their phone specifications
        jsonify_listings -

    (4)


    :param delete_temp_files: deletes the temporary files (email log) created from the pipeline run if set to true
    :param send_mail: sends the email log to the designated email if set to true
    :param send_to_mongo: sends the price data of each phone to the mongodb cluster
    :param ebay_page_reach: number of product pages the API should get per phone
    :param listings_per_page: number of listings per product page
    :param recursive_get: makes extra API calls to recoup the removal of removed/filtered listings during each API call
    """

    pipeline_start_time = time.time()

    # reset the call limit number before making new eBay api calls
    ebay_caller.reset_daily_call_limit()

    # (1)
    phones_metadata = mongo_reads.get_phones_data()

    if phones_metadata:
        # (2)
        file_read_write.make_json_nested_store(phones_metadata)
        file_read_write.make_log_email_file(phones_metadata)

        # (3)
        print("Beginning ebay calls")
        ebay_call_start = time.time()
        phones = call(phones_metadata, ebay_page_reach, listings_per_page, recursive_get)
        ebay_call_stop = time.time()
        print(f'eBay calls duration: {ebay_call_stop-ebay_call_start}', end='\n\n')

        print("Beginning duplicate filter")
        duplicate_filter_start = time.time()
        filter_duplicates()
        duplicate_filter_stop = time.time()
        print(f'duplicate listing filter duration: {duplicate_filter_stop-duplicate_filter_start}', end='\n\n')

        print("Beginning priority sort")
        sort_start = time.time()
        priority_sort(phones)
        sort_stop = time.time()
        print(f'listings sort duration {sort_stop-sort_start}', end='\n\n')

        print("Beginning Jsonify")
        jsonify_start = time.time()
        jsonify_listings(phones)
        jsonify_stop = time.time()
        print(f'jsonify duration: {jsonify_stop-jsonify_start}', end='\n\n')

        # (4)
        for phone in phones:
            phone_stats_calc.calculate_phone_price_stats(phone)

        # (5)
        if send_to_mongo:
            mongo_writes.prep_mongo_store(phones)
            mongo_writes.save_stats_db(phones)

    pipeline_stop_time = time.time()

    file_read_write.set_runtime(pipeline_stop_time - pipeline_start_time)

    # (6)
    if send_mail:
        try:
            emailer.send_mail()
        except Exception as e:
            print("Email error has occurred")
            print(e, end='\n\n')

    # (7)
    if delete_temp_files:
        file_read_write.delete_temp_files()
