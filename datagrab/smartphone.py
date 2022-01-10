from dataclasses import dataclass
from bson.objectid import ObjectId
from typing import List


@dataclass
class PhoneSpecs:
    """

    """
    brand: str
    series: str
    model: str
    search_strs: List[str]
    storage_size: str
    other_sizes: List[str]

    def get_search_str(self):
        return self.search_strs[0]

    def get_search_strs(self):
        return self.search_strs

    def get_other_sizes(self):
        return self.other_sizes

    def get_storagesize(self):
        storage = self.storage_size.split()
        storage_str = ''
        if 'gb' in storage:
            storage_str = f'{storage[0]} GB'
        elif 'tb' in storage:
            storage_str = f'{storage[0]} TB'
        return storage_str


@dataclass
class Phone:
    """

    """
    id: ObjectId
    priority: int
    phone_specs: PhoneSpecs

    def get_search_data(self):
        """

        :return:
        """
        name = self.phone_specs.get_search_str()
        storage_size = self.phone_specs.get_storagesize()

        return {
            'phone': name,
            'storage': storage_size,
            'full_str': name + " " + storage_size.replace(" ", ""),
        }

    def get_match_data(self):
        storage_size = self.phone_specs.get_storagesize()
        other_storage_sizes = []
        for other_storage_size in self.phone_specs.get_other_sizes():
            other_storage_sizes.append(other_storage_size)
            other_storage_sizes.append(other_storage_size.replace(" ", ""))
        return {
            'search_strs': self.phone_specs.get_search_strs(),
            'storage_strs': [storage_size.replace(" ", "").lower(), storage_size.lower()],
            'alt_specs': other_storage_sizes
        }


def make_phones(phone_list):
    """Construct python objects representing smartphones with their specifications

       :param phone_list: list of data of each smartphone to make objects out of
       :return: a list of phone objects
    """

    phones = []
    for phone_dict in phone_list:
        storages = phone_dict.get('specs').get('storage')

        if storages:

            '''exclude storages are the other storages of a particular brand-series-model.
               for example the apple-iphone-x may have storages of 64gb and 128gb meaning
               2 phone objects will be created: apple-iphone-x 64gb and apple-iphone-x 128gb
               the 64gb version will have 128gb as an excluded storage. This is used in 
               matching listings to the correct phone object.'''

            for storage in storages:
                exclude_storage = []
                exclude_storage.extend(storages)
                exclude_storage.remove(storage)

                phone_spec = PhoneSpecs(phone_dict.get('brand'), phone_dict.get('series'), phone_dict.get('model'),
                                        phone_dict.get('search_strs'), storage, exclude_storage)

                new_phone = Phone(phone_dict.get('_id'), phone_dict.get('priority'), phone_spec)
                phones.append(new_phone)

    return phones