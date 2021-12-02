from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests
import tabulate

import common


cmds = ['hello']
cmds_with_sub_cmds = ['hello']


def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the hello parser'''
    parsers = {}

    # hello action parser
    hello_parser: ArgumentParser = main_subparsers.add_parser(
        "hello",
        help="hello commands",
        )
    parsers['hello'] = hello_parser
    hello_subparsers: _SubParsersAction = \
        hello_parser.add_subparsers(
                help="sub-commands",
                dest="sub_command",
                )

    # hello user parser
    hello_user_parser: ArgumentParser = \
        hello_subparsers.add_parser(
                "user",
                help="Hello as normal user",
                )

    # hello admin parser
    hello_admin_parser: ArgumentParser = \
        hello_subparsers.add_parser(
                "admin",
                help="Hello as admin user",
                )

    # just to avoid unused variable warnings
    common.do_nothing(hello_user_parser)
    common.do_nothing(hello_admin_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line arguments checks'''
    pass


def hello_user(args: Namespace):
    '''hello for users'''
    resp = common.api_request('get', '/hello', None, args)
    common.print_response(resp, args)


def hello_admin(args: Namespace):
    '''hello for admins'''
    resp = common.api_request('get', '/hello/admin', None, args)
    common.print_response(resp, args)
