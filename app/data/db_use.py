########### OLD ###########

from pymongo import MongoClient
import os
from dotenv import load_dotenv
# from pathlib import Path

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
