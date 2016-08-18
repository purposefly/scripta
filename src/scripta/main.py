#!/usr/bin/env python

import sys
import argparse
import importlib
import traceback
import pprint
from botocore.exceptions import ClientError

clients = {
    'lambda': 'lambda_'
}


# noinspection PyBroadException
def invoke(module, client, command, args):
    try:
        instance = importlib.import_module('scripta.%s.%s' % (module, clients.get(client, client)))
        function = getattr(instance, command.replace('-', '_'))
    except Exception:
        print('Failed to load command %s.%s.%s()' % (module, client, command))
        sys.exit(255)

    try:
        function(args)
    except ClientError as e:
        traceback.print_exc()
        pprint.pprint(e.response)
        sys.exit(255)
    except Exception:
        traceback.print_exc()
        sys.exit(255)


def main():
    # command-line parser
    parser = argparse.ArgumentParser(description='Scripta Tools')
    parser.add_argument('module', help='module name')
    parser.add_argument('client', help='AWS client')
    parser.add_argument('command', help='AWS client command')
    xargs, xargv = parser.parse_known_args()

    # invoke command
    invoke(xargs.module, xargs.client, xargs.command, xargv)


if __name__ == '__main__':
    main()
