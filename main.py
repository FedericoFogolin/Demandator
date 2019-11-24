import argparse
from demandator import demandator

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="insert the path of the image to analyze")
parser.add_argument("-v", "--verbose", action="count", default=0)
args = parser.parse_args()

demandator.demandator(args.path, args.verbose)