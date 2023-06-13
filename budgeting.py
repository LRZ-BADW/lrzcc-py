from argparse import _SubParsersAction, ArgumentParser, Namespace
import urllib.parse
from datetime import datetime

from common import (do_nothing, print_response, api_request, valid_datetime,
                    parse_user, parse_project, parse_flavor,
                    ask_for_confirmation, generate_modify_data)


cmds = ['project-budget', 'user-budget']
cmds_with_sub_cmds = ['project-budget', 'user-budget']
dangerous_cmds = {'project-budget': ['delete'],
                  'user-budget': ['delete'],
                  }


def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the accounting parser'''
    parsers = {}

    # project budget parser
    project_budget_parser: ArgumentParser = main_subparsers.add_parser(
        "project-budget",
        help="project budget commands",
        )
    parsers['project-budget'] = project_budget_parser
    project_budget_subparsers: _SubParsersAction = \
        project_budget_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # project budget list parser
    project_budget_list_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "list",
            help="List project budgets",
            )

    # project budget show parser
    project_budget_show_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "show",
            help="Show project budget",
            )
    project_budget_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the project budget',
        )

    # project budget create parser
    project_budget_create_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "create",
            help="Create project budget",
            )
    project_budget_create_parser.add_argument(
        "project",
        type=str,
        help='Project name or ID',
    )
    project_budget_create_parser.add_argument(
        "-y",
        "--year",
        type=int,
        help='Year for the budget (default: current year)',
        default=datetime.now().year,
    )
    project_budget_create_parser.add_argument(
        "-a",
        "--amount",
        type=int,
        help='Amount for the budget (default: 0)',
        default=0,
    )

    # project budget delete parser
    project_budget_delete_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "delete",
            help="Delete project budget",
            )
    project_budget_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the project budget',
        )

    # user budget parser
    user_budget_parser: ArgumentParser = main_subparsers.add_parser(
        "user-budget",
        help="user budget commands",
        )
    parsers['user-budget'] = user_budget_parser
    user_budget_subparsers: _SubParsersAction = \
        user_budget_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # user budget list parser
    user_budget_list_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "list",
            help="List user budgets",
            )

    # user budget show parser
    user_budget_show_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "show",
            help="Show user budget",
            )
    user_budget_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the user budget',
        )

    # user budget create parser
    user_budget_create_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "create",
            help="Create user budget",
            )
    user_budget_create_parser.add_argument(
        "user",
        type=str,
        help='User name or ID',
    )
    user_budget_create_parser.add_argument(
        "-y",
        "--year",
        type=int,
        help='Year for the budget (default: current year)',
        default=datetime.now().year,
    )
    user_budget_create_parser.add_argument(
        "-a",
        "--amount",
        type=int,
        help='Amount for the budget (default: 0)',
        default=0,
    )

    # user budget delete parser
    user_budget_delete_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "delete",
            help="Delete user budget",
            )
    user_budget_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the user budget',
        )

    # avoid variable not used warnings
    do_nothing(project_budget_list_parser)
    do_nothing(user_budget_list_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line argument checks'''

    parse_user(args)
    parse_project(args)

    if (args.command in dangerous_cmds and args.sub_command
            and args.sub_command in dangerous_cmds[args.command]):
        ask_for_confirmation()


def project_budget_list(args: Namespace):
    '''list project budgets'''
    params = ""
    resp = api_request('get', f'/budgeting/projectbudgets/{params}',
                       None, args)
    print_response(resp, args)


def project_budget_show(args: Namespace):
    '''show project budget with the given ID'''
    resp = api_request('get', f'/budgeting/projectbudgets/{args.id}',
                       None, args)
    print_response(resp, args)


def project_budget_delete(args: Namespace):
    '''delete project budget with the given ID'''
    resp = api_request('delete', f'/budgeting/projectbudgets/{args.id}',
                       None, args)
    print_response(resp, args)


def project_budget_create(args: Namespace):
    '''create a project budget'''
    data = {
        "project": args.project,
        "year": args.year,
        "amount": args.amount,
    }
    resp = api_request('post', '/budgeting/projectbudgets/', data, args)
    print_response(resp, args)


def user_budget_list(args: Namespace):
    '''list user budgets'''
    params = ""
    resp = api_request('get', f'/budgeting/userbudgets/{params}',
                       None, args)
    print_response(resp, args)


def user_budget_show(args: Namespace):
    '''show user budget with the given ID'''
    resp = api_request('get', f'/budgeting/userbudgets/{args.id}',
                       None, args)
    print_response(resp, args)


def user_budget_create(args: Namespace):
    '''create a user budget'''
    data = {
        "user": args.user,
        "year": args.year,
        "amount": args.amount,
    }
    resp = api_request('post', '/budgeting/userbudgets/', data, args)
    print_response(resp, args)


def user_budget_delete(args: Namespace):
    '''delete user budget with the given ID'''
    resp = api_request('delete', f'/budgeting/userbudgets/{args.id}',
                       None, args)
    print_response(resp, args)
