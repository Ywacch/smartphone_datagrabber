from datagrab.datasources import priceapi
from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class eBayPriceAPI(priceapi.PriceAPI):
    """
    child class of PriceAPI
    """
    page_reach: int = 35
    listings_per_page: int = 100
    recursive_get: bool = True
    search_verb: str = field(default='findItemsAdvanced')

    def build_requests(self):
        for search in self.search_list:
            search['request_dict'] = {
                'keywords': search['phone'],
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'currency', 'value': 'CAD'},
                    # {'name': 'minPrice', 'value': 100.0}
                ],
                'aspectFilter': [
                    {
                        'aspectName': 'Storage Capacity',
                        'aspectValueName': search['storage']
                    }
                ],
                'categoryId': 9355,
                'paginationInput': {
                    'entriesPerPage': self.listings_per_page,
                    'pageNumber': 1
                },
                'sortOrder': 'BestMatch'
            }


@dataclass
class eBayListings:
    item_name: str
    listings: List[Any]
