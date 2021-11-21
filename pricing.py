from argparse import _SubParsersAction, ArgumentParser, Namespace
from datetime import datetime

from common import (do_nothing, print_response, api_request, valid_datetime,
                    valid_flavor)


cmds_with_sub_cmds = ['flavor-price']


# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the pricing parser'''
    parsers = {}

    # flavor price parser
    flavor_price_parser: ArgumentParser = main_subparsers.add_parser(
        "flavor-price",
        help="flavor price commands",
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
            help="List flavor prices",
            )

    # flavor price show parser
    flavor_price_show_parser: ArgumentParser = \
        flavor_price_subparsers.add_parser(
            "show",
            help="Show a flavor price",
            )
    flavor_price_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor price',
        )

    # flavor price create parser
    flavor_price_create_parser: ArgumentParser = \
        flavor_price_subparsers.add_parser(
            "create",
            help="Create a flavor price",
            )
    flavor_price_create_parser.add_argument(
        "flavor",
        type=valid_flavor,
        help="Flavor name",
    )
    flavor_price_create_parser.add_argument(
        "userclass",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help="User class",
    )
    flavor_price_create_parser.add_argument(
        "-p",
        "--price",
        type=float,
        help="Price of flavor (default: 0.0)",
        default=0.0,
    )
    flavor_price_create_parser.add_argument(
        "-s",
        "--start-time",
        type=valid_datetime,
        help="Datetime at which this price starts in ISO-8601 format, "
             "so for example 2021-11-09Z12:30:00T "
             "(default: now)",
        default=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    # flavor price delete parser
    flavor_price_delete_parser: ArgumentParser = \
        flavor_price_subparsers.add_parser(
            "delete",
            help="Delete a flavor price",
            )
    flavor_price_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor price',
        )

    # flavor price modify parser
    flavor_price_modify_parser: ArgumentParser = \
        flavor_price_subparsers.add_parser(
            "modify",
            help="Modify a flavor price",
            )
    flavor_price_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor price',
        )

    # avoid variable not used warnings
    do_nothing(flavor_price_list_parser)
    do_nothing(flavor_price_create_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line arguments checks'''
    pass


def flavor_price_list(args: Namespace):
    '''list flavor prices'''
    resp = api_request('get', '/pricing/flavorprices', None, args)
    print_response(resp, args)


def flavor_price_show(args: Namespace):
    '''show the flavor price with the given id'''
    resp = api_request('get', f'/pricing/flavorprices/{args.id}', None, args)
    print_response(resp, args)


def flavor_price_create(args: Namespace):
    '''create a flavor price'''
    data = {
        "flavor": args.flavor,
        "user_class": args.user_class,
        "unit_price": args.price,
        "start_time": args.start_time,
    }
    resp = api_request('post', '/pricing/flavorprices/', data, args)
    print_response(resp, args)


def flavor_price_modify(args: Namespace):
    '''modify the flavor price with the given id'''
    # TODO
    pass


def flavor_price_delete(args: Namespace):
    '''delete the flavor price with the given id'''
    resp = api_request('delete', f'/pricing/flavorprices/{args.id}', None,
                       args)
    print_response(resp, args)
