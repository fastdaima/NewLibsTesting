from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance()


@singleton
class MongoDBConnection(object):
    def __init__(self, host, username, password, port, database_name):
        uri = f'mongodb://{username}:{password}@{host}/{database_name}?authSource=admin'
        self.connection = MongoClient(uri)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def retrieve_data():
    client = MongoClient()



@app.route('/api/service/idp/list', methods=['GET'])
def get_list():
    pass

@app.route('/api/service/idp/{id}', methods=['GET'])
def get_item():
    pass