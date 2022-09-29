import os

import argparse
import datawrapper as dw
import repo_mongo as rm
import repo_cassandra as rc
from time import sleep
from time import time
from timeit import default_timer as timer
from time import perf_counter
import time
import sys

exit_codes = ['q', 'quit','exit','e', 'end']

query_options = '''
To exit this program, just type \'(q)uit\'\n
Select any of the following queries (enter the number):
1)  Return selected record
2)  Delete certain record
3)  Delete certain record
4)  Delete certain record
5)  Delete certain record
6)  Get similar songs for track
7)  Return selected record
8)  Delete certain record
9)  Delete certain record
10) Delete certain record
11) Delete certain record
12) Get similar songs for track
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
  
    switch_function ={'1':switch_module[db_selected].get_similar_songs,
                '2':switch_module[db_selected].get_similar_songs,
                '3':switch_module[db_selected].get_similar_songs,
                '4':switch_module[db_selected].get_similar_songs,
                '5':switch_module[db_selected].get_similar_songs,
                '6':switch_module[db_selected].get_similar_songs,
                '7':switch_module[db_selected].get_similar_songs,
                '8':switch_module[db_selected].get_similar_songs,
                '9':switch_module[db_selected].get_similar_songs,
                '10':switch_module[db_selected].get_similar_songs,
                '11':switch_module[db_selected].get_similar_songs,
                '12':switch_module[db_selected].get_similar_songs}

    user_input = ''
    print(query_options)
    while(True):
        user_input = str(input('> '))
        if(user_input in exit_codes):
            break
        start = time.process_time()
        switch_function[user_input]()
        elapsed_time = round(time.process_time() - start,4)
        print('Result returned in: ', elapsed_time, ' seconds')
        print('')
        input('Press the Enter key to clear output and reprint query options')
        os.system('cls||clear')
        print(query_options)

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

if __name__ == "__main__":
    main()