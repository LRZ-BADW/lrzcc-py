from argparse import _SubParsersAction, ArgumentParser, Namespace
import urllib.parse
from datetime import datetime

from common import (do_nothing, print_response, api_request, valid_datetime,
                    parse_user, parse_project, parse_flavor,
                    ask_for_confirmation, generate_modify_data)


cmds = ['project-budget', 'user-budget', 'budget-over-tree',
        'budget-bulk-create']
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
    project_budget_list_filter_group = \
        project_budget_list_parser.add_mutually_exclusive_group()
    project_budget_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all project budgets",
    )
    project_budget_list_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List project budgets for the user with the given name or ID",
    )
    project_budget_list_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List project budgets for the project with the given name or ID",
    )
    project_budget_list_parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="List project budgets for only the given year",
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

    # project budget modify parser
    project_budget_modify_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "modify",
            help="Modify project budget",
            )
    project_budget_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the project budget',
        )
    project_budget_modify_parser.add_argument(
        "-a",
        "--amount",
        type=int,
        help='New amount for the budget',
    )
    project_budget_modify_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help='Force the modification',
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

    # project budget over parser
    project_budget_over_parser: ArgumentParser = \
        project_budget_subparsers.add_parser(
            "over",
            help="Check if cost exceeds project budget",
        )
    project_budget_over_filter_group = \
        project_budget_over_parser.add_mutually_exclusive_group()
    project_budget_over_filter_group.add_argument(
        "-b",
        "--budget",
        type=int,
        help="Check if respective cost exceeds the budget with the given ID",
    )
    project_budget_over_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="Check project budgets for the project with the given name or ID",
    )
    project_budget_over_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all project budgets and if their exceeded",
    )
    project_budget_over_parser.add_argument(
        "-e",
        "--end",
        type=valid_datetime,
        help="""End up to which to calculate the over status, year is inferred
             from this value (default: current time)""",
    )
    project_budget_over_parser.add_argument(
        "-d",
        "--detail",
        action="store_true",
        help="Show cost and budget values as well",
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
    user_budget_list_filter_group = \
        user_budget_list_parser.add_mutually_exclusive_group()
    user_budget_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all user budgets",
    )
    user_budget_list_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="List user budgets for the user with the given name or ID",
    )
    user_budget_list_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List user budgets for the project with the given name or ID",
    )
    user_budget_list_parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="List user budgets for only the given year",
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

    # user budget modify parser
    user_budget_modify_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "modify",
            help="Modify user budget",
            )
    user_budget_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the user budget',
        )
    user_budget_modify_parser.add_argument(
        "-a",
        "--amount",
        type=int,
        help='New amount for the budget',
    )
    user_budget_modify_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help='Force the modification',
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

    # user budget over parser
    user_budget_over_parser: ArgumentParser = \
        user_budget_subparsers.add_parser(
            "over",
            help="Check if cost exceeds user budget",
        )
    user_budget_over_filter_group = \
        user_budget_over_parser.add_mutually_exclusive_group()
    user_budget_over_filter_group.add_argument(
        "-b",
        "--budget",
        type=int,
        help="Check if respective cost exceeds the budget with the given ID",
    )
    user_budget_over_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="Check user budgets for the user with the given name or ID",
    )
    user_budget_over_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="Check user budgets for the project with the given name or ID",
    )
    user_budget_over_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all user budgets and if their exceeded",
    )
    user_budget_over_parser.add_argument(
        "-e",
        "--end",
        type=valid_datetime,
        help="""End up to which to calculate the over status, year is inferred
             from this value (default: current time)""",
    )
    user_budget_over_parser.add_argument(
        "-c",
        "--combined",
        action="store_true",
        help="Combine over-budget status of user- and project budgets",
    )
    user_budget_over_parser.add_argument(
        "-d",
        "--detail",
        action="store_true",
        help="Show cost and budget values as well",
    )

    # budget over tree parser
    budget_over_tree_parser: ArgumentParser = main_subparsers.add_parser(
        "budget-over-tree",
        help="Get a hierarchical budget cost comparison",
        )
    parsers['budget-over-tree'] = budget_over_tree_parser
    budget_over_tree_filter_group = \
        budget_over_tree_parser.add_mutually_exclusive_group()
    budget_over_tree_filter_group.add_argument(
        "-u",
        "--user",
        type=str,
        help="Get budget over tree for user with the given name or ID",
    )
    budget_over_tree_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="Get budget over tree for the project with the given name or ID",
    )
    budget_over_tree_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Get budget over tree for entire system",
    )
    budget_over_tree_filter_group.add_argument(
        "-e",
        "--end",
        type=valid_datetime,
        help="""End up to which to calculate the over status, year is inferred
             from this value (default: current time)""",
    )

    # budget bulk create parser
    budget_bulk_create_parser: ArgumentParser = main_subparsers.add_parser(
        "budget-bulk-create",
        help="Bulk create user and project budgets",
        )
    parsers['budget-bulk-create'] = budget_bulk_create_parser
    budget_bulk_create_filter_group = \
        budget_bulk_create_parser.add_mutually_exclusive_group()
    budget_bulk_create_filter_group.add_argument(
        "-y",
        "--year",
        type=str,
        default=datetime.now().year,
        help="Year for the budget (default: current year)",
    )

    # avoid variable not used warnings

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
    if args.all:
        params += '?all=True'
    elif args.user:
        params += f'?user={args.user}'
    elif args.project:
        params += f'?project={args.project}'
    if args.year:
        params += f'&year={args.year}'
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


def project_budget_modify(args: Namespace):
    '''modify the project budget with the given id'''
    params = ""
    if args.force:
        params += '?force=True'
    data = generate_modify_data(args,
                                [('amount', int, 'amount'),
                                 ])
    resp = api_request('patch',
                       f'/budgeting/projectbudgets/{args.id}/{params}',
                       data, args)
    print_response(resp, args)


def project_budget_over(args: Namespace):
    '''check if cost exceeds project budget'''
    params = ""
    if args.all:
        params += '&all=True'
    elif args.project:
        params += f'&project={args.project}'
    elif args.budget:
        params += f'&budget={args.budget}'
    if args.end:
        params += f"&end={urllib.parse.quote(args.end)}"
    if args.detail:
        params += '&detail=True'
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/budgeting/projectbudgets/over/{params}',
                       None, args)
    print_response(resp, args)


def user_budget_list(args: Namespace):
    '''list user budgets'''
    params = ""
    if args.all:
        params += '?all=True'
    elif args.user:
        params += f'?user={args.user}'
    elif args.project:
        params += f'?project={args.project}'
    if args.year:
        params += f'&year={args.year}'
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


def user_budget_modify(args: Namespace):
    '''modify the user budget with the given id'''
    params = ""
    if args.force:
        params += '?force=True'
    data = generate_modify_data(args,
                                [('amount', int, 'amount'),
                                 ])
    resp = api_request('patch', f'/budgeting/userbudgets/{args.id}/{params}',
                       data, args)
    print_response(resp, args)


def user_budget_over(args: Namespace):
    '''check if cost exceeds project budget'''
    params = ""
    if args.all:
        params += '&all=True'
    elif args.project:
        params += f'&project={args.project}'
    elif args.user:
        params += f'&user={args.user}'
    elif args.budget:
        params += f'&budget={args.budget}'
    if args.end:
        params += f"&end={urllib.parse.quote(args.end)}"
    if args.detail:
        params += '&detail=True'
    if args.combined:
        params += '&combined=True'
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/budgeting/userbudgets/over/{params}',
                       None, args)
    print_response(resp, args)


def budget_over_tree(args: Namespace):
    '''get a hierarchical budget cost comparison'''
    params = ""
    if args.user:
        params += f'?user={args.user}'
    elif args.project:
        params += f'?project={args.project}'
    elif args.all:
        params += '?all=True'
    if args.end:
        params += f"&end={urllib.parse.quote(args.end)}"
    if params:
        params = '?' + params[1:]
    resp = api_request('get', f'/budgeting/budgetovertree/{params}',
                       None, args)
    print_response(resp, args)


def budget_bulk_create(args: Namespace):
    '''bulk create user and project budgets'''
    data = {
        "year": args.year,
    }
    resp = api_request('post', '/budgeting/budgetbulkcreate/', data, args)
    print_response(resp, args)
