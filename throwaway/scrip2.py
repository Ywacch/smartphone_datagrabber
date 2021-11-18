import yaml
from datagrab.datasources.ebay import ebay_config

with open(ebay_config) as file:
    config = yaml.load(file.read(), Loader=yaml.FullLoader)
    print(config['svcs.ebay.com']['appid'])

