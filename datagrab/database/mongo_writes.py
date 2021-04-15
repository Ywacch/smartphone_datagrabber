from datagrab.database import mongo_init


def prep_mongo_store(phones):
    """
    Checks if the each phone has a price time series in the mongodb. If True, do nothing, If False,
    Create a phone dictionary to represent the phone and its specs to contain the time series and save it to mongodb
    :param phones: List if phone items that eBay data was collected on
    :return: None
    """
    database = mongo_init.get_db()
    collection = database.price_history

    if collection:
        for phone in phones:
            if collection.count_documents({'_id': phone.id}) == 0:
                price_doc = {'_id': phone.id, 'phone': phone.search_strs[0], 'price_data_by_specs': dict()}
                for silo in phone.silos.keys():
                    phone_silo = phone.silos[silo]
                    price_doc['price_data_by_specs'][silo] = []
                    # print(f'adding {phone.search_str} {phone_silo.search_data["specs"]}')
                collection.insert_one(price_doc)


def save_stats_db(phones):
    """
    Save the daily stats of phone prices to its unique mongodb instance, identifying each phone by id
    :param phones: List if phone items that eBay data was collected on
    :return: None
    """
    database = mongo_init.get_db()
    collection = database.price_history

    if collection:
        for phone in phones:
            for silo in phone.silos.keys():
                phone_silo = phone.silos[silo]
                collection.update_one({'_id': phone.id}, {"$push": {f'price_data_by_specs.{phone_silo.search_data["specs"]}': phone_silo.stat_metrics}})
