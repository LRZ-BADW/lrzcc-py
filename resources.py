from argparse import _SubParsersAction, ArgumentParser, Namespace
from datetime import datetime

from common import (do_nothing, print_response, api_request, valid_datetime,
                    valid_flavor)

cmds_with_sub_cmds = ['flavor', 'flavor-group']


# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the quota parser'''
    parsers = {}

    # flavor parser
    flavor_parser: ArgumentParser = main_subparsers.add_parser(
        "flavor",
        help="flavor commands",
        )
    parsers['flavor'] = flavor_parser
    flavor_subparsers: _SubParsersAction = \
        flavor_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # flavor group parser
    flavor_group_parser: ArgumentParser = main_subparsers.add_parser(
        "flavor-group",
        help="flavor group commands",
        )
    parsers['flavor-group'] = flavor_group_parser
    flavor_group_subparsers: _SubParsersAction = \
        flavor_group_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # flavor list parser
    flavor_list_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "list",
            help="List flavors",
            )

    # flavor show parser
    flavor_show_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "show",
            help="Show a flavor",
            )
    flavor_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor',
        )

    # flavor create parser
    flavor_create_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "create",
            help="Create a flavor",
            )
    flavor_create_parser.add_argument(
        "name",
        type=str,
        help="Flavor name",
    )

    # flavor delete parser
    flavor_delete_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "delete",
            help="Delete a flavor",
            )
    flavor_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor',
        )

    # flavor modify parser
    flavor_modify_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "modify",
            help="Modify a flavor",
            )
    flavor_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor',
        )

    # flavor group list parser
    flavor_group_list_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "list",
            help="List flavors",
            )

    # flavor group show parser
    flavor_group_show_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "show",
            help="Show a flavor group",
            )
    flavor_group_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor group',
        )

    # flavor group create parser
    flavor_group_create_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "create",
            help="Create a flavor group",
            )
    flavor_group_create_parser.add_argument(
        "name",
        type=str,
        help="Flavor group name",
    )

    # flavor group delete parser
    flavor_group_delete_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "delete",
            help="Delete a flavor group",
            )
    flavor_group_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor group',
        )

    # flavor group modify parser
    flavor_group_modify_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "modify",
            help="Modify a flavor group",
            )
    flavor_group_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor group',
        )

    # avoid variable not used warnings
    do_nothing(flavor_list_parser)
    do_nothing(flavor_group_list_parser)

    return parsers


def parse_args(args: Namespace):
    '''parse the command line arguments'''
    # TODO
    pass


def flavor_list(args: Namespace):
    '''list flavors'''
    resp = api_request('get', '/resources/flavors', None, args)
    print_response(resp, args)


def flavor_show(args: Namespace):
    '''show the flavor with the given id'''
    resp = api_request('get', f'/resources/flavors/{args.id}', None, args)
    print_response(resp, args)


def flavor_create(args: Namespace):
    '''create a flavor'''
    data = {
        "name": args.name,
        # "group": None,
    }
    print(data)
    resp = api_request('post', '/resources/flavors/', data, args)
    print_response(resp, args)


def flavor_modify(args: Namespace):
    '''modify the flavor with the given id'''
    # TODO
    pass


def flavor_delete(args: Namespace):
    '''delete the flavor with the given id'''
    resp = api_request('delete', f'/resources/flavors/{args.id}', None, args)
    print_response(resp, args)


def flavor_group_list(args: Namespace):
    '''list flavors'''
    resp = api_request('get', '/resources/flavorgroups', None, args)
    print_response(resp, args)


def flavor_group_show(args: Namespace):
    '''show the flavor group with the given id'''
    resp = api_request('get', f'/resources/flavorgroups/{args.id}', None, args)
    print_response(resp, args)


def flavor_group_create(args: Namespace):
    '''create a flavor group'''
    data = {
        "name": args.name,
        "flavors": [],
    }
    print(data)
    resp = api_request('post', '/resources/flavorgroups/', data, args)
    print_response(resp, args)


def flavor_group_modify(args: Namespace):
    '''modify the flavor group with the given id'''
    # TODO
    pass


def flavor_group_delete(args: Namespace):
    '''delete the flavor group with the given id'''
    resp = api_request('delete', f'/resources/flavorgroups/{args.id}', None, args)
    print_response(resp, args)
