import json
import os
from datagrab import email_log, temp_listings_store, eBay_API_metrics


def make_json_nested_store(phones):
    """
    creates a temporary json store for holding phone listings and sorting them by brand->seres->models->storage.
    Along with a tray(list) to temporarily hold listings

    :param phones: a list of phones in the mongo database
    :return: None. Converts the phone_dict to a json
    """

    # get all unique brands
    brands = set(phone['brand'] for phone in phones)

    phones_dict = dict()

    phones_dict['store'] = dict()

    for key in phones_dict.keys():
        for brand in brands:
            phones_dict[key][brand] = dict()
            series = set()

            # sorting by series
            for phone in phones:
                if phone['brand'] == brand:
                    phones_dict[key][brand][phone['series']] = dict()
                    series.add(phone['series'])

            # sorting by model and adding each spec
            for serie in series:
                for phone in phones:
                    if phone['series'] == serie:
                        phones_dict[key][brand][serie][phone['model']] = dict()
                        for spec in phone['specs']['storage']:
                            phones_dict[key][brand][serie][phone['model']][spec] = dict()
                            phones_dict[key][brand][serie][phone['model']][spec]['listings'] = list()

    phones_dict['listing_tray'] = list()

    write_listings(phones_dict)


def make_log_email_file(phones):
    """

    :param phones:
    :return:
    """
    # get all unique brands
    brands = set(phone['brand'] for phone in phones)

    metrics_dict = dict()

    metrics_dict['calls_made'] = 0
    metrics_dict['runtime'] = 0
    metrics_dict['discarded_listings'] = None
    metrics_dict['time'] = 0
    metrics_dict['store'] = dict()
    metrics_dict['distinct_phones'] = 0

    for brand in brands:
        metrics_dict['store'][brand] = dict()
        series = set()

        # sorting by series
        for phone in phones:
            if phone['brand'] == brand:
                metrics_dict['store'][brand][phone['series']] = dict()
                series.add(phone['series'])

        # sorting by model and adding each spec
        for serie in series:
            for phone in phones:
                if phone['series'] == serie:
                    metrics_dict['store'][brand][serie][phone['model']] = dict()
                    for spec in phone['specs']['storage']:
                        metrics_dict['distinct_phones'] += 1
                        metrics_dict['store'][brand][serie][phone['model']][spec] = dict()
                        metrics_dict['store'][brand][serie][phone['model']][spec]['sample_size'] = 0
                        metrics_dict['store'][brand][serie][phone['model']][spec]['highest_price'] = None
                        metrics_dict['store'][brand][serie][phone['model']][spec]['highest_listing'] = None
                        metrics_dict['store'][brand][serie][phone['model']][spec]['lowest_price'] = None
                        metrics_dict['store'][brand][serie][phone['model']][spec]['lowest_listing'] = None

    write_email_log(metrics_dict)


def delete_temp_files():
    """

    :return:
    """
    # os.remove(temp_listings_store)
    os.remove(email_log)


def set_sample_size(silo, value):
    """

    :param silo:
    :param value:
    :return:
    """
    log = get_email_log()
    log['store'][silo.search_data['brand']][silo.search_data['series']][
                    silo.search_data['model']][
                    silo.search_data['specs']]['sample_size'] = value
    write_email_log(log)


def set_highest_listing(silo, value):
    """

    :param silo:
    :param value:
    :return:
    """
    log = get_email_log()
    log['store'][silo.search_data['brand']][silo.search_data['series']][
        silo.search_data['model']][
        silo.search_data['specs']]['highest_listing'] = value
    write_email_log(log)


def set_lowest_listing(silo, value):
    """

    :param silo:
    :param value:
    :return:
    """
    log = get_email_log()
    log['store'][silo.search_data['brand']][silo.search_data['series']][
        silo.search_data['model']][
        silo.search_data['specs']]['lowest_listing'] = value
    write_email_log(log)


def set_highest_price(silo, value):
    """

    :param silo:
    :param value:
    :return:
    """
    log = get_email_log()
    log['store'][silo.search_data['brand']][silo.search_data['series']][
        silo.search_data['model']][
        silo.search_data['specs']]['highest_price'] = value
    write_email_log(log)


def set_lowest_price(silo, value):
    """

    :param silo:
    :param value:
    :return:
    """
    log = get_email_log()
    log['store'][silo.search_data['brand']][silo.search_data['series']][
        silo.search_data['model']][
        silo.search_data['specs']]['lowest_price'] = value
    write_email_log(log)


def set_discarded_listings(value):
    """

    :param value:
    :return:
    """
    log = get_email_log()
    log['discarded_listings'] = value
    write_email_log(log)


def set_runtime(value):
    """

    :param value:
    :return:
    """
    log = get_email_log()
    log['runtime'] = value
    write_email_log(log)


def set_time(value):
    """

    :param value:
    :return:
    """
    log = get_email_log()
    log['time'] = value
    write_email_log(log)


def write_listings(data, indent_len=2):
    """

    :param data:
    :param indent_len:
    :return:
    """
    with open(temp_listings_store, 'w') as file:
        json.dump(data, file, indent=indent_len)


def write_api_metrics(data, indent_len=2):
    """

    :param data:
    :param indent_len:
    :return:
    """
    with open(eBay_API_metrics, 'w') as file:
        json.dump(data, file, indent=indent_len)


def get_temp_listings():
    """

    :return:
    """
    with open(temp_listings_store, 'r') as file:
        return json.load(file)


def get_metrics():
    """

    :return:
    """
    with open(eBay_API_metrics, 'r') as file:
        return json.load(file)


def write_email_log(data, indent_len=2):
    """

    :param data:
    :param indent_len:
    :return:
    """
    with open(email_log, 'w') as file:
        json.dump(data, file, indent=indent_len)


def get_email_log():
    """

    :return:
    """
    try:
        with open(email_log, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'the file "{email_log}" can\'t be found')