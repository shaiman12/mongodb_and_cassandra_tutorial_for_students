#


### load_data_mongo
```python
.load_data_mongo()
```

---
This function sets up a MongoDB client on the user's local machine.
If the Million Song Dataset(MSD) database has not yet been created, the data will be loaded
in from the raw JSON files and inserted into the database.

----


### load_data_cassandra
```python
.load_data_cassandra()
```

---
This function sets up a Cassandra cluster on the user's local machine.
A Cassandra session then connects to the cluster.
If the Million Song Dataset(MSD) keyspace has not yet been created,the MSD keyspace will be built and the
songs table will be made.
Therafter, the data will read in from the raw JSON files and inserted into the database.
Please take notice: 
The insertion time is longer than it ought to be, this is due to Cassandra's strong typing enforcement which
requires handling fine-grained type conversions, because of how the fields are stored in the raw JSON files.
Ideally, the field values in the JSON files should be adapted and stored permanetely in the appropriate encodings.
