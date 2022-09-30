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

def delete_record():
    """This query will allow a developer to delete all songs from a specified artist 
    The python code will ask the user to input the artist
    The query will then delete all songs from that input artist 
    """
    artist = input("Input artist name to delete all songs from that artist. Note this permanent:\n")
    posts = collection.delete_many({"artist":artist})
    print(artist +" successfully deleted from database")

def get_all_artists_beginning_with_letter():
    """This query will show the developer the functionality of having to use regex in certain queries
    The user will be prompted to enter a letter
    The DB will return all artists beginning with that input letter
    The query also demonstrates how to use 'distinct' functionality to show only unique arists and not repeats
    The regular expression will match all artists begginning with that input letter.
    """
    letter = input("Enter a single letter:\n")[0]
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
    song_name = input("Enter the name of the song that you wish to find similar songs of\n")
    item_count = collection.count_documents({"title":song_name})
    if item_count == 0:
        print('Song not in database')
    else:

        similars = collection.find({"title":song_name},{"similars":1})
        
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
        print('Songs similar to: ', song_name)
        print(tabulate(table_print, headers=['Title','Artist', 'Similarity Measure'], tablefmt="github"))

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

