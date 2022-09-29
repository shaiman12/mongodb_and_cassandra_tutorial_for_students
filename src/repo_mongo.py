from pymongo import MongoClient
from tabulate import tabulate

client,db,collection = None,None,None

def setup():
    global client
    global db
    global collection
    
    client = MongoClient('localhost',27017)
    db=client['MSD']
    collection = db['songs']

def insert_data():
    
    id = collection.insert_one()
    print('Data successfully inserted with id: ', id)