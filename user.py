from argparse import _SubParsersAction, ArgumentParser, Namespace

from common import do_nothing, print_response, api_request


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

    # user show parser
    user_show_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "show",
            help="Show a user",
            )
    user_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the user',
        )

    # user create parser
    user_create_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "create",
            help="Create a user",
            )

    # user delete parser
    user_delete_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "delete",
            help="Delete a user",
            )
    user_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the user',
        )

    # user modify parser
    user_modify_parser: ArgumentParser = \
        user_subparsers.add_parser(
            "modify",
            help="Modify a user",
            )
    user_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the user',
        )

    # project list parser
    project_list_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "list",
            help="List projects",
            )

    # project show parser
    project_show_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "show",
            help="Show a project",
            )
    project_show_parser.add_argument(
        "id",
        type=int,
        help='ID of the project',
        )

    # project create parser
    project_create_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "create",
            help="Create a project",
            )

    # project delete parser
    project_delete_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "delete",
            help="Delete a project",
            )
    project_delete_parser.add_argument(
        "id",
        type=int,
        help='ID of the project',
        )

    # project modify parser
    project_modify_parser: ArgumentParser = \
        project_subparsers.add_parser(
            "modify",
            help="Modify a project",
            )
    project_modify_parser.add_argument(
        "id",
        type=int,
        help='ID of the project',
        )

    # avoid variable not used warnings
    common.do_nothing(user_list_parser)
    common.do_nothing(user_create_parser)
    common.do_nothing(project_list_parser)
    common.do_nothing(project_create_parser)

    return parsers


def parse_args(args: Namespace):
    '''parse the command line arguments'''
    # TODO
    pass


def user_list(args: Namespace):
    '''list users'''
    resp = api_request('get', '/user/users', None, args)
    print_response(resp, args)


def user_show(args: Namespace):
    '''show the user with the given id'''
    resp = api_request('get', f'/user/users/{args.id}', None, args)
    print_response(resp, args)


def user_create(args: Namespace):
    '''create a user'''
    # TODO
    pass


def user_modify(args: Namespace):
    '''modify the user with the given id'''
    # TODO
    pass


def user_delete(args: Namespace):
    '''delete the user with the given id'''
    # TODO
    pass


def project_list(args: Namespace):
    '''list projects'''
    resp = api_request('get', '/user/projects', None, args)
    print_response(resp, args)


def project_show(args: Namespace):
    '''show the project with the given id'''
    resp = api_request('get', f'/user/projects/{args.id}', None, args)
    print_response(resp, args)


def project_create(args: Namespace):
    '''create a project'''
    # TODO
    pass


def project_modify(args: Namespace):
    '''modify the project with the given id'''
    # TODO
    pass


def project_delete(args: Namespace):
    '''delete the project with the given id'''
    # TODO
    pass
