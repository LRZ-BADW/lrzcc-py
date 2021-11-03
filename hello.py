from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests
import tabulate


cmds_with_sub_cmds = ['hello']


def do_nothing(variable):
    pass


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
    do_nothing(hello_user_parser)
    do_nothing(hello_admin_parser)

    return parsers


def parse_args(args: Namespace):
    '''parse the command line arguments'''
    # TODO
    pass


def hello_user(args: Namespace):
    '''hello for users'''
    url = f'{args.url}/hello'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    resp = requests.get(url, headers=headers)
    output = tabulate.tabulate(resp.json().items(), tablefmt=args.format)
    print(output)


def hello_admin(args: Namespace):
    '''hello for admins'''
    url = f'{args.url}/hello/admin'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    resp = requests.get(url, headers=headers)
    output = tabulate.tabulate(resp.json().items(), tablefmt=args.format)
    print(output)
