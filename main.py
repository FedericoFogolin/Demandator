#! /usr/bin/env python3

import argparse
from demandator_pkg import demandator, db_handler

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="insert the path of the image to analyze")
    parser.add_argument('-p', help="the username password", required=True)
    parser.add_argument('-u', help="check for a usernamename and password (requires -p)", required=True)
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity parameter")
    parser.add_argument("-n", "--n_results", type = int, default=5,choices = range(1, 51, 1), help="insert number of results to show from 1 to 50")
    parser.add_argument("-t", "--threshold", type = float, default=0.0, help="insert minimum treshold of accuracy for prediction to display ")
    parser.add_argument("--graph", action='store_true', default=False, help="insert --graph if you want to see the graph of the prediction")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    db_handler.open_or_create()
    if args.u and args.p:
        if db_handler.check_for_username(args.u, args.p):
            demandator.demandator(args.path, args.verbose, args.n_results, args.threshold, args.graph)
        else:
            print('[ERROR] The User is not valid or the password is incorrect.')
    else:
        print("[ERROR] No User has been selected or added. Type 'main.py -h' or 'main.py --help' for further Informations.")
