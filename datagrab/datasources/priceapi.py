from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PriceAPI:
    """
    Base/parent class for holding information used when making api calls to servers holding phone price data
    """
    source_name: str
    search_list: List[Dict] = field(default_factory=lambda: [])

    def add_search_data(self, phone_searches):
        """
        get the list of phone data that will be used to make searches for each phone
        :param phone_searches: list of eBay phone listing containers
        :return:
        """
        self.search_list = phone_searches
