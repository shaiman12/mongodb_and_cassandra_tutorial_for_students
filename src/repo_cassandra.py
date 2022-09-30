from sqlite3 import Timestamp
from cassandra.cluster import Cluster
from tabulate import tabulate
import datetime
import uuid

session = None
clstr = None

def setup():
    global session
    global clstr
    clstr=Cluster()
    session = clstr.connect('msd')

def read_record():
    title = input('Please input a song title\n> ')
    qry=f'''
    SELECT * FROM msd.songs WHERE title = \'{title}\' ALLOW FILTERING;
    '''
    result = session.execute(qry)
    if (result.one() is None):
        print('Song not in database')
    else:
        arrTracks = []
        for track in result:
            
            arrTracks.append((track.track_id,track.artist, str(track.timestamp), track.title))
        
        print(tabulate(arrTracks, headers=['Track_id','Artist', 'Timestamp', 'Title'], tablefmt="github"))
            
def delete_all_songs_with_tag():
    
    tag = input('Please input a tag to delete on\n> ')
    qry=f'''
    SELECT track_id, tags FROM msd.songs;
    '''
    result = session.execute(qry)
    tracks_to_delete = []
    
    for track in result:
        
            if(track.tags is not None):
            
                for item in track.tags:
                    if(tag==item[0]):
                        tracks_to_delete.append(track.track_id)
                        break
    num_delete = len(tracks_to_delete)
    if(num_delete!=0):
        tracks_to_delete = tuple(tracks_to_delete)
        
        qry=f'''
        DELETE FROM msd.songs WHERE track_id IN {tracks_to_delete};
        '''
        session.execute(qry)
        print('Applied: True. Number of rows deleted: ', num_delete)
    else:
        print('No songs with tag: ',f'\'{tag}\'')


def get_similar_songs():
    
    title = input('Please input a song title:\n> ')

    qry=f'''
    SELECT similars FROM msd.songs WHERE title = \'{title}\' ALLOW FILTERING;
    '''
    result = session.execute(qry)
    if (result.one() is None):
        print('Song not in database')
    else:
        arrTracks = []
        for track in result[0][0]:
            arrTracks.append(track)
        
        table_print = []
        for song in arrTracks:
            
            try:
                result = session.execute(f'SELECT title, artist FROM msd.songs WHERE track_id = \'{song[0]}\' ALLOW FILTERING;')
                table_print.append((result[0].title, result[0].artist, song[1]))
            except:
                pass
        table_print = set(table_print)
        table_print = sorted(table_print, key=lambda tup:tup[2], reverse=True)    
        print('Songs similar to: ', title)
        print(tabulate(table_print, headers=['Title','Artist', 'Similarity Measure'], tablefmt="github"))

#TODO: Implement
def get_most_frequent_tags():
    pass

#TODO: Implement
def get_all_artists_beginning_with_letter():
    pass

#TODO: Implement
def delete_record():
    pass

def insert_record():


    title = input('Please input a song title\n> ')
    artist = input('Please input the song artist\n> ')
    track_id = uuid.uuid4()
    t_stamp = datetime.datetime.now()
    
    qry=f'''
    INSERT INTO msd.songs (track_id, title, artist, timestamp)
    VALUES (\'{track_id}\', \'{title}\', \'{artist}\', \'{t_stamp}\')
    IF NOT EXISTS;
    '''
    print(session.execute(qry).one())
    
def restore_db():

    user_choice = input('This operation will drop the database and restore the songs table\n'+
                    'Please confirm this operation by entering (Y)es or (N)o\n> ')
    from wrapper import str2bool

    if(str2bool(user_choice)):

        qry=f'''
        DROP KEYSPACE IF EXISTS msd;
        '''
        session.execute(qry)
        print('DB dropped')
        from datawrapper import load_data_cassandra

        load_data_cassandra()
        
    else:
        print('Operation cancelled')

def tear_down():

    session.shutdown()
    clstr.shutdown()