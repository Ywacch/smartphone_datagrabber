from datagrab import zeldr_log
from datagrab.datasources import priceapi
from dataclasses import dataclass, field
from typing import List, Any
import time

from asyncebay.config import Config
from asyncebay.request_builder import FindingRequest
from asyncebay import ebay_caller
from datagrab.datasources.ebay import ebay_config, utils, findingKey
from datagrab import temp_listings_store


@dataclass
class eBayPriceAPI(priceapi.PriceAPI):
    """
    child class of PriceAPI for the eBay API
    """
    page_reach: int = 35
    listings_per_page: int = 100
    recursive_get: bool = True
    search_verb: str = field(default='findItemsAdvanced')
    listings: List[Any] = field(default_factory=lambda: [])

    def execute_requests(self):
        utils.reset_daily_call_limit()

        config_dict = {
            'service_name': 'FindingService',
            'app_id': findingKey,
            'site_id': 'EBAY-ENCA',
            'op_name': self.search_verb,
            'response_format': 'JSON'}
        config = Config(config_dict)

        # setup finding api requests building class
        finding = FindingRequest(config)
        finding.build_request_header()
        self.build_urls(finding)

        calls_made = len(finding.urls)

        call_start = time.perf_counter()
        ebay_caller.start(finding.response_list, finding.urls, finding.headers)
        call_stop = time.perf_counter()

        zeldr_log.info(f'eBay call made {calls_made} requests in {call_stop - call_start} seconds')
        zeldr_log.info(f'{len(finding.response_list)} responses returned')
        utils.call_made(calls_made)
        self.listings.extend(finding.response_list)

    def build_urls(self, request):
        baseurl = 'https://svcs.ebay.com/services/search/FindingService/v1?'
        for search in self.search_list:
            payload = 'REST-PAYLOAD&itemFilter(' \
                      '0).name=Condition&itemFilter(0).value=Used&aspectFilter(' \
                      f'0).aspectName=Storage Capacity&aspectFilter(0).aspectValueName={search["storage"]}' \
                      f'&paginationInput.entriesPerPage={self.listings_per_page}' \
                      '&paginationInput.pageNumber={}' \
                      f'&keywords={search["phone"]}'
            request.build_request_urls(baseurl + payload, self.page_reach)

    def get_listings(self):
        listings = []
        empty_responses = 0
        for listing in self.listings:
            try:
                listings.extend(listing['findItemsAdvancedResponse'][0]["searchResult"][0]["item"])
            except KeyError:
                empty_responses += 1
        zeldr_log.info(f"{empty_responses} responses contain no listings")
        self.listings = self.remove_multi_variations(listings)

    def remove_multi_variations(self, listings):
        """
        iterate through the listings returned by eBay and remove the multi variation listings
        :param listings: list of eBay listings
        :return: non multi variation listings
        """
        clean_listings = []
        for listing in listings:
            try:
                if listing["isMultiVariationListing"][0] == 'false':
                    clean_listings.append(listing)
            except Exception as e:
                zeldr_log.exception(e)
        return clean_listings

    def save_listings(self):
        utils.write_json({'listings': self.listings}, temp_listings_store)
