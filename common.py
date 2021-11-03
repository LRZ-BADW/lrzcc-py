import tabulate
import requests


def do_nothing(variable):
    pass


def print_response(resp, args):
    if type(resp.json()) == list:
        output = tabulate.tabulate(resp.json(), tablefmt=args.format)
    else:
        output = tabulate.tabulate(resp.json().items(), tablefmt=args.format)
    print(output)


def api_request(method, path, data, args):
    url = f'{args.url}{path}'
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': args.token}
    resp = requests.request(method, url, headers=headers, data=data)
    return resp
