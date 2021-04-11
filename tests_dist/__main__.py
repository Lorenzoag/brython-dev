
import argparse

def install(args):
    print(args)

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

install = subparser.add_parser('install', help='Install in an empty directory')
install.set_defaults(func=install)

