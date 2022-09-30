import json
import os
from pymongo import MongoClient
from cassandra.cluster import Cluster

def load_data_mongo():

    """This function sets up a MongoDB client on the user's local machine.
    If the Million Song Dataset(MSD) database has not yet been created, the data will be loaded
    in from the raw JSON files and inserted into the database.
    """

    client = MongoClient('localhost',27017)
    if('MSD' not in client.list_database_names()):
        db=client['MSD']
        collection = db['songs']
        print('Inserting Data... Please wait')
        #TODO: Test insert_many instead of insert_one
        data_to_insert = []
        for file in os.listdir("./data/"):
            f = open('./data/' + file)
            data = json.load(f)
            data_to_insert.append(data)
            f.close()
        collection.insert_many(data_to_insert)
        print('Data inserted')
    else:
        print('MSD Data already loaded')
    client.close()


def load_data_cassandra():

    """This function sets up a Cassandra cluster on the user's local machine.
    A Cassandra session then connects to the cluster.
    If the Million Song Dataset(MSD) keyspace has not yet been created,the MSD keyspace will be built and the
    songs table will be made. Therafter, the data will read in from the raw JSON files and inserted into the database.
    Note: The insertion time is longer than it ought to be, this is due to Cassandra's strong typing enforcement which
    requires handling fine-grained type conversions, because of how the fields are stored in the raw JSON files.
    Ideally, the field values in the JSON files should be adapted and stored permanetely in the appropriate encodings.
    """

    clstr=Cluster()
    session = clstr.connect()
    data = list(clstr.metadata.keyspaces.keys())
    session.shutdown()

    if('msd' not in data):
        session = clstr.connect()
        session.execute("create keyspace msd with replication={'class': 'SimpleStrategy', 'replication_factor' : 1};")
        print('Keyspace created: MSD')
        session.shutdown()
        session = clstr.connect('msd')

        qry= '''
        CREATE TABLE songs (
            track_id text,
            title text,
            artist text,
            timestamp timestamp,
            similars set<tuple<text,float>>,
            tags set<tuple<text,text>>,
            primary key(track_id)
        );'''
        session.execute(qry)
        
        session.encoder.mapping[tuple] = session.encoder.cql_encode_tuple
        print('Inserting Data... Please wait')
        for file in os.listdir("./data/"):
            f = open('./data/' + file)
            data = json.load(f)
            
            session.execute(
            '''
            insert into msd.songs (track_id, title, artist, timestamp, similars, tags)
            values (%s,%s,%s,%s,%s,%s)
            ''',
            (data['track_id'],data['title'],data['artist'],data['timestamp'],helper(data['similars']), helper(data['tags']))
            )
            
        print('Data inserted')
        session.shutdown()
        clstr.shutdown()

def helper(data):

    """This auxillary function adapts the list of lists found in the Raw JSON files
    into sets of tuples (which our Cassandra instance requires)

    Returns:
        set<tuple(a,b)>: collection type (for input to Cassandra DB)
    """

    new_data = []
    for i in data:
        new_data.append(tuple(i))
    
    return set(new_data)

