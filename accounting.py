from argparse import _SubParsersAction, ArgumentParser, Namespace

from common import do_nothing, print_response, api_request


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
        required=True,
        help="ID of the corresponding row in the accounting table",
    )
    server_action_create_parser.add_argument(
        "action_id",
        type=int,
        required=True,
        help="ID of the action",
    )
    server_action_create_parser.add_argument(
        "deleted",
        type=int,
        required=True,
        help="1 when instance action was deleted, 0 otherwise",
    )
    server_action_create_parser.add_argument(
        "created_at",
        type=valid_datetime,
        required=True,
        help="datetime when the action was created",
    )
    server_action_create_parser.add_argument(
        "updated_at",
        type=valid_datetime,
        required=True,
        help="datetime when the action was last updated",
    )
    server_action_create_parser.add_argument(
        "deleted_at",
        type=valid_datetime,
        required=True,
        help="datetime when the action was last deleted",
    )
    server_action_create_parser.add_argument(
        "create_triggered_at",
        type=valid_datetime,
        required=True,
        help="datetime when the create trigger was invoked",
    )
    server_action_create_parser.add_argument(
        "instance_id",
        # TODO maybe validate UUIDs too
        type=str,
        required=True,
        help="UUID of the instance",
    )
    server_action_create_parser.add_argument(
        "instance_name",
        type=str,
        required=True,
        help="name of the instance",
    )
    server_action_create_parser.add_argument(
        "instance_state",
        type=str,
        required=True,
        help="state of the instance",
    )
    server_action_create_parser.add_argument(
        "project_id",
        type=str,
        required=True,
        help="ID of the OpenStack project the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "project_name",
        type=str,
        required=True,
        help="name of the OpenStack project the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "domain_id",
        type=str,
        required=True,
        help="ID of the OpenStack domain the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "domain_name",
        type=str,
        required=True,
        help="name of the OpenStack domain the instance belongs to",
    )
    server_action_create_parser.add_argument(
        "flavor",
        # TODO use valid_flavor() once that's created
        type=str,
        required=True,
        help="name of the flavor the instance, matches either flavor_new or "
             "flavor_old",
    )
    server_action_create_parser.add_argument(
        "flavor_new",
        # TODO use valid_flavor() once that's created
        type=str,
        required=True,
        help="name of the flavor the instance had after the action",
    )
    server_action_create_parser.add_argument(
        "flavor_old",
        # TODO use valid_flavor() once that's created
        type=str,
        required=True,
        help="name of the flavor the instance had before the action",
    )
    server_action_create_parser.add_argument(
        "action",
        # TODO should be restricted to the specific actions available
        type=str,
        required=True,
        help="the action done to the instance",
    )
    server_action_create_parser.add_argument(
        "request_id",
        type=str,
        required=True,
        help="ID of the request that issued the action",
    )
    server_action_create_parser.add_argument(
        "request_project_id",
        type=str,
        required=True,
        help="ID of the OpenStack project that invoked the request that "
             "issued this action",
    )
    server_action_create_parser.add_argument(
        "request_user_id",
        type=str,
        required=True,
        help="ID of the OpenStack user that invoked the request that "
             "issued this action",
    )
    server_action_create_parser.add_argument(
        "start_time",
        type=valid_datetime,
        required=True,
        help="datetime when the action started",
    )
    server_action_create_parser.add_argument(
        "finish_time",
        type=valid_datetime,
        required=True,
        help="datetime when the action was finished",
    )
    server_action_create_parser.add_argument(
        "message",
        type=str,
        required=True,
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

    # avoid variable not used warnings
    do_nothing(server_action_list_parser)
    do_nothing(server_action_create_parser)

    return parsers


def parse_args(args: Namespace):
    '''parse the command line arguments'''
    # TODO
    pass


def server_action_list(args: Namespace):
    '''list server actions'''
    resp = api_request('get', '/accountint/serveractions', None, args)
    print_response(resp, args)


def server_action_show(args: Namespace):
    '''show the server action with a given id'''
    resp = api_request('get', f'/accounting/serveractions/{args.id}', None,
                       args)
    print_response(resp, args)


def server_action_create(args: Namespace):
    '''create a server action'''
    # TODO
    pass


def server_action_modify(args: Namespace):
    '''modify the server action with the given id'''
    # TODO
    pass


def server_action_delete(args: Namespace):
    '''delete the server action with the given id'''
    # TODO
    pass
