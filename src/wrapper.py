import os
from argparse import ArgumentTypeError
import argparse
import datawrapper as dw
import repo_mongo as rm
import repo_cassandra as rc
from time import sleep

import sys
from time import process_time

exit_codes = ['q', 'quit','exit','e', 'end']

#TODO: Input other query options
query_options = '''
To exit this program, just type \'(q)uit\'\n
Select any of the following queries (enter the number):
1)  Insert new song
2)  Return whole record (based on song title)
3)  Delete certain record
4)  Delete certain record
5)  Delete certain record
6)  Get similar songs for track
7)  Return selected record
8)  Delete certain record
9)  Delete certain record
10) Delete certain record
11) Delete all songs with a given tag
12) Get similar songs for track
13) Restore database
'''

switch_module ={'1':rm, '2':rc}
db_selected = None


def main():
    
    global db_selected
    printWelcomeInformation()

    db_selected = input('To begin this tutorial, please select MongoDB (1) or Cassandra (2)\n'+
                        'Enter 1 or 2\n> ')
    
    if(db_selected != '1' and db_selected != '2'):
        sys.exit('Please select a DB to work with by inputing a 1 for MongoDB or 2 for Cassandra')
    print('-----------------------------')
    
    if db_selected == '1':
        print('You selected MongoDB')
        dw.load_data_mongo()
        rm.setup()
    else:
        print('You selected Cassandra')
        dw.load_data_cassandra()
        rc.setup() 
  
    #This dictionary maps between the database type the user selected
    #and any query a user selects to run 
    #TODO: Input other query function names

    switch_function ={'1':switch_module[db_selected].insert_record,
                '2':switch_module[db_selected].read_record,
                '3':switch_module[db_selected].get_similar_songs,
                '4':switch_module[db_selected].get_similar_songs,
                '5':switch_module[db_selected].get_similar_songs,
                '6':switch_module[db_selected].get_similar_songs,
                '7':switch_module[db_selected].get_similar_songs,
                '8':switch_module[db_selected].get_similar_songs,
                '9':switch_module[db_selected].get_similar_songs,
                '10':switch_module[db_selected].get_similar_songs,
                '11':switch_module[db_selected].remove_all_songs_with_tag,
                '12':switch_module[db_selected].get_similar_songs,
                '13':switch_module[db_selected].restore_db}

    user_input = ''
    print(query_options)

    #Start user-input loop
    while(True):
        user_input = str(input('> ')).lower()

        
        if(user_input == ''):
            continue
        #Break loop when user inputs a 'quit' command
        if(user_input in exit_codes):
            break

        
        start_time = process_time()

        #Call appropriate query function based on user's selection
        switch_function[user_input]()

        #Evaluate time taken to perform the query selected, for the DB type selected
        elapsed_time = round(process_time() - start_time,4)
        print('')
        print('Query executed in: ', elapsed_time, ' seconds')
        print('')
        
        input('Press the Enter key to clear output and reprint query options')
        os.system('cls||clear')
        print(query_options)

    rm.tear_down if db_selected == '1' else rc.tear_down

def parseArgs():
    pass


def printWelcomeInformation():
    print('Welcome to the NoSQL tutorial')
    print('-----------------------------')
    sleep(1)

    print('This tutorial introduces some basic functionality with two popular NoSQL type DBs, namely:')
    print('1) MongoDB: Document-store')
    print('2) Cassandra: Column-store')
    print('-----------------------------')
    sleep(1)

    print('We have provided some sample queries for both databases that you can run right now.')
    print('The dataset used in this tutorial is a subset of the Last.fm Million Song Dataset (http://millionsongdataset.com/lastfm/)')
    print('Please refer to the source code and accompaning documentation for further details on the queries and NoSQL databases used')
    print('-----------------------------')
    sleep(1)

def str2bool(b):
    if isinstance(b, bool):
        return b
    if b.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif b.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    main()