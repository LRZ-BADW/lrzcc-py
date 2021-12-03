import tabulate
import requests
import json
from datetime import datetime
from argparse import ArgumentError, Namespace
import sys
from pydoc import locate


def do_nothing(variable):
    '''just do nothing, this can be used to avoid wrongful linter warnings
    about unused variables'''
    pass


def print_response(resp, args):
    '''print an API response'''
    if not resp.content:
        return
    if type(resp.json()) == list:
        output = tabulate.tabulate(resp.json(), tablefmt=args.format)
    else:
        output = tabulate.tabulate(resp.json().items(), tablefmt=args.format)
    print(output)


def api_request(method, path, data, args):
    '''issue a request to the API and return the response'''
    url = f'{args.url}{path}'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    resp = requests.request(method, url, headers=headers,
                            data=json.dumps(data))
    return resp


def valid_datetime(string):
    try:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        msg = f"Not a valid datetime: {string}"
        raise ArgumentError(msg)


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


def api_list(entity: str, args: Namespace):
    path = list_paths[entity]
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


def search_flavor(string: str, args: Namespace):
    return search_entity('flavor', string, args)


def search_flavor_group(string: str, args: Namespace):
    return search_entity('flavor_group', string, args)


def search_project(string: str, args: Namespace):
    return search_entity('project', string, args)


def search_user(string: str, args: Namespace):
    return search_entity('user', string, args)


def parse_entity(entity: str, args: Namespace, argname: str = None):
    if not argname:
        argname = entity
    if argname in args and args.__dict__[argname]:
        obj = search_entity(entity, args.__dict__[argname], args)
        if not obj:
            print(f'{sys.argv[0]}: error: not a valid {entity}: ' +
                  f'{args.__dict__[argname]}', file=sys.stderr)
            exit(1)
        args.__dict__[argname] = obj['id']


def parse_flavor(args: Namespace, argname='flavor'):
    parse_entity('flavor', args, argname)


def parse_flavor_group(args: Namespace, argname='group'):
    parse_entity('flavor_group', args, argname)


def parse_project(args: Namespace):
    parse_entity('project', args)


def parse_user(args: Namespace):
    parse_entity('user', args)


def generate_modify_data(args: Namespace, fields):
    data = {}
    for fieldname, fieldtype, argname in fields:
        if argname in args and args.__dict__[argname]:
            data[fieldname] = fieldtype(args.__dict__[argname])
        if f'no{argname}' in args and args.__dict__[f'no{argname}']:
            data[fieldname] = None
    return data
