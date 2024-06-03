from xmlrpc.server import SimpleXMLRPCServer

from blockchain.database import *
import yaml

def load_config(file_path):
    with open(file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            return None

config_file = 'node3009.yaml'

config = load_config(config_file)
set_file_path(config)
cachedb = CacheDB()
cache = cachedb.find_all()
