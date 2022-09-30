#


### setup
```python
.setup()
```

---
Initialises the DB connection. The client is started locally
and connects to the Million Song Dataset (MSD). The collection (i.e. table) that
is connected to is the 'songs'\ collection 

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
track ID and a timestamp for when the record was created. This will all then be inserted into the DB.
Notice: Similar songs and tags are not included for simplicity sake.

----


### restore_db
```python
.restore_db()
```

---
This function restores the database to the original state. That is,
before any deletions, insertions or updates were performed. The database will be
dropped and then rebuilt from scratch.

----


### tear_down
```python
.tear_down()
```

---
This function shuts the session down and disconnects any connected databases


----


### delete_record
```python
.delete_record()
```

---
This query will allow a developer to delete all songs from a specified artist 
The python code will ask the user to input the artist
The query will then delete all songs from that input artist 

----


### get_all_artists_beginning_with_letter
```python
.get_all_artists_beginning_with_letter()
```

---
This query will show the developer the functionality of having to use regex in certain queries
The user will be prompted to enter a letter
The DB will return all artists beginning with that input letter
The query also demonstrates how to use 'distinct' functionality to show only unique arists and not repeats
The regular expression will match all artists begginning with that input letter.

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
is provided natively by MongoDB

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
identify an item. The aim of this function is to display a simple get of a collection.

----


### get_songs_with_tag
```python
.get_songs_with_tag()
```

---
Prints a table of all songs and the (relevant artists) that are associated
with a particular input tag. The aim of this function is to display both a
large-scale search as well as how to search within nested collections.

----


### update_record
```python
.update_record()
```

---
Updates a record's title or artist field. This is implemented as a separate
update as other values such as timestamp and track_id should be immutable, and
collection based updates are to be handled differently (see add_tags()). The aim
of this function is to display a simple update to non-collection based entries.

----


### add_tags
```python
.add_tags()
```

---
Adds a list of tags (separated by ;) to a particular song by a particular artist.
The function will then print out the new tag set for a given record. The aim of this function
is to show how one can update a collection.
