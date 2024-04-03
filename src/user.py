from argparse import _SubParsersAction, ArgumentParser, Namespace

from common import (do_nothing, print_response, api_request, parse_project,
                    parse_user, generate_modify_data)


cmds = ['user', 'project']
cmds_with_sub_cmds = ['user', 'project']


# TODO we should probably use type annotations everywhere, here I'm just using
# it, so that my editor can give me suggestions
def setup_parsers(main_subparsers: _SubParsersAction):
    '''setup the pricing parser'''
    parsers = {}

    # user parser
    user_parser: ArgumentParser = main_subparsers.add_parser(
            "user",
            help="user commands",
            )
    parsers['user'] = user_parser
    user_subparsers: _SubParsersAction = \
        user_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # project parser
    project_parser: ArgumentParser = main_subparsers.add_parser(
        "project",
        help="project commands",
        )
    parsers['project'] = project_parser
    project_subparsers: _SubParsersAction = \
        project_parser.add_subparsers(
            help="sub-commands",
            dest="sub_command",
            )

    # user list parser
    user_list_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "list",
            help="List users",
            )
    user_list_filter_group = user_list_parser.add_mutually_exclusive_group()
    user_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all users",
    )
    user_list_filter_group.add_argument(
        "-p",
        "--project",
        type=str,
        help="List users of the project specified by name or ID",
    )

    # user show parser
    user_show_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "show",
            help="Show a user",
            )
    user_show_parser.add_argument(
        "user",
        type=str,
        help='Name or ID of the user',
        )

    # user create parser
    user_create_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "create",
            help="Create a user",
            )
    user_create_parser.add_argument(
        "name",
        type=str,
        help="Name of the user",
    )
    user_create_parser.add_argument(
        "project",
        type=str,
        help="Project Name or ID",
    )
    user_create_parser.add_argument(
        "-r",
        "--role",
        type=str,
        choices=["user", "masteruser"],
        default="user",
        help="Role of the user within the project (default: user)",
    )
    user_create_parser.add_argument(
        "-s",
        "--staff",
        action="store_true",
        help="When the user is admin",
    )
    user_create_parser.add_argument(
        "-i",
        "--inactive",
        action="store_true",
        help="When the user is inactive",
    )

    # user delete parser
    user_delete_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "delete",
            help="Delete a user",
            )
    user_delete_parser.add_argument(
        "user",
        type=str,
        help='Name or ID of the user',
        )

    # user modify parser
    user_modify_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "modify",
            help="Modify a user",
            )
    user_modify_parser.add_argument(
        "user",
        type=str,
        help='Name or ID of the user',
        )
    user_modify_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="New name for the user",
    )
    user_modify_parser.add_argument(
        "-p",
        "--project",
        type=str,
        help="New project of the user",
    )
    user_modify_parser.add_argument(
        "-r",
        "--role",
        type=str,
        choices=["user", "masteruser"],
        help="New role of the user within the project",
    )
    user_modify_staff_group = \
        user_modify_parser.add_mutually_exclusive_group()
    user_modify_staff_group.add_argument(
        "-s",
        "--staff",
        dest="staff",
        action="store_true",
        default=None,
        help="Make the user staff",
    )
    user_modify_staff_group.add_argument(
        "-S",
        "--nostaff",
        dest="staff",
        action="store_false",
        default=None,
        help="Make user not-staff",
    )
    user_modify_active_group = \
        user_modify_parser.add_mutually_exclusive_group()
    user_modify_active_group.add_argument(
        "-a",
        "--active",
        dest="active",
        action="store_true",
        default=None,
        help="Activate the user",
    )
    user_modify_active_group.add_argument(
        "-i",
        "--inactive",
        dest="active",
        action="store_false",
        default=None,
        help="Deactivate the user",
    )

    # user import parser
    user_import_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "import",
            help="Import users and projects from OpenStack API",
            )
    user_import_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Don't print anything, when nothing is imported",
    )

    # user me parser
    user_me_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "me",
            help="Show your own user",
            )

    # project list parser
    project_list_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "list",
            help="List projects",
            )
    project_list_filter_group = \
        project_list_parser.add_mutually_exclusive_group()
    project_list_filter_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all projects",
    )
    project_list_parser.add_argument(
        "-u",
        "--user-class",
        type=int,
        choices=[0, 1, 2, 3, 4, 5, 6],
        help="List projects with the specified user class",
    )

    # project show parser
    project_show_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "show",
            help="Show a project",
            )
    project_show_parser.add_argument(
        "project",
        type=str,
        help='Name or ID of the project',
        )

    # project create parser
    project_create_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "create",
            help="Create a project",
            )
    project_create_parser.add_argument(
        "name",
        type=str,
        help='Name of the project',
    )
    project_create_parser.add_argument(
        "-u",
        "--user-class",
        type=int,
        choices=[0, 1, 2, 3, 4, 5, 6],
        default=1,
        help="User class of the project",
    )

    # project delete parser
    project_delete_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "delete",
            help="Delete a project",
            )
    project_delete_parser.add_argument(
        "project",
        type=str,
        help='Name or ID of the project',
        )

    # project modify parser
    project_modify_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "modify",
            help="Modify a project",
            )
    project_modify_parser.add_argument(
        "project",
        type=str,
        help='Name or ID of the project',
        )
    project_modify_parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="New name for the project",
    )
    project_modify_parser.add_argument(
        "-u",
        "--user-class",
        type=int,
        choices=[0, 1, 2, 3, 4, 5, 6],
        help="New user class of the project",
    )

    # avoid variable not used warnings
    do_nothing(user_list_parser)
    do_nothing(user_me_parser)
    do_nothing(project_list_parser)

    return parsers


def parse_args(args: Namespace):
    '''do custom command line argument checks'''

    parse_project(args)
    parse_user(args)


def user_list(args: Namespace):
    '''list users'''
    params = ""
    if args.all:
        params += "?all=True"
    elif args.project:
        params += f"?project={args.project}"
    resp = api_request('get', f'/user/users/{params}', None, args)
    print_response(resp, args)


def user_show(args: Namespace):
    '''show the user with the given id'''
    resp = api_request('get', f'/user/users/{args.user}', None, args)
    print_response(resp, args)


def user_create(args: Namespace):
    '''create a user'''
    data = {
        "name": args.name,
        "project": args.project,
        "role": 1 if args.role == 'user' else 2,
        "is_staff": args.staff,
        "is_active": not args.inactive,
    }
    resp = api_request('post', '/user/users/', data, args)
    print_response(resp, args)


def user_modify(args: Namespace):
    '''modify the user with the given id'''
    data = generate_modify_data(args,
                                [('name', str, 'name'),
                                 ('project', int, 'project'),
                                 ('is_staff', bool, 'staff'),
                                 ('is_active', bool, 'active'),
                                 ])
    if "role" in args and args.role:
        data["role"] = 1 if args.role == 'user' else 2
    resp = api_request('patch', f'/user/users/{args.user}/', data, args)
    print_response(resp, args)


def user_delete(args: Namespace):
    '''delete the user with the given id'''
    resp = api_request('delete', f'/user/users/{args.user}', None, args)
    print_response(resp, args)


def user_import(args: Namespace):
    '''Import users and projects from the OpenStack API'''
    resp = api_request('get', '/user/import/', None, args)
    resp_json = resp.json()
    if (
        args.quiet
        and not
        ('new_user_count' in resp_json and resp_json['new_user_count'])
        and not
        ('new_project_count' in resp_json
         and resp_json['new_project_count'])
    ):
        return
    print_response(resp, args)


def user_me(args: Namespace):
    '''show your own user'''
    resp = api_request('get', f'/user/me/', None, args)
    print_response(resp, args)


def project_list(args: Namespace):
    '''list projects'''
    params = ""
    if args.all:
        params += "?all=True"
    elif args.user_class:
        params += f"?userclass={args.user_class}"
    resp = api_request('get', f'/user/projects/{params}', None, args)
    print_response(resp, args)


def project_show(args: Namespace):
    '''show the project with the given id'''
    resp = api_request('get', f'/user/projects/{args.project}', None, args)
    print_response(resp, args)


def project_create(args: Namespace):
    '''create a project'''
    data = {
        "name": args.name,
        "user_class": args.user_class,
        "users": [],
    }
    resp = api_request('post', '/user/projects/', data, args)
    print_response(resp, args)


def project_modify(args: Namespace):
    '''modify the project with the given id'''
    data = generate_modify_data(args,
                                [('name', str, 'name'),
                                 ('user_class', int, 'user_class'),
                                 ])
    resp = api_request('patch', f'/user/projects/{args.project}/', data, args)
    print_response(resp, args)


def project_delete(args: Namespace):
    '''delete the project with the given id'''
    resp = api_request('delete', f'/user/projects/{args.project}', None, args)
    print_response(resp, args)
