import argparse
import hashlib
import sqlite3
import os
import sys
sys.path.append(".")  # Adds higher directory to python modules path.
# This import is not at the top as it needed the above entry.
from demandator_pkg import db_handler


def parse_arguments1():
    '''This function parses all the parameters inserted in the command line
    ----------
    Parameters
    ----------
    -a : username
    -p : username's password
    -v : increase verbosity parameter
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', help="Username", required=True)
    parser.add_argument('-p', help="Password", required=True)
    parser.add_argument('-v', "--verbose", action="count", default=0,
                        help="increase verbosity parameter")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments1() 
    db_handler.open_or_create(args.verbose, './user-pwd.db')
    if args.a and args.p:
        db_handler.save_new_username(args.a, args.p, args.verbose)
