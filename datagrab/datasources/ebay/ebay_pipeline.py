import time
from datagrab.datasources.ebay.pipeline_functions import pipeline_functs
from datagrab.database import database_ops
from datagrab import zeldr_log


def start_pipeline(delete_temp_files=True, send_mail=True, send_to_mongo=True, ebay_page_reach=35, listings_per_page=100, recursive_get=True):
    """
    This is where the pipeline functions are set off.

    (1) Get the list of phones along with the necessary filter data for each. Make ebay calls


    :param delete_temp_files: deletes the temporary files (email log) created from the pipeline run if set to true
    :param send_mail: sends the email log to the designated email if set to true
    :param send_to_mongo: sends the price data of each phone to the mongodb cluster
    :param ebay_page_reach: number of product pages the API should get per phone
    :param listings_per_page: number of listings per product page
    :param recursive_get: makes extra API calls to recoup the removal of removed/filtered listings during each API call
    """

    pipeline_start_time = time.perf_counter()

    # (1)
    zeldr_log.info('Retrieving phones from mongodb store')

    phones_metadata = database_ops.get_mongodb_phones()
    phones_objects = pipeline_functs.make_phone_objs(phones_metadata)
    #database_ops.update_postgres_phones(phones_objects)
    zeldr_log.info(f"{len(phones_metadata)} phones found in store with {len(phones_objects)} unique phone objects")

    phones = pipeline_functs.make_listing_containers(phones_objects)

    zeldr_log.info("Beginning eBay Calls")
    pipeline_functs.get_daily_data(phones, ebay_page_reach, listings_per_page)

    pipeline_stop_time = time.perf_counter()

    zeldr_log.info(f"Code ran in {pipeline_stop_time-pipeline_start_time} seconds")

    #(2)
    pipeline_functs.sort_daily_listings(phones)
    #(3)
