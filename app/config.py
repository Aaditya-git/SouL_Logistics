from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    try:
        client = MongoClient(os.getenv('MONGO_URI'))
        print("Connected to MongoDB Atlas successfully.")
        return client[os.getenv('MONGO_DATABASE')]
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
