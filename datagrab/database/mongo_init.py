import yaml
import pymongo.errors
from pymongo import MongoClient
from datagrab.database import yaml_config


def get_config():
    """
    open the yaml config file and parse it
    :return: parsed yaml file if found
    """
    try:
        with open(yaml_config, 'r') as file:
            parsed_yml = yaml.load(file, Loader=yaml.FullLoader)
            return parsed_yml
    except FileNotFoundError:
        print("mongo_init.get_config: Config file not found. Please insert a file named 'config.yaml' in the database/datafiles directory")
    except Exception as e:
        print(f"mongo_init.get_config: Error occurred: {e}")


def get_db():
    """
    Connect to the mongodb atlas cluster using the username and password provided by the user via a yaml file
    :return: A mongo client of the devices database
    """
    config = get_config()
    if config:
        username = config['mongo_username']
        password = config['mongo_password']

        try:
            uri = f'mongodb+srv://{username}:{password}@zeldr-avclh.mongodb.net/test?retryWrites=true&w=majority'
            client = MongoClient(uri)
            database = client.devices
        except pymongo.errors.ServerSelectionTimeoutError:
            print(f"mongo_init.get_db: ServerSelectionTimeout occurred: it may be that your IP isn't on the whitelist")
        except Exception as e:
            print(f"mongo_init.get_db: {e}")
        else:
            return database
    else:
        print("get_db: Unable to get config file.")
