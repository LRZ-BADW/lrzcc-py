from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests
# import sys


cmds_with_sub_cmds = ['flavor-price']


# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the pricing parser'''
    parsers = {}

    # flavor price parser
    flavor_price_parser: ArgumentParser = main_subparsers.add_parser(
            "flavor-price",
            help = "flavor price commands",
            )
    parsers['flavor-price'] = flavor_price_parser
    flavor_price_subparsers: _SubParsersAction = \
            flavor_price_parser.add_subparsers(
                    help="sub-commands",
                    dest="sub_command",
                    )

    # flavor price list parser
    flavor_price_list_parser: ArgumentParser = \
            flavor_price_subparsers.add_parser(
                    "list",
                    help = "List flavor prices",
                    )

    # flavor price show parser
    flavor_price_show_parser: ArgumentParser = \
            flavor_price_subparsers.add_parser(
                    "show",
                    help = "Show a flavor price",
                    )
    flavor_price_show_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the flavor price',
            )

    # flavor price create parser
    flavor_price_create_parser: ArgumentParser = \
            flavor_price_subparsers.add_parser(
                    "create",
                    help = "Create a flavor price",
                    )

    # flavor price delete parser
    flavor_price_delete_parser: ArgumentParser = \
            flavor_price_subparsers.add_parser(
                    "delete",
                    help = "Delete a flavor price",
                    )
    flavor_price_delete_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the flavor price',
            )

    # flavor price modify parser
    flavor_price_modify_parser: ArgumentParser = \
            flavor_price_subparsers.add_parser(
                    "modify",
                    help = "Modify a flavor price",
                    )
    flavor_price_modify_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the flavor price',
            )

    return parsers


def parse_args(args: dict):
    '''parse the command line arguments'''
    # TODO
    pass


def flavor_price_list(args: Namespace):
    '''list flavor prices'''
    url = f'{args.url}/pricing/flavorprices'
    headers={'Content-Type': 'application/json',
             'X-Auth-Token': args.token}
    resp = requests.get(url, headers=headers)
    print(resp.json())


# TODO why dict here instead of Namespace
def flavor_price_show(args: dict):
    '''show the price with a given id'''
    # TODO
    pass


# TODO other methods
