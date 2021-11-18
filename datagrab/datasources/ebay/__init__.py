import os
import yaml

ebay_config = os.path.join(os.path.dirname(__file__), 'datafiles/ebay_config.yaml')
ebay_metrics = os.path.join(os.path.dirname(__file__), 'datafiles/api_metrics.json')


with open(ebay_config) as file:
    config = yaml.load(file.read(), Loader=yaml.FullLoader)
    findingKey = config['svcs.ebay.com']['appid']