from pymongo import MongoClient

client,db,collection = None,None,None

def setup():
    global client
    global db
    global collection
    
    client = MongoClient('localhost',27017)
    db=client['MSD']
    collection = db['songs']

def insert_data(data:dict):
    
    id = collection.insert_one(data)
    print('Data successfully inserted with id: ', id)