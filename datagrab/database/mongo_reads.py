import pymongo.errors
from datagrab.database import mongo_init


def get_phones_data():
    """
    Connect to the phones database to collect the list of phone objects with data about brand, model, etc.
    This data will be use for searching and sorting data collected from the datasources (like ebay listings data)
    :return: A list of dictionaries of phones containing needed data for searching through & sorting collected data
    """
    phones = []
    cluster = mongo_init.get_db()
    if cluster:
        database = cluster.phones
        if database:
            try:
                phones.extend(list(database.find({}, {'_id': 1, 'brand': 1, 'series': 1, 'model': 1, 'search_strs': 1, 'specs.storage': 1, 'priority': 1})))
            except pymongo.errors.OperationFailure:
                print("mongo_reads.get_phones_data: Authentiation failed. Try using a different username and/or "
                      "password")
            except Exception as e:
                print(e)
        else:
            print("mongo_reads.get_phones_data: Unable to get phones database.")

    return phones
