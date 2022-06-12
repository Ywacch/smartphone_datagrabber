from datagrab.database.mongo import mongo_reads
from datagrab.database.postgres import postgres_db


def create_tables():
    database = postgres_db.Database()
    database.init_tables()


def get_mongodb_phones():
    return mongo_reads.get_phones_data()


def update_postgres_phones(phones):
    smarthphone_db = postgres_db.SmartPhoneTable()
    smarthphone_db.add_phones(phones)
    smarthphone_db.close_db()


def add_listings(listings):
    listings_db = postgres_db.ListingTable()
    listings_db.add_listings(listings)
    listings_db.close_db()


def add_phonelistings(phonelistings):
    phonelistings_db = postgres_db.PhoneListingTable()
    phonelistings_db.add_phonelistings(phonelistings)
    phonelistings_db.close_db()
