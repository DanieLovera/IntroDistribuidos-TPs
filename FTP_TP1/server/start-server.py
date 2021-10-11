import os
import sys
import argparse

script_dir = os.path.dirname(__file__)
myModule_dir = os.path.join(script_dir, '..', 'common')
sys.path.append(myModule_dir)

def parseArguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    group.add_argument('-q', '--quiet', help='decrease output verbosity', dest='verbose', action='store_false')

    parser.add_argument('-H', '--host', help='host service IP address', default='localhost', metavar='ADDR')
    parser.add_argument('-p', '--port', help='service port', metavar='PORT', type=int)
    parser.add_argument('-s', '--storage', help='storage dir path', metavar='DIRPATH')

def main():
    parser = argparse.ArgumentParser('start-server', description='<command description>')

    parseArguments(parser)
    args = parser.parse_args()