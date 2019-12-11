import argparse
import hashlib
import sqlite3
import os
import sys

sys.path.append(".") # Adds higher directory to python modules path.
from demandator_pkg import db_handler

def parse_arguments1():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', help="Username", required=True)
    parser.add_argument('-p', help="Password", required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments1()
    db_handler.open_or_create()
    if args.a and args.p:
        db_handler.save_new_username(args.a, args.p)
