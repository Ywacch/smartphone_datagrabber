from datagrab.domain_objects.smartphone import Phone
from dataclasses import dataclass, field
from typing import List, Any


@dataclass(order=True)
class EBayListing:
    """
    A class representing the relationship between a phone and it's listings collected
    """
    phone: Phone = field(compare=False)
    listings: List[Any] = field(default_factory=lambda: [], compare=False)

    def get_search_data(self):
        return self.phone.get_search_data()

    def get_match_data(self):
        return self.phone.get_match_data()

    def add_listing(self, listing):
        if listing not in self.listings:
            self.listings.append(listing)

    @property
    def priority(self):
        return self.phone.priority

    def get_phone_listings(self):
        return [{
            'phone_id': self.phone.id_,
            'item_id': listing['item_id'],
            'date_added': listing['date_added']
        } for listing in self.listings]

    def clear_listings(self):
        self.listings.clear()

    def __str__(self):
        return f"{self.phone} object holding {len(self.listings)} listings"
    
    def phone_name(self):
        return Phone.phone_name
