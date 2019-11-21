import argparse
from demandator import demandator

parser = argparse.ArgumentParser()
parser.add_argument("path", help="insert the path of the image to analyze")
args = parser.parse_args()

demandator.demandator(args.path)
