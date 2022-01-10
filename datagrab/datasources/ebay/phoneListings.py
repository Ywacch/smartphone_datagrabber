from datagrab.smartphone import Phone
from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class EBayListing:
    """
    A class representing the relationship between a phone and it's listings collected
    """
    phone: Phone
    listings: List[Any] = field(default_factory=lambda: [])

    def get_search_data(self):
        return self.phone.get_search_data()

    def get_match_data(self):
        return self.phone.get_match_data()
