from cassandra.cluster import Cluster
from tabulate import tabulate

session = None
clstr = None

def setup():
    global session
    global clstr
    clstr=Cluster()
    session = clstr.connect('msd')

def get_similar_songs(title):
    
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

def tear_down():

    session.shutdown()
    clstr.shutdown()