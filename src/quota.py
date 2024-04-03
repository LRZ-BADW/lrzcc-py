from argparse import _SubParsersAction, ArgumentParser, Namespace

from common import (do_nothing, print_response, api_request, parse_flavor,
                    parse_flavor_group, parse_user, generate_modify_data,
                    valid_positive_integer)


cmds = ['flavor-quota']
cmds_with_sub_cmds = ['flavor-quota']


# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the quota parser'''
    parsers = {}

    # flavor quota parser
    flavor_quota_parser: ArgumentParser = main_subparsers.add_parser(
        "flavor-quota",
        help="flavor quota commands",
        )
    parsers['flavor-quota'] = flavor_quota_parser
    flavor_quota_subparsers: _SubParsersAction = \
        flavor_quota_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # flavor quota list parser
    flavor_quota_list_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "list",
            help="List flavor quotas",
            )
    flavor_quota_list_filter_group = \
        flavor_quota_list_parser.add_mutually_exclusive_group()
    flavor_quota_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List flavor quotas of all users",
    )
    flavor_quota_list_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List flavor quotas for the user specified by name or ID",
    )
    flavor_quota_list_filter_group.add_argument(
        "-g",
        "--flavorgroup",
        type=str,
        help="List flavor quotas for the flavor group specified by name or ID",
    )

    # flavor quota show parser
    flavor_quota_show_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "show",
            help="Show a flavor quota",
            )
    flavor_quota_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor quota',
        )

    # flavor quota create parser
    flavor_quota_create_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "create",
            help="Create a flavor quota",
            )
    flavor_quota_create_parser.add_argument(
        "flavorgroup",
        type=str,
        help="Name or ID of the flavor group",
    )
    flavor_quota_create_parser.add_argument(
        "user",
        type=str,
        help="User name or ID",
    )
    flavor_quota_create_parser.add_argument(
        "-q",
        "--quota",
        type=int,
        help="Actual quota value (default: -1)",
        default=-1,
    )

    # flavor quota delete parser
    flavor_quota_delete_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "delete",
            help="Delete a flavor quota",
            )
    flavor_quota_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor quota',
        )

    # flavor quota modify parser
    flavor_quota_modify_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "modify",
            help="Modify a flavor quota",
            )
    flavor_quota_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the flavor quota',
        )
    flavor_quota_modify_parser.add_argument(
        "-q",
        "--quota",
        type=int,
        help="New quota value",
    )

    # flavor quota check parser
    flavor_quota_check_parser: ArgumentParser = \
        flavor_quota_subparsers.add_parser(
            "check",
            help="""Check if a user remains under the flavor quota, when a
            given count of the given flavor is added.""",
            )
    flavor_quota_check_parser.add_argument(
        "user",
        type=str,
        help="User name or ID",
    )
    flavor_quota_check_parser.add_argument(
        "flavor",
        type=str,
        help="Flavor name or ID",
    )
    flavor_quota_check_parser.add_argument(
        "-c",
        "--count",
        type=valid_positive_integer,
        default=1,
        help="Count of the flavor",
    )

    # avoid variable not used warnings
    do_nothing(flavor_quota_list_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line argument checks'''

    parse_flavor_group(args, 'flavorgroup')
    parse_user(args)
    parse_flavor(args)


def flavor_quota_list(args: Namespace):
    '''list flavor quotas'''
    params = ""
    if args.all:
        params += "?all=True"
    elif args.user:
        params += f"?user={args.user}"
    elif args.flavorgroup:
        params += f"?flavorgroup={args.flavorgroup}"
    url = f"/quota/flavorquotas{params}"
    resp = api_request('get', url, None, args)
    print_response(resp, args)


def flavor_quota_show(args: Namespace):
    '''show the flavor quota with the given id'''
    resp = api_request('get', f'/quota/flavorquotas/{args.id}', None, args)
    print_response(resp, args)


def flavor_quota_create(args: Namespace):
    '''create a flavor quota'''
    data = {
        "flavor_group": args.flavorgroup,
        "user": args.user,
        "quota": args.quota,
    }
    print(data)
    resp = api_request('post', '/quota/flavorquotas/', data, args)
    print_response(resp, args)


def flavor_quota_modify(args: Namespace):
    '''modify the flavor quota with the given id'''
    data = generate_modify_data(args,
                                [('quota', int, 'quota'),
                                 ])
    resp = api_request('patch', f'/quota/flavorquotas/{args.id}/', data, args)
    print_response(resp, args)


def flavor_quota_delete(args: Namespace):
    '''delete the flavor quota with the given id'''
    resp = api_request('delete', f'/quota/flavorquotas/{args.id}', None, args)
    print_response(resp, args)


def flavor_quota_check(args: Namespace):
    '''check if user remains under flavor quota'''
    params = f"?user={args.user}&flavor={args.flavor}" + \
        f"&flavorcount={args.count}"
    url = f"/quota/flavorquotas/check{params}"
    resp = api_request('get', url, None, args)
    print_response(resp, args)
