#! /usr/bin/env python3

import argparse
from demandator_pkg import demandator, db_handler
import logging
import verboselogs
from numpy import arange, around

logger = verboselogs.VerboseLogger('demo')
logger.addHandler(logging.StreamHandler())


def parse_arguments():
    # TODO find a way to hide or make homogeneus METAVAR
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", type=str,
                        help="insert the path of the image to analyze")
    parser.add_argument("-p", "--password", help="the username password",
                        required=True)
    parser.add_argument("-u", "--username",
                        help="""check for a usernamename and password
                        (requires -p)""", required=True)
    # TODO limit maximum number of -v to 2 and alert the user
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase verbosity parameter")
    parser.add_argument("-n", "--n_results", type=int, default=5,
                        choices=range(1, 51, 1),
                        help="insert number of results to show from 1 to 50")
    parser.add_argument("-t", "--threshold", type=float, default=0.0,
                        choices=around(arange(0, 1, 0.01),2),
                        help="""insert minimum treshold of accuracy for
                        prediction to display""")
    parser.add_argument("-g", "--graph", action="store_true", default=False,
                        help="""insert -g if you want to see the graph of
                        the prediction""")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    if db_handler.open_database(args.verbose, './user-pwd.db'):
        if args.username and args.password:
            if db_handler.check_for_username(args.username, args.password,
                                             args.verbose):
                demandator.demandator(args.image_path, args.verbose,
                                      args.n_results, args.threshold,
                                      args.graph)
            else:
                logger.error("""[ERROR] The Username is not present or
                             password is invalid.""")
        else:
            logger.error("""[ERROR] No User has been selected or added.
                         Type 'main.py -h' or 'main.py --help' for
                         further information""")
