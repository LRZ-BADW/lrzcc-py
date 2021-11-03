#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
# import logging
import os
import sys
import hello
import pricing
import accounting

THISMODULE = sys.modules[__name__]
DESCRIPTION = 'client program for the LRZ Compute Cloud budgeting system'
API_URL = 'http://localhost:8000/api'


parser = None
subparsers = None

parsers = {}
cmds_with_sub_cmds = []

args = None

token = None


def setup_parsers():
    '''setup the main argument parser, and call respective methods for
    each module
    '''
    # main parser
    global parser
    parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
    parser.add_argument('-u',
                        '--url',
                        type = str,
                        help = "URL of the budgeting API to talk to",
                        default=API_URL,
                        )
    parser.add_argument('-t',
                        '--token',
                        type = str,
                        help = """Keystone token for authentication. If not
                        specified, environment variable OS_TOKEN is expected""",
                        )
    parser.add_argument('-d',
                        '--debug',
                        help = """Be more verbose and print out helpful
                                information to figure out why things
                                (do not) work.""",
                        action = "store_true",
                        required = False,
                        default = False,
                        )
    parser.add_argument('-f',
                        '--format',
                        type=str,
                        choices = ["plain",
                                   "simple",
                                   "github",
                                   "grid",
                                   "fancy_grid",
                                   "pipe",
                                   "orgtbl",
                                   "jira",
                                   "presto",
                                   "pretty",
                                   "psql",
                                   "rst",
                                   "mediawiki",
                                   "moinmoin",
                                   "youtrack",
                                   "html",
                                   "unsafehtml",
                                   "latex",
                                   "latex_raw",
                                   "latex_booktabs",
                                   "latex_longtable",
                                   "textile",
                                   "tsv",
                                   ],
                        help = "output table format (default: plain)",
                        required = False,
                        default = "grid",
                        )

    # add main arguments here
    global subparsers
    subparsers = parser.add_subparsers(help='commands',
                                       dest='command')

    # module parsers
    global parsers
    parsers |= hello.setup_parsers(subparsers)
    parsers |= pricing.setup_parsers(subparsers)
    parsers |= accounting.setup_parsers(subparsers)

    # get list of commands with sub-commands
    global cmds_with_sub_cmds
    cmds_with_sub_cmds.extend(hello.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(pricing.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(accounting.cmds_with_sub_cmds)


def parse_args():
    '''parse the command line arguments'''
    global args
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # do argument checks here
    if not args.command:
        parser.print_usage(sys.stderr)
        print(f'{sys.argv[0]}: error: argument missing.', file=sys.stderr)
        exit(1)
    if args.command in cmds_with_sub_cmds and not args.sub_command:
        parsers[args.command].print_usage(sys.stderr)
        print(f'{sys.argv[0]}: error: argument missing.', file=sys.stderr)
        exit(1)

    # Read token either from the command line (preferred if given) or from
    # the environment variable OS_TOKEN.
    args.token = args.token if args.token else os.getenv('OS_TOKEN')
    if args.token:
        # The token string may contain \r and \n
        # We need to rstrip() the string to get rid of these characters
        args.token = args.token.rstrip()
    else:
        print(f"{sys.argv[0]}: error: no Openstack token given. " \
                "Use -t/--token or the environment variable OS_TOKEN.",
                file=sys.stderr)
        exit(1)

    # do module argument checks
    hello.parse_args(args)
    pricing.parse_args(args)
    accounting.parse_args(args)


def execute_command():
    '''execute the respective function for the given command'''

    if args.debug:
        print(args)

    function_name = args.command.replace('-', '_')
    if args.sub_command:
        function_name += f'_{args.sub_command}'
    for module in [hello, pricing, accounting]:
        if hasattr(module, function_name):
            function = getattr(module, function_name)
    function(args)


def main():
    '''the main method'''
    setup_parsers()
    parse_args()
    execute_command()


if __name__ == "__main__":
    main()
