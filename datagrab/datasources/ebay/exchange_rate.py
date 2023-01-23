import requests
import decimal
from dateutil import parser
from datagrab import datagrab_log

def get_fxrates():

    currencies = ['FXAUDCAD', 'FXEURCAD', 'FXGBPCAD', 'FXUSDCAD']

    endpoint = f"https://www.bankofcanada.ca/valet/observations/{','.join(currencies)}/json?recent=1"

    try:
        response = requests.get(endpoint)
    except Exception as e:
        datagrab_log.error(e)
    else:
        if response.status_code == 200:
            data = response.json()
            fx_dict = {}
            for observation in data["observations"]:
                for key, value in observation.items():
                    if key != "d":
                        fx_dict[key] = decimal.Decimal(value["v"])
            fx_dict['date'] = parser.parse(data['observations'][0]['d']).strftime("%Y-%m-%d")
            return fx_dict
