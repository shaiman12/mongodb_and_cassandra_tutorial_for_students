from pymongo import MongoClient
from tabulate import tabulate
import uuid
import datetime

client,db,collection = None,None,None

def setup():

    """Initialises the DB connection. The client is started locally
    and connects to the Million Song Dataset (MSD). The collection (i.e. table) that
    is connected to is the \'songs'\ collection 
    """

    global client
    global db
    global collection
    
    client = MongoClient('localhost',27017)
    db=client['MSD']
    collection = db['songs']


def read_record():

    """This function returns the song(s) that contain the user-selected song title
    If there are no entities in the DB with the song title inputed, the user is promted
    that the song is not in the DB. Otherwise, the user is shown the matching song(s) 
    """

    title = input('Please input a song title\n> ')
    qry = {"title":title}
    arrTracks = []
    for track in collection.find(qry, {"similars":0, "tags":0}):
        arrTracks.append((track['_id'],track['track_id'],track['artist'], str(track['timestamp']), track['title']))
        
    
    if(len(arrTracks) != 0):
        print(tabulate(arrTracks, headers=['_id','Track_id','Artist', 'Timestamp', 'Title'], tablefmt="github"))
    else:
        print('Song not in database')

def delete_all_songs_with_tag():

    """This function removes all songs that contain the user-selected tag. E.g. Rock
    If, no entities contain this tag, the user is informed that no deletions took place.
    Otherwise, the number of deleted rows are printed for the user to see.
    """

    tag = input('Please input a tag to delete on\n> ')
    qry = {'tags':{'$elemMatch':{'$elemMatch':{'$in':[tag]}}}}

    x = collection.delete_many(qry)

    if(x!=0):
        print(x.deleted_count, " documents deleted.")
    else:
        print('No songs with tag: ',f'\'{tag}\'')

def insert_record():

    """This function is a simple creation operation.
    A user can input song and artist values, which will then joined with a unique
    track ID and a timestamp for when the record was created. This will all then be inserted into the DB.
    Notice: Similar songs and tags are not included for simplicity sake.
    """
    
    title = input('Please input a song title\n> ')
    artist = input('Please input the song artist\n> ')
    track_id = str(uuid.uuid4())
    
    t_stamp = datetime.datetime.now()

    data = {'track_id':track_id,'title': title, 'artist':artist,'timestamp':t_stamp}

    id = collection.insert_one(data)
    print('Data successfully inserted with id: ', id.inserted_id)

def restore_db():

    """This function restores the database to the original state. That is,
    before any deletions, insertions or updates were performed. The database will be
    dropped and then rebuilt from scratch.
    """

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

    """This function shuts the session down and disconnects any connected databases
    """

    client.close()

def delete_record():

    """This query will allow a developer to delete all songs from a specified artist 
    The python code will ask the user to input the artist
    The query will then delete all songs from that input artist 
    """

    artist = input("Input artist name to delete all songs from that artist. Note this is permanent:\n> ")
    posts = collection.delete_many({"artist":artist})
    print(artist +" successfully deleted from database")

def get_all_artists_beginning_with_letter():

    """This query will show the developer the functionality of having to use regex in certain queries
    The user will be prompted to enter a letter
    The DB will return all artists beginning with that input letter
    The query also demonstrates how to use 'distinct' functionality to show only unique arists and not repeats
    The regular expression will match all artists begginning with that input letter.
    """

    letter = input("Enter a single letter:\n> ")[0]
    query_string = "/^"+letter+"/"
    artists = collection.find({"artist": { '$regex': '^'+letter, '$options': 'i' }}, {}).distinct("artist")
    for artist in artists:
        print(artist)

def get_similar_songs():

    """This query is a more advanced query that actually runs a series of queries because of how our DB set up
    This function will ask a user to input a song name. The functions will return a series of songs that are similar
    to the song that was given by the user.
    The first query finds the song input by the user and returns the similar song list
    The next set of queries finds all the similar song names and artists based on the track_id extracted above
    This will be output to the user in a neat format 
    """

    title = input('Please input a song title (case-sensitive):\n> ')
    item_count = collection.count_documents({"title":title})
    if item_count == 0:
        print('Song not in database')
    else:

        similars = collection.find({"title":title},{"similars":1})
        
        tracks = []
        
        similars = similars[0]['similars']
        for song in similars:
            tracks.append(song)
        table_print = []
        
        for song in tracks:
            try:
                result = collection.find({"track_id":song[0]}, {"artist":1, "title":1})
                table_print.append((result[0]['title'], result[0]['artist'], song[1]))
            except:
                pass
        
        table_print  = set(table_print)
        table_print = sorted(table_print, key=lambda tup:tup[2], reverse=True)    
        print('Songs similar to: ', title)
        print(tabulate(table_print, headers=['Title','Artist', 'Similarity Measure'], tablefmt="github"))

def average_song_title_length():

    """This function returns the average length of all the song titles
    in this dataset, formatted to 2 decimal places. All functionality needed
    is provided natively by MongoDB
    """

    result = collection.aggregate([
        { '$group': { '_id': 'null', 'avg': { '$avg': { '$strLenCP': "$title" } } } } ]
    )

    avg_length = result.next()['avg']

    print('Average song title length = ',round(avg_length,2),' characters')

def get_most_frequent_tags():

    """This function runs a query that finds all the tags stored by the dataset. 
    The function ultimately returns the top 10 occuring tags/genres in the dataset
    Because of the way the dataset is structured only one query is used here and the rest is supplemented by 
    python code
    This shows how powerful the combination of NoSQL and python can be
    """

    all_tags = collection.find({},{"tags":1})
    tag_dict = {}
    for tagset in all_tags:
        tags = tagset['tags']
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

def get_tags():

    '''Retrieves a set of tags and their relevance for a given song-artist pair. The query in the function
    bypasses the primary key by using a composite key which can also be used to uniquely 
    identify an item. The aim of this function is to display a simple get of a collection.
    '''

    title = input("Enter a song title\n> ")
    artist = input("(Optional) Enter an artist\n> ")
    if artist == '':
        query = {"title" : title}
    else:
        query = {"title" : title, "artist" : artist}

    doc = collection.find(query)
    
    for x in doc:

        print(tabulate(x['tags'],headers=['Tag','Relevance'], tablefmt="github"))

 
    

def get_songs_with_tag():

    '''Prints a table of all songs and the (relevant artists) that are associated
    with a particular input tag. The aim of this function is to display both a
    large-scale search as well as how to search within nested collections.
    '''

    tag = input('Enter a tag you want to search with\n>')
    songs = []
    query = {"tags":{"$elemMatch":{"$elemMatch":{"$eq":tag}}}}
    doc = collection.find(query)
    for x in doc:
        songs.append((x['title'],x['artist']))
    print(tabulate(songs,headers=['Song','Artist'], tablefmt="github"))
        
    

def update_record():
    '''Updates a record's title or artist field. This is implemented as a separate
    update as other values such as timestamp and track_id should be immutable, and
    collection based updates are to be handled differently (see add_tags()). The aim
    of this function is to display a simple update to non-collection based entries.
    '''
    song = input('Enter the title of the record you want to update\n> ')
    artist = input('Enter the artist of the record you want to update\n> ')
    field_type = int(input('Enter the field type you want to update: (0) title (1) artist: '))
    new_entry = input('Enter the new value: ')
    
    f = ''
    if field_type == 0:
            f = 'title'
    elif field_type == 1:
            f = 'artist'
    query = {'artist': artist,'title' : song}
    update = {'$set':{f:new_entry}}
    collection.update_one(query,update)
        
def add_tags():
    """Adds a list of tags (separated by ;) to a particular song by a particular artist.
    The function will then print out the new tag set for a given record. The aim of this function
    is to show how one can update a collection.
    """    
    song = input('Enter the title of the record you want to update\n> ')
    artist = input('Enter the artist of the record you want to update\n> ')
    tags_string = input('Enter the tags and associated relevance factor separated by a semicolon\n> ')
    tags_list = tags_string.split(';')
    tags = []
    for i in tags_list:
        t = i.split()
        tags.append(t)
    for i in tags:
        collection.update_one({'artist': artist,'title' : song},{'$push':{'tags':i}})
    query = {'artist': artist,'title' : song}
    doc = collection.find(query)
    print('New Tags')
    for x in doc:
        print(tabulate(x['tags'],headers=['Tags'],tablefmt='github'))
