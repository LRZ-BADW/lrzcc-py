#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
# import logging
import os
import sys
import user
import hello
import pricing
import accounting
import quota
import resources
import budgeting
from common import issue_api_token, revoke_api_token, parse_user


THISMODULE = sys.modules[__name__]
DESCRIPTION = 'CLI client for LRZ specific features of the Compute Cloud'
API_URL = 'https://cc.lrz.de:1337/api'


parser = None
subparsers = None

parsers = {}
cmd_mod_map = {}
cmds_with_sub_cmds = []

args = None

token = None
token_issued = False
keystone_url = None

module = None


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
                        type=str,
                        help="URL of the budgeting API to talk to",
                        default=API_URL,
                        )
    parser.add_argument('-t',
                        '--token',
                        type=str,
                        help="""Keystone token for authentication. If not
                        specified, environment variable OS_TOKEN is
                        expected""",
                        )
    parser.add_argument('-d',
                        '--debug',
                        help="""Be more verbose and print out helpful
                                information to figure out why things
                                (do not) work.""",
                        action="store_true",
                        required=False,
                        default=False,
                        )
    parser.add_argument('-f',
                        '--format',
                        type=str,
                        choices=["json",
                                 "plain",
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
                        help="output table format (default: plain)",
                        required=False,
                        default="github",
                        )
    parser.add_argument('-N',
                        '--names',
                        action='store_true',
                        help="""force parser to treat arguments that could
                             be names or IDs as names""",
                        )
    parser.add_argument('-I',
                        '--ids',
                        action='store_true',
                        help="""force parser to treat arguments that could
                             be names or IDs as IDs""",
                        )
    parser.add_argument('-i',
                        '--impersonate',
                        type=str,
                        help="Username or ID of the user to impersonate",
                        )

    # add main arguments here
    global subparsers
    subparsers = parser.add_subparsers(help='commands',
                                       dest='command')

    # module parsers
    global parsers
    parsers.update(user.setup_parsers(subparsers))
    parsers.update(hello.setup_parsers(subparsers))
    parsers.update(pricing.setup_parsers(subparsers))
    parsers.update(accounting.setup_parsers(subparsers))
    parsers.update(quota.setup_parsers(subparsers))
    parsers.update(resources.setup_parsers(subparsers))
    parsers.update(budgeting.setup_parsers(subparsers))

    # get list of commands with sub-commands
    global cmds_with_sub_cmds
    cmds_with_sub_cmds.extend(user.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(hello.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(pricing.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(accounting.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(quota.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(resources.cmds_with_sub_cmds)
    cmds_with_sub_cmds.extend(budgeting.cmds_with_sub_cmds)

    # get command to module map
    for module in [user, hello, pricing, accounting, quota, resources,
                   budgeting]:
        for cmd in module.cmds:
            cmd_mod_map[cmd] = module


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
    if not args.token:
        global token_issued
        global keystone_url
        keystone_url = os.getenv('OS_AUTH_URL')
        username = os.getenv('OS_USERNAME')
        password = os.getenv('OS_PASSWORD')
        user_domain_name = os.getenv('OS_USER_DOMAIN_NAME')
        project_name = os.getenv('OS_PROJECT_NAME')
        project_domain_id = os.getenv('OS_PROJECT_DOMAIN_ID')
        if (keystone_url and username and password and user_domain_name
                and project_name and project_domain_id):
            args.token = issue_api_token(keystone_url, username, password,
                                         user_domain_name, project_name,
                                         project_domain_id)
            if not args.token:
                print(f"{sys.argv[0]}: error: the Openstack authentication "
                      "with the provided credentials failed. Unable to "
                      "acquire a token. Please make sure the openrc file "
                      "you sourced is correct.",
                      file=sys.stderr)
                exit(1)
            token_issued = True
        else:
            print(f"{sys.argv[0]}: error: no Openstack token or login "
                  "credentials given. Source your openrc file, use -t/--token "
                  "or the environment variable OS_TOKEN.",
                  file=sys.stderr)
            exit(1)

    # check that --names and --ids are not both given
    if args.names and args.ids:
        print(f"{sys.argv[0]}: error: mutually exclusive arguments "
              "Use -n/--names OR -i/--ids but not both.",
              file=sys.stderr)
        exit(1)

    # parse impersonation user if given
    if args.impersonate:
        parse_user(args, 'impersonate')

    # get module for specified command
    global module
    module = cmd_mod_map[args.command]

    # do module argument checks
    module.parse_args(args)


def execute_command():
    '''execute the respective function for the given command'''

    if args.debug:
        print(args)

    function_name = args.command.replace('-', '_')
    if 'sub_command' in args and args.sub_command:
        function_name += f'_{args.sub_command}'
    if hasattr(module, function_name):
        function = getattr(module, function_name)
    function(args)


def clean_up():
    '''clean up afterwards'''
    if token_issued:
        revoked = revoke_api_token(keystone_url, args.token)
        if not revoked:
            print(f"{sys.argv[0]}: error: token could not be revoked. Please "
                  f" revoke the following token manually: {args.token}",
                  file=sys.stderr)
            exit(1)


def main():
    '''the main method'''
    setup_parsers()
    parse_args()
    execute_command()
    clean_up()


if __name__ == "__main__":
    main()
