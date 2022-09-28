import json
import os
from pymongo import MongoClient
from cassandra.cluster import Cluster

def load_data_mongo():
    client = MongoClient('localhost',27017)
    if('MSD' not in client.list_database_names()):
        db=client['MSD']
        collection = db['songs']

        for file in os.listdir("./data/"):
            f = open('./data/' + file)
            data = json.load(f)
            collection.insert_one(data)
            f.close()
        print('Song data loaded')
    else:
        print('MSD Data already loaded')
    client.close()


def load_data_cassandra():
    clstr=Cluster()
    session = clstr.connect()
    data = list(clstr.metadata.keyspaces.keys())
    session.shutdown()

    if('msd' not in data):
        session = clstr.connect()
        session.execute("create keyspace msd with replication={'class': 'SimpleStrategy', 'replication_factor' : 3};")
        print('Keyspace created: MSD')
        session.shutdown()
        session = clstr.connect('msd')
        qry= '''
        create table songs (
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
        for file in os.listdir("./data/"):
            f = open('./data/' + file)
            data = json.load(f)
            # qry= f'insert into msd.songs JSON \'{data}\';'
            
            session.execute(
            '''
            insert into msd.songs (track_id, title, artist, timestamp, similars, tags)
            values (%s,%s,%s,%s,%s,%s)
            ''',
            (data['track_id'],data['title'],data['artist'],data['timestamp'],helper(data['similars']), helper(data['tags']))
            )
            
        
        session.shutdown()
        clstr.shutdown()

def helper(data):
    new_data = []
    for i in data:
        new_data.append(tuple(i))
    
    return set(new_data)
