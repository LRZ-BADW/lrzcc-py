from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests


cmds_with_sub_cmds = ['hello']


def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the hello parser'''
    parsers = {}

    # hello action parser
    hello_parser: ArgumentParser = main_subparsers.add_parser(
        "hello",
        help = "hello commands",
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
                    help = "Hello as normal user",
                    )

    # hello admin parser
    hello_admin_parser: ArgumentParser = \
            hello_subparsers.add_parser(
                    "admin",
                    help = "Hello as admin user",
                    )

    return parsers


def parse_args(args: dict):
    '''parse the command line arguments'''
    # TODO
    pass


def hello_user(args: Namespace):
    '''hello for users'''
    # TODO
    pass


def hello_admin(args: dict):
    '''hello for admins'''
    # TODO
    pass
