import json
from datagrab import eBay_API_metrics
from datagrab import datagrab_log


def write_json(data, file, indent_len=2):
    """

    :param data:
    :param indent_len:
    :return:
    """
    with open(file, 'w') as jfile:
        json.dump(data, jfile, indent=indent_len)


def get_json(file):
    """

    :return:
    """
    try:
        with open(file, 'r') as jfile:
            return json.load(jfile)
    except FileNotFoundError:
        datagrab_log.exception(f'{file}" can\'t be found')
    except Exception as e:
        datagrab_log.exception(f'{e}')


def call_made(calls_made):
    """
    reduces the daily number of eBay API finding calls allowed when called and then increments the calls_made in logs by 1
    :return:
    """
    metrics = get_json(eBay_API_metrics)
    metrics['finding_api_calls_left'] -= calls_made

    write_json(metrics, eBay_API_metrics)


def reset_daily_call_limit():
    """
    resets the eBay API finding call limits each day whe called
    :return:None
    """
    ebay_metrics = dict()
    ebay_metrics['finding_api_call_limit'] = 5000
    ebay_metrics['finding_api_calls_left'] = 5000

    write_json(ebay_metrics, eBay_API_metrics)

