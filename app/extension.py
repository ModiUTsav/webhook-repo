# app/extensions.py
from pymongo import MongoClient
from flask import g 
import os

class MongoExtension:
    def __init__(self):
        self.client = None
        self.db = None
        self.events_collection = None

    def init_app(self, app):
        """
        Initializes the MongoDB connection with the Flask app.
        This method should be called from your create_app function.
        """
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGO_DB_NAME", "webhook_repo")
        collection_name = os.getenv('MONGO_COLLECTION_NAME', 'webhook_events')

        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.events_collection = self.db[collection_name]

            # Ensure index for timestamp for efficient querying
            self.events_collection.create_index([("timestamp", -1)])
            print(f"MongoDB connected to DB: {db_name}, Collection: {collection_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            
        @app.teardown_appcontext
        def teardown_mongo(exception):
            
            client_to_close = g.pop('mongo_client', None)
            if client_to_close is not None:
                client_to_close.close()
                print("MongoDB client closed.")


mongo = MongoExtension()

def get_events_collection():
    """
    Helper function to get the events collection from the global mongo instance.
    This is what  routes will call.
    """
    if mongo.events_collection is None:
      
        raise RuntimeError("MongoDB events_collection not initialized. Call mongo.init_app(app) first.")
    return mongo.events_collection