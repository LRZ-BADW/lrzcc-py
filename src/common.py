import tabulate
import requests
from http import HTTPStatus
import json
from datetime import datetime
from pytz import timezone
from argparse import ArgumentError, Namespace
import sys
# from pydoc import locate


def do_nothing(variable):
    '''just do nothing, this can be used to avoid wrongful linter warnings
    about unused variables'''
    pass


def now_str():
    tz = timezone("Europe/Berlin")
    format = "%Y-%m-%dT%H:%M:%S%z"
    return datetime.now(tz).strftime(format)


def print_response(resp, args):
    '''print an API response'''
    if not resp.content:
        return
    if resp.status_code >= 400:
        content = resp.json()
        message = ': ' + content['msg'] if 'msg' in content else ''
        print(f"Error: {resp.status_code} {resp.reason}{message}",
              file=sys.stderr)
        sys.exit(1)
    if args.format == 'json':
        output = json.dumps(resp.json())
    elif type(resp.json()) == list:
        headers = {}
        if resp.json():
            headers = {key: key for key in resp.json()[0].keys()}
        output = tabulate.tabulate(resp.json(), tablefmt=args.format,
                                   headers=headers)
    else:
        output = tabulate.tabulate(resp.json().items(), tablefmt=args.format,
                                   headers=['name', 'value'])
    print(output)


def api_request(method, path, data, args):
    '''issue a request to the API and return the response'''
    url = f'{args.url}{path}'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    if args.impersonate and isinstance(args.impersonate, int):
        headers['X-Impersonate'] = str(args.impersonate)
    resp = requests.request(method, url, headers=headers,
                            data=json.dumps(data))
    return resp


def valid_datetime(string):
    try:
        # Example: 2023-08-11T11:25:47.583802+02:00
        datetime.strptime(string, "%Y-%m-%dT%H:%M:%S%z")
        return string
    except ValueError:
        msg = f"Not a valid datetime: {string}"
        raise ArgumentError(msg)


def valid_positive_integer(string):
    try:
        integer = int(string)
    except ValueError:
        msg = f"Not a valid positive integer: {string}"
        raise ArgumentError(msg)

    if integer <= 0:
        msg = f"Not a valid positive integer: {string}"
        raise ArgumentError(msg)

    return integer


def valid_flavor(string):
    # TODO rewrite this according to new flavor api
    flavors = [
        'tiny',
        'lrz.small',
        'lrz.medium',
        'lrz.large',
        'lrz.xlarge',
        'lrz.2xlarge',
        'lrz.4xlarge',
        'nvidia-v100.1',
        'nvidia-v100.2',
        'lrz.huge',
        'lrz.xhuge',
        'lrz.2xhuge',
        'lrz.4xhuge',
    ]
    if string in flavors:
        return flavors.index(string) + 1
    msg = f"Not a valid flavor: {string}. Valid choices are: {flavors}"
    raise ArgumentError(msg)


list_paths = {
    'flavor': '/resources/flavors/',
    'flavor_group': '/resources/flavorgroups/',
    'project': '/user/projects/',
    'user': '/user/users/',
}


def get_me(args: Namespace):
    resp = api_request('get', '/user/me/', None, args)
    user = resp.json()
    return user


def api_list(entity: str, args: Namespace):
    params = ''
    me = get_me(args)
    if me['is_staff']:
        params += '?all=True'
    elif entity == 'user' and me['role'] == 2:
        params += f"?project={me['project']['id']}"
    path = f'{list_paths[entity]}{params}'
    resp = api_request('get', path, None, args)
    return resp.json()


def search_entity(entity: str, string: str, args: Namespace):
    # TODO Maybe in the future names won't be unique, so we have to deal with
    # situations where commands are ambiguous. Some form of listing from which
    # the user may choose would be pretty fancy.
    items = api_list(entity, args)

    for item in items:
        if ((not args.ids and item['name'] == string)
                or (not args.names and str(item['id']) == string)):
            return item

    return None

# TODO there are also entities without names like flavor quotas, a more
# elaborate function to search them by flavor group and user would be
# cool


def search_flavor(string: str, args: Namespace):
    return search_entity('flavor', string, args)


def search_flavor_group(string: str, args: Namespace):
    return search_entity('flavor_group', string, args)


def search_project(string: str, args: Namespace):
    return search_entity('project', string, args)


def search_user(string: str, args: Namespace):
    return search_entity('user', string, args)


def parse_entity(entity: str, args: Namespace, argname: str = None,
                 get_name=False):
    if not argname:
        argname = entity
    if argname in args and args.__dict__[argname]:
        obj = search_entity(entity, args.__dict__[argname], args)
        if not obj:
            print(f'{sys.argv[0]}: error: not a valid {entity}: ' +
                  f'{args.__dict__[argname]}', file=sys.stderr)
            exit(1)
        if get_name:
            args.__dict__[argname] = obj['name']
        else:
            args.__dict__[argname] = obj['id']


def parse_flavor(args: Namespace, argname='flavor', get_name=False):
    parse_entity('flavor', args, argname, get_name)


def parse_flavor_group(args: Namespace, argname='group', get_name=False):
    parse_entity('flavor_group', args, argname, get_name)


def parse_project(args: Namespace, argname='project', get_name=False):
    parse_entity('project', args, argname, get_name)


def parse_user(args: Namespace, argname='user', get_name=False):
    parse_entity('user', args, argname, get_name)


def generate_modify_data(args: Namespace, fields):
    data = {}
    for fieldname, fieldtype, argname in fields:
        if argname in args and args.__dict__[argname] is not None:
            data[fieldname] = fieldtype(args.__dict__[argname])
        if f'no{argname}' in args and args.__dict__[f'no{argname}']:
            data[fieldname] = None
    return data


def issue_api_token(keystone_url, username, password, user_domain_name,
                    project_name, project_domain_id):
    url = keystone_url + '/auth/tokens/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': username,
                        'domain': {'name': user_domain_name},
                        'password': password,
                    }
                }
            },
            'scope': {
                'project': {
                    'name': project_name,
                    'domain': {'id': project_domain_id}
                }
            }
        }
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code != HTTPStatus.CREATED:
        return None

    return resp.headers['X-Subject-Token']


def revoke_api_token(keystone_url, token):
    url = keystone_url + '/auth/tokens/'
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token,
        'X-Subject-Token': token,
    }

    resp = requests.delete(url, headers=headers)

    if resp.status_code != HTTPStatus.NO_CONTENT:
        return False

    return True


def ask_for_confirmation():
    expected = 'Yes, I really really mean it!'
    question = 'This command is potentially dangerous. Are you sure? ' + \
        f'Then type "{expected}" and press enter: '
    answer = input(question)
    if answer != expected:
        print('Aborting.')
        exit(1)
