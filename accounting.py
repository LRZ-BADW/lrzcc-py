from argparse import _SubParsersAction, ArgumentParser, Namespace
import requests


cmds_with_sub_cmds = ['server-action']


def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the accounting parser'''
    parsers = {}

    # server action parser
    server_action_parser: ArgumentParser = main_subparsers.add_parser(
        "server-action",
        help = "server action commands",
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
                    help = "List server actions",
                    )

    # server action show parser
    server_action_show_parser: ArgumentParser = \
            server_action_subparsers.add_parser(
                    "show",
                    help = "Show a server action",
                    )
    server_action_show_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the server action',
            )

    # server action create parser
    server_action_create_parser: ArgumentParser = \
            server_action_subparsers.add_parser(
                    "create",
                    help = "Create a server action",
                    )

    # server action delete parser
    server_action_delete_parser: ArgumentParser = \
            server_action_subparsers.add_parser(
                    "delete",
                    help = "Delete a server action",
                    )
    server_action_delete_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the server action',
            )

    # server action modify parser
    server_action_modify_parser: ArgumentParser = \
            server_action_subparsers.add_parser(
                    "modify",
                    help = "Modify a server action",
                    )
    server_action_modify_parser.add_argument(
            "id",
            type = int,
            help = 'ID of the server action',
            )

    return parsers


def parse_args(args: Namespace):
    '''parse the command line arguments'''
    # TODO
    pass


def server_action_list(args: Namespace):
    '''list server actions'''
    url = f'{args.url}/accounting/serveractions'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    resp = requests.get(url, headers=headers)
    print(resp.json())


def server_action_show(args: Namespace):
    '''show the server action with a given id'''
    # TODO
    pass


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
