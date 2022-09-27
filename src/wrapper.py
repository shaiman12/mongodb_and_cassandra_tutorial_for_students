import os

import argparse
import datawrapper
import repo


def main():
    #datawrapper.load_data_mongo()
    datawrapper.load_data_cassandra()
    

def parseArgs():
    pass

if __name__ == "__main__":
    main()