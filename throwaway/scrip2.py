import json

from datagrab.database.mongo import mongo_reads
from datagrab.domain_objects import smartphone, phoneListings
from datagrab.datasources.ebay.match_filters import matchlistings

phones = []
for phone in smartphone.make_phones(mongo_reads.get_phones_data()):
    phones.append(phoneListings.EBayListing(phone))


with open('../datagrab/datafiles/temp_files/temp_listings-november-21-2021.json') as jfile:
    listings = json.load(jfile)['listings']

priority_1 = []
priority_2 = []
priority_3 = []

for phone in phones:
    priority = phone.phone.priority
    if priority == 1:
        priority_1.append(phone)
    elif priority == 2:
        priority_2.append(phone)
    else:
        priority_3.append(phone)

phone = priority_2[1]

search_data = phone.get_match_data()
print(f"matching listings for {search_data}")

listing = {'title': ["Apple iPhone 11 Pro 256GB\u00a0Green, Unlocked & 100% Battery Health"]}
print(listing)
match = matchlistings.match_phone_listing(search_data, listing['title'][0])
print(match)
