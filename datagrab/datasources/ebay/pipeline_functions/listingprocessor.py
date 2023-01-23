from queue import PriorityQueue
from datagrab.datasources.ebay.match_filters import matchlistings
from datagrab.domain_objects.listing import Listing, fx_rates
from datagrab.database import database_ops
from datagrab import datagrab_log

try:
    database_ops.add_exchange_rate(fx_rates)
except Exception as e:
    datagrab_log.error(e)


def remove_duplicates(listings):
    """
    Removes duplicate listings
    :param listings: a list of dictionaries representing eBay listings
    :return: unique list of eBay listings based on itemId
    """
    return list({listing['itemId'][0]: listing for listing in listings}.values())


class ListingProcessor:

    def __init__(self):
        self.phone_match_queue = PriorityQueue()

    def load_phone_objs(self, phones):
        for phone in phones:
            self.phone_match_queue.put((phone.priority, phone))

    def clean_listings(self, listings, date_collected):
        """
        Removes duplicate listings and unnecessary key-values
        :param date_collected: date on which the listing was requested
        :param listings: a list of dictionaries representing eBay listings
        :return: unique list of eBay listings based on itemId
        """
        unique_listings = remove_duplicates(listings)
        filtered_listings = [{
            'item_id': Listing.get_itemid(listing),
            'title': Listing.get_title(listing),
            'global_id': Listing.get_globalid(listing),
            'product_id': Listing.get_productid(listing),
            'postal_code': Listing.get_postalcode(listing),
            'location_': Listing.get_location(listing),
            'country': Listing.get_country(listing),
            'currency': Listing.get_currency(listing),
            'price': Listing.get_price(listing),
            'condition_': Listing.get_condition(listing),
            'shipping_type': Listing.get_shippingtype(listing),
            'shipping_currency': Listing.get_shippingcurrency(listing),
            'shipping_cost': Listing.get_shippingcost(listing),
            'top_rated': Listing.get_toprated(listing),
            'start_date': Listing.get_startdate(listing),
            'end_date': Listing.get_enddate(listing),
            'listing_type': Listing.get_listingtype(listing),
            'date_added': date_collected,
            'canadian_price_base': Listing.get_cad_base(listing)

        } for listing in unique_listings]
        return filtered_listings

    def match_phone_listings(self, listings):
        while not self.phone_match_queue.empty():
            phone = self.phone_match_queue.get()[1]
            for listing in listings:
                if matchlistings.match_phone_listing(phone.get_match_data(), listing['title']):
                    phone.add_listing(listings.pop(listings.index(listing)))
