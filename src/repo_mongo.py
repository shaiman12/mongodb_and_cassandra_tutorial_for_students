from pymongo import MongoClient
from tabulate import tabulate
import uuid
import datetime

client,db,collection = None,None,None

def setup():
    global client
    global db
    global collection
    
    client = MongoClient('localhost',27017)
    db=client['MSD']
    collection = db['songs']

def get_similar_songs():
    pass

def read_record():
    title = input('Please input a song title\n> ')
    qry = {"title":title}
    arrTracks = []
    for track in collection.find(qry):
        print(track)
    for track in collection.find(qry, {"similars":0, "tags":0}):
        arrTracks.append((track['_id'],track['track_id'],track['artist'], str(track['timestamp']), track['title']))
        
    
    if(len(arrTracks) != 0):
        print(tabulate(arrTracks, headers=['_id','Track_id','Artist', 'Timestamp', 'Title'], tablefmt="github"))
    else:
        print('Song not in database')

def remove_all_songs_with_tag():
    tag = input('Please input a tag to delete on\n> ')
    qry = {'tags':{'$elemMatch':{'$elemMatch':{'$in':[tag]}}}}

    x = collection.delete_many(qry)

    if(x!=0):
        print(x.deleted_count, " documents deleted.")
    else:
        print('No songs with tag: ',f'\'{tag}\'')

def insert_record():
    
    title = input('Please input a song title\n> ')
    artist = input('Please input the song artist\n> ')
    track_id = str(uuid.uuid4())
    
    t_stamp = datetime.datetime.now()

    data = {'track_id':track_id,'title': title, 'artist':artist,'timestamp':t_stamp}

    id = collection.insert_one(data)
    print('Data successfully inserted with id: ', id.inserted_id)

def restore_db():

    user_choice = input('This operation will drop the database and restore the songs table\n'+
                    'Please confirm this operation by entering (Y)es or (N)o\n> ')
    
    from wrapper import str2bool

    if(str2bool(user_choice)):
        
        client.drop_database('MSD')
        print('DB dropped')
        from datawrapper import load_data_mongo

        load_data_mongo()
    else:
        print('Operation cancelled')

def tear_down():

    client.close()
