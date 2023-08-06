#!/usr/bin/python3

# Usage: python -m shellviz [options] data
# Data can be piped in or passed as an argument.
# e.g. python -m shellviz [options] '[1, 2, 3]'
# e.g. python -m shellviz [options] < data.json
# options:
#  -h, --help            show this help message and exit
#  -i ID, --id=ID        ID of the visualization to update


import argparse
import sys
from . import visualize


def main():
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Process data for shellviz')
    parser.add_argument('-i', '--id', type=int, help='ID of the visualization to update')
    parser.add_argument('data', nargs='?', help='Data to process; may be passed from input redirection (e.g. shellviz < data.json), piped (e.g. cat data.son | shellviz) or passed as an argument (e.g. shellviz "[1, 2, 3]")')
    args = parser.parse_args()

    data = args.data or sys.stdin.read()
    id = args.id

    result = visualize(data, id)
    print(result)


if __name__ == '__main__':
    main()
