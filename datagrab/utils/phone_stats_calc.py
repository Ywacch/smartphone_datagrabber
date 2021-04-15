import datetime
import statistics
from datagrab.utils import file_read_write
from datagrab.utils.file_read_write import get_temp_listings


def calculate_phone_price_stats(phone):
    """

    :param phone:
    :return:
    """
    listings_store = get_temp_listings()
    for silo in phone.iterate_silos():
        listings = \
            listings_store['store'][silo.search_data['brand']][silo.search_data['series']][silo.search_data['model']][
                silo.search_data['specs']]['listings']

        # no point in calculating statistics if sample size is 0
        if len(listings) > 0:
            prices = []
            lowest_listing = listings[0]
            highest_listing = listings[0]
            for current_listing in listings:
                if float(current_listing['sellingStatus']['convertedCurrentPrice']['value']) >= float(highest_listing['sellingStatus']['convertedCurrentPrice']['value']):
                    highest_listing = current_listing
                if float(current_listing['sellingStatus']['convertedCurrentPrice']['value']) <= float(lowest_listing['sellingStatus']['convertedCurrentPrice']['value']):
                    lowest_listing = current_listing
                prices.append(float(current_listing['sellingStatus']['convertedCurrentPrice']['value']))

            stat_metrics = dict()

            date_time_now = datetime.datetime.now().isoformat()
            stat_metrics['date'] = date_time_now
            file_read_write.set_time(date_time_now)

            try:
                stat_metrics['mean'] = statistics.mean(prices)
                stat_metrics['median'] = statistics.median(prices)
                stat_metrics['popular_price'] = statistics.mode(prices)
                try:
                    stat_metrics['std_dev'] = statistics.stdev(prices)
                except Exception as e:
                    pass  # log
                stat_metrics['low'] = min(prices)
                stat_metrics['high'] = max(prices)
            except Exception as e:
                print(e)
                pass  # log
                print()
            else:
                file_read_write.set_highest_listing(silo, highest_listing)
                file_read_write.set_lowest_listing(silo, lowest_listing)
                file_read_write.set_lowest_price(silo, stat_metrics['low'])
                file_read_write.set_highest_price(silo, stat_metrics['high'])
                silo.input_stats(stat_metrics)
