from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests
import sys


cmds_with_sub_cmds = ['flavor-price']

# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the pricing parser'''
    parsers = {}

    # flavor price parser
    flavor_price_parser: ArgumentParser = main_subparsers.add_parser(
        'flavor-price', help='flavor price commands')
    parsers['flavor-price'] = flavor_price_parser
    flavor_price_subparsers: _SubParsersAction = flavor_price_parser.add_subparsers(
        help='sub-commands', dest='sub_command')

    # flavor price list parser
    flavor_price_list_parser: ArgumentParser = flavor_price_subparsers.add_parser(
        'list', help='list flavor prices')

    # flavor price show parser
    flavor_price_show_parser: ArgumentParser = flavor_price_subparsers.add_parser(
        'show', help='show a flavor price')
    flavor_price_show_parser.add_argument('id', type=int, help='id of the flavor price')

    # flavor price create parser
    # flavor price delete parser
    # flavor price modify parser

    return parsers


def parse_args(args: dict):
    '''parse the command line arguments'''
    pass


def flavor_price_list(args: Namespace):
    '''list flavor prices'''
    url = f'{args.url}/pricing/flavorprices'
    headers={'Content-Type': 'application/json',
             'X-Auth-Token': args.token}
    resp = requests.get(url, headers=headers)
    print(resp.json())


def flavor_price_show(args: dict):
    '''show the price with a given id'''
    pass
