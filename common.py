import tabulate
import requests
import json


def do_nothing(variable):
    '''just do nothing, this can be used to avoid wrongful linter warnings
    about unused variables'''
    pass


def print_response(resp, args):
    '''print an API response'''
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
