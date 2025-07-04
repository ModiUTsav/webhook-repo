from pymongo import MongoClient
from flask import current_app,g
import os 

class MongoExtension:
    def __init__(self):
        self.client = None
        self.db = None
        self.events_collection = None
    
    def init_app(self,app):
        mongo_uri = os.getenv("MONGO_URI","mongodb://localhost:27017/")
        Db_name = os.getenv("MONGO_DB_NAME","webhook_repo")
        collection_name = os.getenv('MONGO_COLLECTION_NAME', 'webhook_events')

        self.client = MongoClient(mongo_uri)
        self.db = self.client[Db_name]
        self.events_collection = self.db[collection_name]

        self.events_collection.create_index([("timestamp", -1)])

        @app.teardown_appcontext
        def teardown_mongo(exception):
            client = g.pop('mongo_client', None)
            if client is not None:
                client.close()

    mongo = MongoExtension()

    def get_events_collection():
        return mongo.events_collection            