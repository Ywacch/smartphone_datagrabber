import psycopg2
from psycopg2.sql import SQL, Identifier
import psycopg2.extras as psy_extras

from datagrab import datagrab_log
from datagrab.database import db_config
from datagrab.database.postgres import schema


class Database:

    def __init__(self):
        try:
            config = db_config.get_config('postgres')
            self.connection = psycopg2.connect(host=config['host'], database=config['database'], user=config["user"],
                                               password=config["password"])
        except Exception as e:
            datagrab_log.error(e)
    
    
    def init_tables(self):
        try:
            with open(schema, 'r') as file:
                statement = file.read()
        except Exception as e:
            datagrab_log.error(e)
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(statement)
        except Exception as e:
            datagrab_log.error(e)

    def close_db(self):
        self.connection.close()


class ListingTable(Database):
    def __init__(self):
        super(ListingTable, self).__init__()
        self.table_name = 'listings'

    def get_listings(self):
        phone_listings = []
        with self.connection:
            with self.connection.cursor() as cursor:
                # 'SELECT * FROM {} WHERE uID = %s AND url_prefix = %s'
                sql_statement = SQL('SELECT * FROM {} ').format(
                    Identifier(self.table_name))
                cursor.execute(sql_statement)
                listings = cursor.fetchall()
            if listings:
                for listing in listings:
                    phone_listings.append(listing[0])
            return phone_listings

    def add_listings(self, listings):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql_statement = SQL('INSERT INTO {} (item_id, title, global_id, product_id, postal_code, '
                                    'location_, country, currency, price, condition_, shipping_type, '
                                    'shipping_currency, shipping_cost, top_rated, start_date, end_date, listing_type, '
                                    'date_added) '
                                    'VALUES (%(item_id)s, %(title)s, %(global_id)s, %(product_id)s, %(postal_code)s, '
                                    '%(location_)s, %(country)s, %(currency)s, %(price)s, %(condition_)s, '
                                    '%(shipping_type)s, %(shipping_currency)s, %(shipping_cost)s, %(top_rated)s, '
                                    '%(start_date)s, %(end_date)s, %(listing_type)s, %(date_added)s)'
                                    'ON CONFLICT (item_id, date_added) DO NOTHING;').format(Identifier(self.table_name))
                psy_extras.execute_batch(cursor, sql_statement, listings)


class SmartPhoneTable(Database):

    def __init__(self):
        super(SmartPhoneTable, self).__init__()
        self.table_name = "smartphones"

    def get_phones(self):  # seems like code duplication
        phones = []
        with self.connection:
            with self.connection.cursor() as cursor:
                # 'SELECT * FROM {} WHERE uID = %s AND url_prefix = %s'
                sql_statement = SQL('SELECT * FROM {} ').format(
                    Identifier(self.table_name))
                cursor.execute(sql_statement)
                phone_list = cursor.fetchall()
            if phone_list:
                for phone in phone_list:
                    phones.append(phone[0])
            return phones

    def add_phones(self, phones):
        with self.connection:
            with self.connection.cursor() as cursor:
                for phone in phones:
                    sql_statement = SQL('INSERT INTO {} (phone_id, brand, model, series, phone_name, storage_size) '
                                        'VALUES (%s, %s, %s, %s, %s, %s)'
                                        'ON CONFLICT (phone_id) DO NOTHING;').format(
                        Identifier(self.table_name))
                    cursor.execute(sql_statement, (phone.id_, phone.brand, phone.model, phone.series, phone.phone_name, phone.size))


class PhoneListingTable(Database):

    def __init__(self):
        super(PhoneListingTable, self).__init__()
        self.table_name = "phonelistings"

    def add_phonelistings(self, phonelistings):
        with self.connection:
            with self.connection.cursor() as cursor:
                sql_statement = SQL('INSERT INTO {} (phone_id, item_id, date_added)'
                                    'VALUES (%(phone_id)s, %(item_id)s, %(date_added)s)'
                                    'ON CONFLICT (phone_id, item_id, date_added) DO NOTHING;').format(Identifier(self.table_name))
                psy_extras.execute_batch(cursor, sql_statement, phonelistings)
