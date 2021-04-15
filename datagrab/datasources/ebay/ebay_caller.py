import os
from ebaysdk.exception import ConnectionError
from datagrab.datasources.ebay import ebay_config
from ebaysdk.finding import Connection as FindConnect


def get_connection():
    """

    :return: connection to the ebay finding api
    """
    try:
        api = FindConnect(config_file=ebay_config, siteid="EBAY-ENCA")

    except ConnectionError as e:
        print("ebay_caller.get_connection: Connection fault")
        print(f'\t{e}')
        print(f'\t{e.response.dict()}')
    except Exception as e:
        print(f'ebay_caller.get_connection: {e}')
    else:
        return api


def execute_call(request_dict, page_iter=1, verb='findItemsAdvanced', listings_expected=100, recursive_get=True):
    """

    :param request_dict: the dictionary of params sent to the eBay API to execute
    :param page_iter: the number of response pages to get
    :param verb: eBay finding API verb specification
    :param listings_expected: number of phone listings expected to return to the code calling this function
    :param recursive_get: boolean. chooses whether to make more calls after filtering out multi variation listings
    :return: list containing phone listings from ebay
    """
    phone_listings = []
    page_count = 0
    iter_count = 0

    api = get_connection()
    if api:
        while iter_count <= page_iter:
            resp = api.execute(verb, request_dict).dict()
            call_made()
            if resp['ack'] == 'Success':
                # check if the number of pages to request is more than available pages and correct it if needed
                actual_page_count = int(resp['paginationOutput']['totalPages'])
                if actual_page_count < page_iter:
                    page_iter = actual_page_count

                try:
                    phone_listings.extend(resp['searchResult']['item'])  # sometimes gives ('KeyError', ('item',))
                except KeyError as e:
                    print(f'ebay_caller.execute_call: {e}')
                except Exception as e:
                    print(f'ebay_caller.execute_call: {e}')

                iter_count += 1
                # go to next page of response
                request_dict['paginationInput']['pageNumber'] += 1
                page_count += 1

    #
    clean_listings = remove_multi_variations(phone_listings)
    listings_removed = len(phone_listings) - len(clean_listings)
    if len(clean_listings) < listings_expected and request_dict['paginationInput']['pageNumber'] < 40 and recursive_get:
        clean_listings.extend(execute_call(request_dict, page_iter=10, verb=verb, listings_expected=listings_removed))

    return clean_listings


def remove_multi_variations(temp_listings):
    """
    iterate through the listings returned by eBay and remove the multi variation listings
    :param temp_listings: list of eBay listings
    :return: non multi variation listings
    """
    clean_listings = []
    for listing in temp_listings:
        if listing["isMultiVariationListing"] == "false":
            clean_listings.append(listing)
    return clean_listings


def call_made():
    """
    reduces the daily number of eBay API finding calls allowed when called and then increments the calls_made in logs by 1
    :return:
    """
    metrics = json_handler.get_metrics()
    metrics['finding_api_calls_left'] -= 1
    json_handler.write_api_metrics(metrics)

    if os.path.exists(email_log):
        log = json_handler.get_email_log()
        log['calls_made'] += 1
        json_handler.write_email_log(log)


def reset_daily_call_limit():
    """
    resets the eBay API finding call limits each day whe called
    :return:None
    """
    ebay_metrics = dict()
    ebay_metrics['finding_api_call_limit'] = 5000
    ebay_metrics['finding_api_calls_left'] = 5000

    json_handler.write_api_metrics(ebay_metrics)
