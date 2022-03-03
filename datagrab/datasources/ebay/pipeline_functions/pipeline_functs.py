from datagrab.domain_objects.smartphone import make_phones
from datagrab.datasources.ebay import eBay_priceAPI
from datagrab.domain_objects.phoneListings import EBayListing
from datagrab.datasources.ebay.pipeline_functions import sort_listings


def make_phone_objs(phones_data):
    """

    :param phones_data:
    :return:
    """
    return make_phones(phones_data)


def make_listing_containers(phone_objects):
    """

    :param phone_objects:
    :return:
    """
    container = []
    for phone in phone_objects:
        ebayphone = EBayListing(phone)
        container.append(ebayphone)

    return container


def build_requests_data(phones, api):
    search_list = [phone.get_search_data() for phone in phones]
    api.add_search_data(search_list)


def get_daily_data(phones, request_pages, listings_per_page):
    eBayAPI = eBay_priceAPI.eBayPriceAPI("eBay", page_reach=request_pages, listings_per_page=listings_per_page)
    build_requests_data(phones, eBayAPI)
    eBayAPI.execute_requests()
    eBayAPI.get_listings()
    eBayAPI.save_listings()


def sort_daily_listings(ebay_phones):
    sort_listings.run(ebay_phones)
