import argparse
import os
import sys
from blockchain.node import Node
from pathlib import Path


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(arg + " does not exist.")
    else:
        return arg


def run():
    parser = argparse.ArgumentParser(description='Executes Blockchain based on a config file')
    parser.add_argument(dest="config_file",
                        help="config file and its path", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()

    config_file = Path(args.config_file)

    chainNode = Node(config_file)
    chainNode.start()


if __name__ == '__main__':
    run()
