import pymongo.errors
from datagrab.database.mongo import mongo_init


def get_phones_data():
    """
    Connect to the phones database to collect the list of phones by data (brand, model, etc).
    This data will be use for searching and sorting data collected from the datasources (like ebay listings data)
    :return: A list of dictionaries of phones containing needed metadata for searching through & sorting collected data
    """
    phone_metalist = []
    cluster = mongo_init.get_db()
    if cluster:
        database = cluster.phones
        if database:
            try:
                phone_metalist.extend(list(database.find({}, {'_id': 1, 'brand': 1, 'series': 1, 'model': 1, 'search_strs': 1, 'specs.storage': 1, 'priority': 1})))
            except pymongo.errors.OperationFailure:
                print("mongo_reads.get_phones_metadata: Authentiation failed. Try using a different username and/or password")
            except Exception as e:
                print(e)
        else:
            print("mongo_reads.get_phones_metadata: Unable to get phones database.")

    return phone_metalist
