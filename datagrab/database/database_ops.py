from datagrab import datagrab_log
from datagrab.database.mongo import mongo_reads
from datagrab.database.postgres import postgres_db


def create_tables():
    datagrab_log.info('Attempting to create database tables')
    database = postgres_db.Database()
    database.init_tables()
    database.close_db()


def get_mongodb_phones():
    datagrab_log.info('Attempting to retrieve smartphones from MongoDB')
    return mongo_reads.get_phones_data()


def update_postgres_phones(phones):
    datagrab_log.info('Attempting to update smartphones in postgres')
    smarthphone_db = postgres_db.SmartPhoneTable()
    smarthphone_db.add_phones(phones)
    smarthphone_db.close_db()


def add_listings(listings):
    datagrab_log.info('Attempting to save listings data to postgres')
    listings_db = postgres_db.ListingTable()
    listings_db.add_listings(listings)
    listings_db.close_db()


def add_phonelistings(phonelistings):
    datagrab_log.info('Attempting to save matched listings data to postgres')
    phonelistings_db = postgres_db.PhoneListingTable()
    phonelistings_db.add_phonelistings(phonelistings)
    phonelistings_db.close_db()
