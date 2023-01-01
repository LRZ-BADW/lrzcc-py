from argparse import _SubParsersAction, ArgumentParser, Namespace

from common import (do_nothing, print_response, api_request, valid_datetime,
                    parse_user, parse_project, parse_flavor)


cmds = ['server-action', 'flavor-consumption']
cmds_with_sub_cmds = ['server-action']


def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the accounting parser'''
    parsers = {}

    # server action parser
    server_action_parser: ArgumentParser = main_subparsers.add_parser(
        "server-action",
        help="server action commands",
        )
    parsers['server-action'] = server_action_parser
    server_action_subparsers: _SubParsersAction = \
        server_action_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # server action list parser
    server_action_list_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "list",
            help="List server actions",
            )
    server_action_list_filter_group = \
        server_action_list_parser.add_mutually_exclusive_group()
    server_action_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all server actions",
    )
    server_action_list_filter_group.add_argument(
        # TODO we could validate that this is UUIDv4
        "-s",
        "--server",
        type=str,
        help="List server actions for the server with the given UUID",
    )
    server_action_list_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List server actions for the user with the given name or ID",
    )
    server_action_list_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List server actions for the project with the given name or ID",
    )

    # server action show parser
    server_action_show_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "show",
            help="Show a server action",
            )
    server_action_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the server action',
        )

    # server action create parser
    server_action_create_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "create",
            help="Create a server action",
            )
    server_action_create_parser.add_argument(
        "acc_db_id",
        type=int,
        help="ID of the corresponding row in the accounting table",
    )
    server_action_create_parser.add_argument(
        "action_id",
        type=int,
        help="ID of the action",
    )
    server_action_create_parser.add_argument(
        "deleted",
        type=int,
        help="1 when instance action was deleted, 0 otherwise",
    )
    server_action_create_parser.add_argument(
        "created_at",
        type=valid_datetime,
        help="datetime when the action was created",
    )
    server_action_create_parser.add_argument(
        "updated_at",
        type=valid_datetime,
        help="datetime when the action was last updated",
    )
    server_action_create_parser.add_argument(
        "deleted_at",
        type=valid_datetime,
        help="datetime when the action was last deleted",
    )
    server_action_create_parser.add_argument(
        "create_triggered_at",
        type=valid_datetime,
        help="datetime when the create trigger was invoked",
    )
    server_action_create_parser.add_argument(
        "instance_id",
        # TODO maybe validate UUIDs too
        type=str,
        help="UUID of the instance",
    )
    server_action_create_parser.add_argument(
        "instance_name",
        type=str,
        help="name of the instance",
    )
    server_action_create_parser.add_argument(
        "instance_state",
        type=str,
        help="state of the instance",
    )
    server_action_create_parser.add_argument(
        "project_id",
        type=str,
        help="ID of the OpenStack project the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "project_name",
        type=str,
        help="name of the OpenStack project the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "domain_id",
        type=str,
        help="ID of the OpenStack domain the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "domain_name",
        type=str,
        help="name of the OpenStack domain the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "flavor",
        type=str,
        help="Name or ID of the flavor the instance, matches either flavor_new"
             " or flavor_old",
    )
    server_action_create_parser.add_argument(
        "flavor_new",
        type=str,
        help="Name or ID of the flavor the instance had after the action",
    )
    server_action_create_parser.add_argument(
        "flavor_old",
        type=str,
        help="Name or ID of the flavor the instance had before the action",
    )
    server_action_create_parser.add_argument(
        "action",
        # TODO should be restricted to the specific actions available
        type=str,
        help="the action done to the instance",
    )
    server_action_create_parser.add_argument(
        "request_id",
        type=str,
        help="ID of the request that issued the action",
    )
    server_action_create_parser.add_argument(
        "request_project_id",
        type=str,
        help="ID of the OpenStack project that invoked the request that "
             "issued this action",
    )
    server_action_create_parser.add_argument(
        "request_user_id",
        type=str,
        help="ID of the OpenStack user that invoked the request that "
             "issued this action",
    )
    server_action_create_parser.add_argument(
        "start_time",
        type=valid_datetime,
        help="datetime when the action started",
    )
    server_action_create_parser.add_argument(
        "finish_time",
        type=valid_datetime,
        help="datetime when the action was finished",
    )
    server_action_create_parser.add_argument(
        "message",
        type=str,
        help="optional message on the action",
    )

    # server action delete parser
    server_action_delete_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "delete",
            help="Delete a server action",
            )
    server_action_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the server action',
        )

    # server action modify parser
    server_action_modify_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "modify",
            help="Modify a server action",
            )
    server_action_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the server action',
        )

    # server action import parser
    server_action_import_parser: ArgumentParser = \
        server_action_subparsers.add_parser(
            "import",
            help="Import server actions from OpenStack database",
            )
    server_action_import_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Don't print anything, when nothing is imported",
    )

    # flavor consumption parser
    flavor_consumption_parser: ArgumentParser = \
        main_subparsers.add_parser(
            "flavor-consumption",
            help="Calculate flavor consumption over time",
            )
    flavor_consumption_parser.add_argument(
        "-b",
        "--begin",
        type=valid_datetime,
        help="Begin of the period to calculate the consumption for",
    )
    flavor_consumption_parser.add_argument(
        "-e",
        "--end",
        type=valid_datetime,
        help="End of the period to calculate the consumption for",
    )
    flavor_consumption_parser.add_argument(
        "-d",
        "--detail",
        action="store_true",
        help="Also retrieve the detailed consumption log",
    )
    flavor_consumption_filter_group = \
        flavor_consumption_parser.add_mutually_exclusive_group()
    flavor_consumption_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Calculate flavor consumption for all users",
    )
    flavor_consumption_filter_group.add_argument(
        "-s",
        "--server",
        type=str,
        help="Calculate flavor consumption for server with specified UUID",
    )
    flavor_consumption_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="Calculate flavor consumption for user specified by name or ID",
    )
    flavor_consumption_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="Calculate flavor consumption for the users of the project " +
             "specified by name or ID",
    )

    # avoid variable not used warnings
    do_nothing(server_action_list_parser)
    do_nothing(server_action_create_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line argument checks'''

    parse_user(args)
    parse_project(args)

    # TODO this is not very efficient, because it's going to make the same
    #      API request three times, so we should change the parse functions
    #      to take a list of argument names
    parse_flavor(args)
    parse_flavor(args, 'flavor_new')
    parse_flavor(args, 'flavor_old')


def server_action_list(args: Namespace):
    '''list server actions'''
    params = ""
    if args.all:
        params += '?all=True'
    elif args.server:
        params += f'?server={args.server}'
    elif args.user:
        params += f'?user={args.user}'
    elif args.project:
        params += f'?project={args.project}'
    resp = api_request('get', f'/accounting/serveractions/{params}',
                       None, args)
    print_response(resp, args)


def server_action_show(args: Namespace):
    '''show the server action with a given id'''
    resp = api_request('get', f'/accounting/serveractions/{args.id}', None,
                       args)
    print_response(resp, args)


def server_action_create(args: Namespace):
    '''create a server action'''
    data = {
        "acc_db_id": args.acc_db_id,
        "action_id": args.action_id,
        "deleted": args.deleted,
        "created_at": args.created_at,
        "updated_at": args.updated_at,
        "deleted_at": args.deleted_at,
        "create_triggered_at": args.create_triggered_at,
        "instance_id": args.instance_id,
        "instance_name": args.instance_name,
        "instance_state": args.instance_state,
        "project_id": args.project_id,
        "project_name": args.project_name,
        "domain_id": args.domain_id,
        "domain_name": args.domain_name,
        "flavor": args.flavor,
        "flavor_new": args.flavor_new,
        "flavor_old": args.flavor_old,
        "action": args.action,
        "request_id": args.request_id,
        "request_project_id": args.request_project_id,
        "request_user_id": args.request_user_id,
        "start_time": args.start_time,
        "finish_time": args.finish_time,
        "message": args.message,
    }
    resp = api_request('post', '/accounting/serveractions/', data, args)
    print_response(resp, args)


def server_action_modify(args: Namespace):
    '''modify the server action with the given id'''
    # TODO
    pass


def server_action_delete(args: Namespace):
    '''delete the server action with the given id'''
    resp = api_request('delete', f'/accounting/serveractions/{args.id}', None,
                       args)
    print_response(resp, args)


def server_action_import(args: Namespace):
    '''import all the server actions from the OpenStack database'''
    resp = api_request('get', '/accounting/serveractions/import/', None, args)
    resp_json = resp.json()
    if (
        args.quiet
        and not
        ('new_server_action_count' in resp_json
         and resp_json['new_server_action_count'])
    ):
        return
    print_response(resp, args)


def flavor_consumption(args: Namespace):
    '''Calculate the flavor consumption'''
    params = ""
    if args.begin:
        params += f"&begin={args.begin}"
    if args.end:
        params += f"&end={args.end}"
    if args.detail:
        params += "&detail=True"
    if args.all:
        params += "&all=True"
    elif args.server:
        params += f"&server={args.server}"
    elif args.user:
        params += f"&user={args.user}"
    elif args.project:
        params += f"&project={args.project}"
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/accounting/flavorconsumption/{params}',
                       None, args)
    print_response(resp, args)


