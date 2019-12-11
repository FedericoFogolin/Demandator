import argparse
import hashlib
import sqlite3
import os

print(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

from demandator_pkg import db_handler

def parse_arguments1():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', help="add a username (requires -p)", required=False)
    parser.add_argument('-p', help="the username password", required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments1()
    db_handler.open_or_create()
    if args.a and args.p:
        db_handler.save_new_username(args.a, args.p)
