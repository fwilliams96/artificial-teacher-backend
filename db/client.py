from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ENVIRONMENT = os.environ.get("ENVIRONMENT")

if ENVIRONMENT == 'PRODUCTION':
    # Base datos remota
    REMOTE_MONGO_URL = os.environ.get("REMOTE_MONGO_URL")
    db_client = MongoClient(REMOTE_MONGO_URL).chat
else:
    # Base datos local
    db_client = MongoClient().chat

