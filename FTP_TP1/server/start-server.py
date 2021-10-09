import argparse

parser = argparse.ArgumentParser('start-server', description='<command description>')

group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
group.add_argument('-q', '--quiet', help='decrease output verbosity', dest='verbose', action='store_false')

parser.add_argument('-H', '--host', help='host service IP address', metavar='ADDR')
parser.add_argument('-p', '--port', help='service port', metavar='PORT')
parser.add_argument('-s', '--storage', help='storage dir path', metavar='DIRPATH')

print(parser.parse_args())