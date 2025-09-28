
import os
import sys
import json
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL not found in environment variables")
print("MongoDB URL:", MONGO_DB_URL)

# Fix certifi SSL path
ca = certifi.where()

# ------------------------------
# Class for Network Data Extraction
# ------------------------------
class NetworkDataExtract:
    def __init__(self):
        try:
            # Initialize Mongo client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        """Converts a CSV file to a list of JSON records"""
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def insert_data_mongodb(self, records, database, collection, unique_key="url"):
        """
        Inserts JSON records into MongoDB.
        Skips duplicates based on the unique_key.
        """
        try:
            db = self.mongo_client[database]   # Select database
            col = db[collection]               # Select collection

            # Create unique index on the unique_key
            col.create_index(unique_key, unique=True)

            # Insert records, skipping duplicates
            try:
                result = col.insert_many(records, ordered=False)
                inserted_count = len(result.inserted_ids)
                logger.info(f"Inserted {inserted_count} new records into {collection}")
                return inserted_count
            except pymongo.errors.BulkWriteError as bwe:
                inserted_count = bwe.details.get("nInserted", 0)
                logger.warning(f"Duplicate records found. Inserted {inserted_count} new records.")
                return inserted_count

        except Exception as e:
            raise NetworkSecurityException(e, sys)

# ------------------------------
# Main script
# ------------------------------
if __name__ == '__main__':
    try:
        # File and MongoDB details
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABASE = "amisha31"
        COLLECTION = "NetworkData"
        UNIQUE_KEY = "url"  # replace with the column in CSV that should be unique

        # Create object
        networkobj = NetworkDataExtract()

        # Convert CSV to JSON
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(f"Loaded {len(records)} records from CSV")
        logger.info(f"Loaded {len(records)} records from CSV")

        # Insert into MongoDB with duplicate handling
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION, UNIQUE_KEY)
        print(f"Inserted {no_of_records} new records into MongoDB")
        logger.info(f"Inserted {no_of_records} new records into MongoDB")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
