import os

import argparse
import datawrapper as dw
import repo_mongo as rm
import repo_cassandra as rc


def main():
    #datawrapper.load_data_mongo()
    #datawrapper.load_data_cassandra()
    rc.setup()
    rc.get_similar_songs('China Doll')

def parseArgs():
    pass

if __name__ == "__main__":
    main()