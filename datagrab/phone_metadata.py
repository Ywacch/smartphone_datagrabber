from datagrab.datasources.ebay.ebay_caller import execute_call
from datagrab.utils.file_read_write import get_temp_listings, write_listings


class Phone:

    def __init__(self, phone_dict, search_length=35, page_size=100, recursive_get=True):
        """

        :param phone_dict:
        :param search_length:
        :param page_size:
        """
        self.id = phone_dict.get('_id')
        self.brand = phone_dict.get('brand')
        self.series = phone_dict.get('series')
        self.model = phone_dict.get('model')
        self.search_strs = phone_dict.get('search_strs')
        self.priority = phone_dict.get('priority')
        self.storages = []
        self.silos = {}
        for storage in phone_dict.get('specs').get('storage'):
            alternative_storages = []
            for alt_storage in phone_dict.get('specs').get('storage'):
                if alt_storage != storage:
                    alternative_storages.append(alt_storage)
            self.storages.append(storage)
            self.silos[f'{storage}'] = PhoneSilo(self.brand, self.series, self.model, storage, self.search_strs, alternative_storages , search_length, page_size, recursive_get)

    def iterate_silos(self):
        """

        :return: Silo values/objects in the dictionary of silos
        """
        return self.silos.values()

    def send_listings_to_tray(self):
        """

        :return:
        """
        for silo in self.silos.values():
            silo.generate_report_to_json()

    def get_daily_data(self):
        """

        :return:
        """
        for silo in self.silos.values():
            silo.make_eBay_call()

    def process_filtered_listings(self):
        for silo in self.silos.values():
            silo.send_filtered_listings()

    def get_search_data(self):
        """

        :return:
        """
        return_silos = []
        for silo in self.silos.values():
            return_silos.append(silo.search_data)
        return return_silos

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class PhoneSilo:
    """

    """
    def __init__(self, brand, series, model, storage,  search_strs, alternative_specs, search_length, page_size, recursive_get=True):
        """

        :param brand:
        :param series:
        :param model:
        :param storage:
        :param search_strs:
        :param alternative_specs:
        :param search_length:
        :param page_size:
        :param recursive_get:
        """
        self.search_data = dict()
        self.search_data['brand'] = brand
        self.search_data['series'] = series
        self.search_data['model'] = model
        self.search_data['specs'] = storage
        self.search_data['alt_specs'] = alternative_specs
        self.search_data['search_strs'] = search_strs
        self.stat_metrics = dict()
        self.sample_size = None
        self.lowest_price = None
        self.highest_price = None

        self.search_page_length = search_length
        self.listings_per_page = page_size

        self.eBay_listings = []
        self.dataget_recursive = recursive_get

    # TODO: Ebay calls should be made from ebay module directly
    def make_eBay_call(self):
        """

        :return:
        """
        request = {
            'keywords': f'{self.search_data["search_strs"][0]}',
            'itemFilter': [
                {'name': 'Condition', 'value': 'Used'},
                {'name': 'currency', 'value': 'CAD'},
                # {'name': 'minPrice', 'value': 100.0}
            ],
            'aspectFilter': [
                {
                    'aspectName': 'Storage Capacity',
                    'aspectValueName': self.spec_size_str()
                }
            ],
            'categoryId': 9355,
            'paginationInput': {
                'entriesPerPage': self.listings_per_page,
                'pageNumber': 1
            },
            'sortOrder': 'BestMatch'
        }
        # access to findCompletedItems is restricted and deprecated to the public
        verbs = ['findItemsAdvanced', 'findCompletedItems', 'findItemsByKeywords']
        page_reach = self.search_page_length
        listings = execute_call(request_dict=request, page_iter=page_reach, verb=verbs[0], listings_expected= request['paginationInput']['entriesPerPage'] * page_reach, recursive_get=self.dataget_recursive)
        self.eBay_listings.extend(listings)

    def generate_report_to_json(self):
        """

        :return:
        """
        phone_store = get_temp_listings()
        phone_store['listing_tray'].extend(self.eBay_listings)
        write_listings(phone_store)
        self.eBay_listings.clear()

    def send_filtered_listings(self):
        """

        :return:
        """
        phone_store = get_temp_listings()
        phone_store['store'][self.search_data['brand']][self.search_data['series']][self.search_data['model']][self.search_data['specs']]['listings'].extend(self.eBay_listings)
        write_listings(phone_store)
        self.eBay_listings.clear()

    def spec_size_str(self):
        """

        :return:
        """
        storage = self.search_data['specs'].lower().split()
        storage_str = ''
        if 'gb' in storage:
            storage_str = f'{storage[0]} GB'
        elif 'tb' in storage:
            storage_str = f'{storage[0]} TB'
        return storage_str

    def input_stats(self, metrics):
        """

        :param metrics:
        :return:
        """
        self.stat_metrics = metrics

    def get_alts(self):
        """

        :return:
        """
        return self.search_data['alt_specs']

    def __str__(self):
        return f'{self.search_data["search_strs"][0]} {self.search_data["specs"]}'

    def __repr__(self):
        return str(self)
