import tabulate
import requests
import json
from datetime import datetime
from argparse import ArgumentError


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
    if string not in flavors:
        return string
    msg = f"Not a valid flavor: {string}. Valid choices are: {flavors}"
    raise ArgumentError(msg)
