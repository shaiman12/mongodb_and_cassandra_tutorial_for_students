# Big Data 

Shai Aarons, Jarred Fisher, Joshua Rosenthal

# Introduction
- Welcome to the NoSQL tutorial.
- This tutorial introduces some basic functionality with two popular NoSQL type DBs, namely:
Cassandra and MongoDB
- We have provided some sample queries for both databases that you can run right now.
- The dataset used in this tutorial is a subset of the Last.fm [Million Song Dataset](http://millionsongdataset.com/lastfm/)
- Please refer to the source code and accompaning documentation for further details on the queries and NoSQL databases used
- The queries we offer should get you up to scratch with how to use these technologies
- We try provide easy, intermediate and advanced queries for you to learn the basics as well as more advanced concepts

# Requirements
- Please note that this program is intended for Ubuntu Users
- This program will not work on Windows or MacOs, unless you can install Mongo and Cassandra on your own system
- This program will not work at all on Macs with M1 chips as Cassandra has not yet offered support for M1

# Installation 
- Please run the autorun.sh script. It will install the required dependencies, Mongo and Cassandra and it will start up the program
```sh
./autorun.sh
```

# Queries we provide in this tutorial
1)  Insert new song
2)  Return song(s) (based on song title)
3)  Return all artists beginning with inputted letter
4)  Update song entry (i.e. change title or artist name)
5)  Delete all song by an artist
6)  Get similar songs of a particular song
7)  Get average song title length
8)  Get tags of a song-artist pair
9)  Get top 10 most popular tags 
10) Add tags to a single song
11) Delete all songs with a given tag
12) Get all songs with a specific tag
13) Restore database

# Full Documentation
Please refer to the following files for full details about how everything is run in this program. The Documentation provides detailed insights into each query and how we set up our databases. Alternatively you may view the commented python code:
- [repo_cassandra](docs/repo_cassandra.md) -> This is the file that runs Cassandra Queries
- [repo_mongo](docs/repo_mongo.md) -> This is the file that runs Mongo Queries
- [datawrapper](docs/datawrapper.md) -> This is the file that sets up the databases and populates them with data
- [wrapper](docs/wrapper.md) -> This is the file that presents the user interface for the user
