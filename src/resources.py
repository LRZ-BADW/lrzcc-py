from argparse import _SubParsersAction, ArgumentParser, Namespace
from datetime import datetime
import sys

from common import (do_nothing, print_response, api_request, valid_datetime,
                    parse_flavor, parse_flavor_group, generate_modify_data,
                    parse_user, parse_project)

cmds = ['flavor', 'flavor-group', 'usage']
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
    flavor_list_filter_group = \
        flavor_list_parser.add_mutually_exclusive_group()
    flavor_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all flavors",
    )
    flavor_list_filter_group.add_argument(
        "-g",
        "--group",
        type=str,
        help="List flavors of the flavor group specified by name or ID",
    )

    # flavor show parser
    flavor_show_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "show",
            help="Show a flavor",
            )
    flavor_show_parser.add_argument(
        "flavor",
        type=str,
        help='Name or ID of the flavor',
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
    flavor_create_parser.add_argument(
        "--group",
        "-g",
        type=str,
        help="Name or ID of the flavor group",
    )
    flavor_create_parser.add_argument(
        "--weight",
        "-w",
        type=int,
        help="Weight of flavor within it's group",
    )

    # flavor delete parser
    flavor_delete_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "delete",
            help="Delete a flavor",
            )
    flavor_delete_parser.add_argument(
        "flavor",
        type=str,
        help='Name or ID of the flavor',
        )

    # flavor modify parser
    flavor_modify_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "modify",
            help="Modify a flavor",
            )
    flavor_modify_parser.add_argument(
        "flavor",
        type=str,
        help='Name or ID of the flavor',
        )
    flavor_modify_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="New name for the flavor",
    )
    flavor_modify_group_group = \
        flavor_modify_parser.add_mutually_exclusive_group()
    flavor_modify_group_group.add_argument(
        "-g",
        "--group",
        type=str,
        help="Name or ID of the new flavor group",
    )
    flavor_modify_group_group.add_argument(
        "-G",
        "--nogroup",
        action='store_true',
        help="Remove the flavor from its group",
    )
    flavor_modify_parser.add_argument(
        "-w",
        "--weight",
        type=int,
        help="New weight within the respective flavor group",
    )

    # flavor import parser
    flavor_import_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "import",
            help="Import flavors from OpenStack API",
            )
    flavor_import_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Don't print anything, when nothing is imported",
    )

    # flavor usage parser
    flavor_usage_parser: ArgumentParser = \
        flavor_subparsers.add_parser(
            "usage",
            help="List the flavor usage",
            )
    flavor_usage_filter_group = \
        flavor_usage_parser.add_mutually_exclusive_group()
    flavor_usage_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List flavor usage for all users",
    )
    flavor_usage_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List flavor usage for user specified by name or ID",
    )
    flavor_usage_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List flavor usage for the users of the project specified by " +
             "name or ID",
    )
    flavor_usage_parser.add_argument(
        "-A",
        "--aggregate",
        action="store_true",
        help="Aggregate the flavor usage for all filtered users",
    )

    # flavor group list parser
    flavor_group_list_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "list",
            help="List flavors",
            )
    flavor_group_list_filter_group = \
        flavor_group_list_parser.add_mutually_exclusive_group()
    flavor_group_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all flavor groups",
    )

    # flavor group show parser
    flavor_group_show_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "show",
            help="Show a flavor group",
            )
    flavor_group_show_parser.add_argument(
        "group",
        type=str,
        help='Name or ID of the flavor group',
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
        "group",
        type=str,
        help='Name or ID of the flavor group',
        )

    # flavor group modify parser
    flavor_group_modify_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "modify",
            help="Modify a flavor group",
            )
    flavor_group_modify_parser.add_argument(
        "group",
        type=str,
        help='Name or ID of the flavor group',
        )
    flavor_group_modify_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="New name for the flavor group",
    )

    # flavor group initialize parser
    flavor_group_initialize_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "initialize",
            help="Initialize the default flavor groups",
            )

    # flavor group usage parser
    flavor_group_usage_parser: ArgumentParser = \
        flavor_group_subparsers.add_parser(
            "usage",
            help="List the flavor group usage",
            )
    flavor_group_usage_filter_group = \
        flavor_group_usage_parser.add_mutually_exclusive_group()
    flavor_group_usage_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List flavor group usage for all users",
    )
    flavor_group_usage_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List flavor group usage for user specified by name or ID",
    )
    flavor_group_usage_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List flavor group usage for users of the project specified by" +
             " name or ID",
    )
    flavor_group_usage_parser.add_argument(
        "-A",
        "--aggregate",
        action="store_true",
        help="Aggregate the flavor usage for all filtered users",
    )

    # usage parser
    usage_parser: ArgumentParser = main_subparsers.add_parser(
        "usage",
        help="Show usage of the entire cloud",
        )
    parsers['usage'] = usage_parser

    # avoid variable not used warnings
    do_nothing(flavor_group_initialize_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line argument checks'''

    parse_flavor(args)
    parse_flavor_group(args)
    parse_user(args)
    parse_project(args)


def flavor_list(args: Namespace):
    '''list flavors'''
    params = ""
    if args.all:
        params += "?all=True"
    elif args.group:
        params += f"?flavorgroup={args.group}"
    resp = api_request('get', f'/resources/flavors/{params}', None, args)
    print_response(resp, args)


def flavor_show(args: Namespace):
    '''show the flavor with the given id'''
    resp = api_request('get', f'/resources/flavors/{args.flavor}', None, args)
    print_response(resp, args)


def flavor_create(args: Namespace):
    '''create a flavor'''
    data = {
        "name": args.name,
        # "group": None,
    }
    if args.group is not None:
        # TODO why do i need group_id here rather than group,
        #      because it works in user_create() with project
        data['group_id'] = args.group
    if args.weight is not None:
        data['weight'] = args.weight
    resp = api_request('post', '/resources/flavors/', data, args)
    print_response(resp, args)


def flavor_modify(args: Namespace):
    '''modify the flavor with the given id'''
    data = generate_modify_data(args,
                                [('name', str, 'name'),
                                 ('group', int, 'group'),
                                 ('weight', int, 'weight'),
                                 ])
    resp = api_request('patch', f'/resources/flavors/{args.flavor}/', data,
                       args)
    print_response(resp, args)


def flavor_delete(args: Namespace):
    '''delete the flavor with the given id'''
    resp = api_request('delete', f'/resources/flavors/{args.flavor}', None,
                       args)
    print_response(resp, args)


def flavor_import(args: Namespace):
    '''import all the flavors from the OpenStack API'''
    resp = api_request('get', '/resources/flavors/import/', None, args)
    resp_json = resp.json()
    if (
        args.quiet
        and not
        ('new_flavor_count' in resp_json and resp_json['new_flavor_count'])
    ):
        return
    print_response(resp, args)


def flavor_usage(args: Namespace):
    '''list the flavor usage'''
    params = ""
    if args.all:
        params += "&all=True"
    elif args.user:
        params += f"&user={args.user}"
    elif args.project:
        params += f"&project={args.project}"
    if args.aggregate:
        params += "&aggregate=True"
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/resources/flavors/usage/{params}', None, args)
    print_response(resp, args)


def flavor_group_list(args: Namespace):
    '''list flavors'''
    params = ""
    if args.all:
        params += "?all=True"
    resp = api_request('get', f'/resources/flavorgroups/{params}', None, args)
    print_response(resp, args)


def flavor_group_show(args: Namespace):
    '''show the flavor group with the given id'''
    resp = api_request('get', f'/resources/flavorgroups/{args.group}', None,
                       args)
    print_response(resp, args)


def flavor_group_create(args: Namespace):
    '''create a flavor group'''
    data = {
        "name": args.name,
        "flavors": [],
    }
    resp = api_request('post', '/resources/flavorgroups/', data, args)
    print_response(resp, args)


def flavor_group_modify(args: Namespace):
    '''modify the flavor group with the given id'''
    data = generate_modify_data(args,
                                [('name', str, 'name'),
                                 ])
    resp = api_request('patch', f'/resources/flavorgroups/{args.group}/', data,
                       args)
    print_response(resp, args)


def flavor_group_delete(args: Namespace):
    '''delete the flavor group with the given id'''
    resp = api_request('delete', f'/resources/flavorgroups/{args.group}', None,
                       args)
    print_response(resp, args)


def flavor_group_initialize(args: Namespace):
    '''initialize the default flavor groups'''
    resp = api_request('get', '/resources/flavorgroups/initialize/', None,
                       args)
    print_response(resp, args)


def flavor_group_usage(args: Namespace):
    '''list the flavor group usage'''
    params = ""
    if args.all:
        params += "&all=True"
    elif args.user:
        params += f"&user={args.user}"
    elif args.project:
        params += f"&project={args.project}"
    if args.aggregate:
        params += "&aggregate=True"
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/resources/flavorgroups/usage/{params}', None,
                       args)
    print_response(resp, args)


def usage(args: Namespace):
    '''show usage of the entire cloud'''
    resp = api_request('get', '/resources/usage/', None, args)
    print_response(resp, args)
