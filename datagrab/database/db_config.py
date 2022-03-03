import yaml
from datagrab.database import postgres_config, mongo_config


def get_config(config_filename):
    """
    open the yaml config file and parse it
    :return: parsed yaml file if found
    """
    if config_filename == 'postgres':
        yaml_file = postgres_config
    elif config_filename == 'mongodb':
        yaml_file = mongo_config
    else:
        yaml_file = None

    try:
        with open(yaml_file, 'r') as file:
            parsed_yml = yaml.load(file, Loader=yaml.FullLoader)
            return parsed_yml
    except FileNotFoundError:
        print(f" Config file not found. Please insert a file named {yaml_file} in the database/datafiles directory")
    except Exception as e:
        print(f"Error occurred at db_config: {e}")
