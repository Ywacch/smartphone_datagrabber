import decimal
from dateutil import parser
import json


class Listing:

    @staticmethod
    def get_itemid(listing):
        try:
            return listing['itemId'][0]
        except KeyError:
            return None

    @staticmethod
    def get_title(listing):
        try:
            return listing['title'][0]
        except KeyError:
            return None

    @staticmethod
    def get_globalid(listing):
        try:
            return listing['globalId'][0]
        except KeyError:
            return None

    @staticmethod
    def get_productid(listing):
        try:
            return listing['productId'][0]['__value__']
        except KeyError:
            return None

    @staticmethod
    def get_postalcode(listing):
        try:
            return listing['postalCode'][0]
        except KeyError:
            return None

    @staticmethod
    def get_location(listing):
        try:
            return listing['location'][0]
        except KeyError:
            return None

    @staticmethod
    def get_country(listing):
        try:
            return listing['country'][0]
        except KeyError:
            return None

    @staticmethod
    def get_currency(listing):
        try:
            return listing['sellingStatus'][0]['currentPrice'][0]['@currencyId']
        except KeyError:
            return None

    @staticmethod
    def get_price(listing):
        try:
            price = listing['sellingStatus'][0]['currentPrice'][0]['__value__']
        except KeyError:
            return None
        else:
            return decimal.Decimal(price)

    @staticmethod
    def get_condition(listing):
        try:
            return listing['condition'][0]['conditionDisplayName'][0]
        except KeyError:
            return None

    @staticmethod
    def get_shippingtype(listing):
        try:
            return listing['shippingInfo'][0]['shippingType'][0]
        except KeyError:
            return None

    @staticmethod
    def get_shippingcurrency(listing):
        try:
            return listing['shippingInfo'][0]['shippingServiceCost'][0]['@currencyId']
        except KeyError:
            return None

    @staticmethod
    def get_shippingcost(listing):
        try:
            cost = listing['shippingInfo'][0]['shippingServiceCost'][0]['__value__']
        except KeyError:
            return None
        else:
            return decimal.Decimal(cost)

    @staticmethod
    def get_toprated(listing):
        try:
            is_toprated = listing['topRatedListing'][0]
        except KeyError:
            return None
        else:
            return json.loads(is_toprated.lower())

    @staticmethod
    def get_startdate(listing):
        try:
            date = listing['listingInfo'][0]['startTime'][0]
        except KeyError:
            return None
        else:
            return parser.parse(date).strftime("%Y-%m-%d")


    @staticmethod
    def get_enddate(listing):
        try:
            date = listing['listingInfo'][0]['endTime'][0]
        except KeyError:
            return None
        else:
            return parser.parse(date).strftime("%Y-%m-%d")

    @staticmethod
    def get_listingtype(listing):
        try:
            return listing['listingInfo'][0]['listingType'][0]
        except KeyError:
            return None


'''class Listing:

    @staticmethod
    def get_itemid(listing):
        try:
            return listing['itemId']
        except KeyError:
            return None

    @staticmethod
    def get_title(listing):
        try:
            return listing['title']
        except KeyError:
            return None

    @staticmethod
    def get_globalid(listing):
        try:
            return listing['globalId']
        except KeyError:
            return None

    @staticmethod
    def get_productid(listing):
        try:
            return listing['productId']['value']
        except KeyError:
            return None

    @staticmethod
    def get_postalcode(listing):
        try:
            return listing['postalCode']
        except KeyError:
            return None

    @staticmethod
    def get_location(listing):
        try:
            return listing['location']
        except KeyError:
            return None

    @staticmethod
    def get_country(listing):
        try:
            return listing['country']
        except KeyError:
            return None

    @staticmethod
    def get_currency(listing):
        try:
            return listing['sellingStatus']['currentPrice']['_currencyId']
        except KeyError:
            return None

    @staticmethod
    def get_price(listing):

        try:
            price = listing['sellingStatus']['currentPrice']['value']
        except KeyError:
            return None
        else:
            return decimal.Decimal(price)

    @staticmethod
    def get_condition(listing):
        try:
            return listing['condition']['conditionDisplayName']
        except KeyError:
            return None

    @staticmethod
    def get_shippingtype(listing):
        try:
            return listing['shippingInfo']['shippingType']
        except KeyError:
            return None

    @staticmethod
    def get_shippingcurrency(listing):
        try:
            return listing['shippingInfo']['shippingServiceCost']['_currencyId']
        except KeyError:
            return None

    @staticmethod
    def get_shippingcost(listing):
        try:
            cost = listing['shippingInfo']['shippingServiceCost']['value']
        except KeyError:
            return None
        else:
            return decimal.Decimal(cost)

    @staticmethod
    def get_toprated(listing):
        try:
            is_toprated = listing['topRatedListing']
        except KeyError:
            return None
        else:
            return json.loads(is_toprated.lower())

    @staticmethod
    def get_startdate(listing):
        try:
            date = listing['listingInfo']['startTime']
        except KeyError:
            return None
        else:
            return parser.parse(date).strftime("%Y-%m-%d")

    @staticmethod
    def get_enddate(listing):
        try:
            date = listing['listingInfo']['endTime']
        except KeyError:
            return None
        else:
            return parser.parse(date).strftime("%Y-%m-%d")

    @staticmethod
    def get_listingtype(listing):
        try:
            return listing['listingInfo']['listingType']
        except KeyError:
            return None'''