from pymongo import MongoClient

# Base datos local
db_client = MongoClient().local 

# Base datos remota
#db_client = MongoClient("mongodb+srv://fwmcomputer:pAZo34M1oopMdknf@cluster0.dabizfp.mongodb.net/?retryWrites=true&w=majority").test

