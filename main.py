#! /usr/bin/env python3

import argparse
from demandator_pkg import demandator

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="insert the path of the image to analyze")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("-n", "--n_results", type = int, default=5, help="insert number of results to show")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    demandator.demandator(args.path, args.verbose, args.n_results)
