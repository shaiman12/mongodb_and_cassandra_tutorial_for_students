from sqlite3 import Timestamp
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
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
    """This query is a more advanced query that actually runs a series of queries because of how our DB set up
    This function will ask a user to input a song name. The functions will return a series of songs that are similar
    to the song that was given by the user.
    The first query finds the song input by the user and returns the similar song list
    The next set of queries finds all the similar song names and artists based on the track_id extracted above
    This will be output to the user in a neat format 
    """    
    title = input('Please input a song title (case-sensitive)\n> ')

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

def delete_record():
    """This query will allow a developer to delete all songs from a specified artist 
    The python code will ask the user to input the artist
    The query will then delete all songs from that input artist 
    In cassandra you are required to use the primary key to perform deletion of rows so 
    two queries are run in this example
    1) find track ids
    2) a series of queries deleting individual tracks
    """   
    artist = input("Input artist name to delete all songs from that artist. Note this permanent:\n")
    qry=f'''
    SELECT * FROM msd.songs WHERE artist = \'{artist}\' ALLOW FILTERING;
    '''
    result = session.execute(qry)
    if (result.one() is None):
        print('Artist is not in DB')
    else:
        track_ids = []
        for song in result:
            track_ids.append(song.track_id)
        for track_id in track_ids:
            qry=f'''
            delete from MSD.songs where track_id = \'{track_id}\' if exists;
            '''
            session.execute(qry)
            print("Deleted 1 row")


def get_all_artists_beginning_with_letter():
    """This function shows you because of the data storage that cassandra offers
    certain queries cannot be run as simply as they can in vanilla SQL. 
    For example in Regular SQL to get the all artists beginning with a letter is quite a simple query
    that uses a 'like; clause. However, this cannot be done without SASII indexes which we will not demonstrate for this
    tutorial. In order to do this query without these Secondary indices we will use python to help run the query
    We first get all unique artist names from cql and let python do the rest.
    This also highlights that simple queries run in SQL cannot be run in a NoSQL partitioned db. We cannot return distinct artists from the DB as this is not
    a request on partition key columns. Our key is track_id based"""
    letter = input("Enter a single letter:\n")[0]
    qry=f'''select artist from msd.songs'''
    results = session.execute(qry)
    all_beginning_with = []
    all_beginning_with = set(all_beginning_with)
    for result in results:
        if result.artist.lower()[0] == letter.lower():
            all_beginning_with.add(result.artist)
    for i in all_beginning_with:
        print(i)

def get_most_frequent_tags():
    """This function runs a query that finds all the tags stored by the dataset. 
    The function ultimately returns the top 10 occuring tags/genres in the dataset
    Because of the way the dataset is structured only one query is used here and the rest is supplemented by 
    python code
    This shows how powerful the combination of NoSQL and python can be
    """
    qry = f'''select tags from msd.songs;'''
    results = session.execute(qry)
    tag_dict = {}
    for r in results:
        if r.tags!=None:
            tags = list(r.tags)
            for tag in tags:
                name = tag[0].lower()
                if name in tag_dict.keys():
                    tag_dict[name] = tag_dict[name]+1
                else:
                    tag_dict[name] = 1
    
    sorted_dict = {k: v for k, v in sorted(tag_dict.items(), key=lambda item: item[1], reverse=True)}
    count = 0
    table_print = []
    for x, y in sorted_dict.items():
        table_print.append((x, y))
        count+=1
        if count==10:
            break
    print(tabulate(table_print, headers=['Genre','Frequency'], tablefmt="github"))
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

def get_tags():
    '''Retrieves a set of tags and their relevance for a given song-artist pair. The query in the function
    bypasses the primary key by using a composite key which can also be used to uniquely 
    identify an item. Since this is not an update - we do not require the primary key.
    The aim of this function is to display a simple get of a collection. Note that if the input for artist
    is left blank, you will receive the tags for all songs of the same name inputted 
    '''
    title = input("Enter a song title\n>")
    artist = input("(Optional) Enter an artist\n>")
    if artist != '':
        query = f'select tags from msd.songs where title = \'{title}\' and artist = \'{artist}\' ALLOW FILTERING;'
    else: 
        query = f'select tags from msd.songs where title = \'{title}\' ALLOW FILTERING;'
    results = session.execute(query)
    arrTracks = []
    for track in results:
        arrTracks.append(track.tags)

    if len(arrTracks)>=1:
        print(tabulate(arrTracks[0], headers=['Tags','Relevance'], tablefmt="github"))
    else:
        print('Song not found.')

def get_songs_with_tag():
    '''Prints a table of all songs and the (relevant artists) that are associated
    with a particular input tag. The aim of this function is to display how nested
    collections can be traversed using Cassandra and Python. We do this by getting
    all tags from the Database and then use python to filter the collection as this
    query is impossible to perform in Cassandra (to our knowledge).
    '''
    tag = input('Please input a tag you want to search with\n> ')
    qry='''
    SELECT artist,title, tags FROM msd.songs;
    '''
    result = session.execute(qry)
    tracks = []
    
    for track in result:
        if(track.tags is not None):
           
            for item in track.tags:
                    if (tag == item[0]):
                        tracks.append((track.title,track.artist))
                        break
    if len(tracks)>0:
        print(tabulate(tracks, headers=['Song','Artist'], tablefmt="github"))
    else: print('No songs with that tag.')

def update_record():
    '''Updates a record's title or artist field. This is implemented as a separate
    update as other values such as timestamp and track_id should be immutable, and
    collection based updates are to be handled differently (see add_tags()). The aim
    of this function is to display a simple update to non-collection based entries. Unlike
    with MongoDB, we cannot perform an update without involving the primary key. As such
    We first fetch the list of relevant track IDs (the primary key) for the update by using song title 
    and artist. Only then do we perform the update.
    '''
    duplicates = []
    title = input('Enter the title of the record you want to update\n>')
    artist = input('Enter the artist of the record you want to update\n>')
    field_type = int(input('Enter the field type you want to update: (0) title (1) artist: '))
    new_entry = input('Enter the new value: ')
    f = ''
    if field_type == 0:
            f = 'title'
    elif field_type == 1:
            f = 'artist'
    qry=f'''
    SELECT track_id FROM msd.songs WHERE title = \'{title}\' AND artist = \'{artist}\' ALLOW FILTERING;
    '''
    result = session.execute(qry)
    for track in result: 
        duplicates.append(track.track_id)
    if len(duplicates)>0:
        for i in duplicates:
            query = f'UPDATE msd.songs SET {f} = \'{new_entry}\' WHERE track_id = \'{i}\';'
            result = session.execute(query)
    else: print('Error in retrieving record. Ensure song title and artist are correct.')
   
    # for i in result: print(i)

def add_tags():
    """Adds a list of tags (separated by ;) to a particular song by a particular artist.
    The function will then print out the new tag set for a given record. The aim of this function
    is to show how one can update a collection. As with the update_records() function, we again
    use title and artist to retrieve the relevant primary key which we then use in the update.
    """    
    to_update = []
    title = input('Enter the title of the record you want to update\n>')
    artist = input('Enter the artist of the record you want to update\n>')
    tags_string = input('Enter the tags and associated relevance factor separated by a semicolon\n>')
    tags_list = tags_string.split(';')
    tags = []
    qry=f'''
    SELECT track_id FROM msd.songs WHERE title = \'{title}\' AND artist = \'{artist}\' ALLOW FILTERING;
    '''
    result = session.execute(qry)
    
    if len(result)>0:
        for track in result: 
            to_update.append(track.track_id)
        for i in tags_list:
            t = i.split()
            tags.append(t)
        for i in to_update:
            for j in tags:
                j = tuple(j)
                query = f'''UPDATE msd.songs SET tags = tags + {{{j}}} WHERE track_id = \'{i}\';'''
                print(query)
                result = session.execute(query)
    else:
        print('Error in retrieving record. Ensure song title and artist are correct.')
        
    
    

setup()
add_tags()
get_tags()