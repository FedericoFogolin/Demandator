#! /usr/bin/env python3

import argparse
from demandator import demandator

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="insert the path of the image to analyze")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    demandator.demandator(args.path, args.verbose)