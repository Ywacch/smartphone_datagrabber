from pprint import pprint
from datagrab import smartphone
from datagrab.database import mongo_reads

phone_db = mongo_reads.get_phones_data()

phones = smartphone.make_phones(phone_db)

for count, phone in enumerate(phones, start=1):
    print(count, phone.get_search_data())
