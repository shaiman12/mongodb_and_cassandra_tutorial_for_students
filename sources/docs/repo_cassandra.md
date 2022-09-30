#


### setup
```python
.setup()
```

---
Initialises the DB connection. The cluster is started locally
and connects to the Million Song Dataset (MSD) keyspace.

----


### read_record
```python
.read_record()
```

---
This function returns the song(s) that contain the user-selected song title
If there are no entities in the DB with the song title inputed, the user is promted
that the song is not in the DB. Otherwise, the user is shown the matching song(s) 

----


### delete_all_songs_with_tag
```python
.delete_all_songs_with_tag()
```

---
This function removes all songs that contain the user-selected tag. E.g. Rock
If, no entities contain this tag, the user is informed that no deletions took place.
Otherwise, the number of deleted rows are printed for the user to see.

----


### insert_record
```python
.insert_record()
```

---
This function is a simple creation operation.
A user can input song and artist values, which will then joined with a unique
track ID and a timestamp for when the record was created.
This will all then be inserted into the DB (if it does not already exist).
Notice: Similar songs and tags are not included for simplicity sake.

----


### restore_db
```python
.restore_db()
```

---
This function restores the database to the original state. That is,
before any deletions, insertions or updates were performed. The keyspace will be
dropped and then rebuilt from scratch.

----


### tear_down
```python
.tear_down()
```

---
This function shuts the session down and disconnects any connected clusters


----


### delete_record
```python
.delete_record()
```

---
This query will allow a developer to delete all songs from a specified artist 
The python code will ask the user to input the artist
The query will then delete all songs from that input artist 
In cassandra you are required to use the primary key to perform deletion of rows so 
two queries are run in this example
1) find track ids
2) a series of queries deleting individual tracks

----


### get_all_artists_beginning_with_letter
```python
.get_all_artists_beginning_with_letter()
```

---
This function shows you because of the data storage that cassandra offers
certain queries cannot be run as simply as they can in vanilla SQL. 
For example in Regular SQL to get the all artists beginning with a letter is quite a simple query
that uses a 'like; clause. However, this cannot be done without SASII indexes which we will not demonstrate for this
tutorial. In order to do this query without these Secondary indices we will use python to help run the query
We first get all unique artist names from cql and let python do the rest.
This also highlights that simple queries run in SQL cannot be run in a NoSQL partitioned db. We cannot return distinct artists from the DB as this is not
a request on partition key columns. Our key is track_id based

----


### get_similar_songs
```python
.get_similar_songs()
```

---
This query is a more advanced query that actually runs a series of queries because of how our DB set up
This function will ask a user to input a song name. The functions will return a series of songs that are similar
to the song that was given by the user.
The first query finds the song input by the user and returns the similar song list
The next set of queries finds all the similar song names and artists based on the track_id extracted above
This will be output to the user in a neat format 

----


### average_song_title_length
```python
.average_song_title_length()
```

---
This function returns the average length of all the song titles
in this dataset, formatted to 2 decimal places. All functionality needed
is provided natively by Cassandra, however an auxillary function to find the length
of the song titles had to be defined.

----


### get_most_frequent_tags
```python
.get_most_frequent_tags()
```

---
This function runs a query that finds all the tags stored by the dataset. 
The function ultimately returns the top 10 occuring tags/genres in the dataset
Because of the way the dataset is structured only one query is used here and the rest is supplemented by 
python code
This shows how powerful the combination of NoSQL and python can be

----


### get_tags
```python
.get_tags()
```

---
Retrieves a set of tags and their relevance for a given song-artist pair. The query in the function
bypasses the primary key by using a composite key which can also be used to uniquely 
identify an item. Since this is not an update - we do not require the primary key.
The aim of this function is to display a simple get of a collection. Note that if the input for artist
is left blank, you will receive the tags for all songs of the same name inputted 

----


### get_songs_with_tag
```python
.get_songs_with_tag()
```

---
Prints a table of all songs and the (relevant artists) that are associated
with a particular input tag. The aim of this function is to display how nested
collections can be traversed using Cassandra and Python. We do this by getting
all tags from the Database and then use python to filter the collection as this
query is impossible to perform in Cassandra (to our knowledge).

----


### update_record
```python
.update_record()
```

---
Updates a record's title or artist field. This is implemented as a separate
update as other values such as timestamp and track_id should be immutable, and
collection based updates are to be handled differently (see add_tags()). The aim
of this function is to display a simple update to non-collection based entries. Unlike
with MongoDB, we cannot perform an update without involving the primary key. As such
We first fetch the list of relevant track IDs (the primary key) for the update by using song title 
and artist. Only then do we perform the update.

----


### add_tags
```python
.add_tags()
```

---
Adds a list of tags (separated by ;) to a particular song by a particular artist.
The function will then print out the new tag set for a given record. The aim of this function
is to show how one can update a collection. As with the update_records() function, we again
use title and artist to retrieve the relevant primary key which we then use in the update.
