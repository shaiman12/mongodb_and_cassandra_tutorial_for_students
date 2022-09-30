
from cassandra.cluster import Cluster
from tabulate import tabulate

session = None
clstr = None

def setup():
    global session
    global clstr
    clstr=Cluster()
    session = clstr.connect('msd')

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

def tear_down():

    session.shutdown()
    clstr.shutdown()

setup()
get_all_artists_beginning_with_letter()