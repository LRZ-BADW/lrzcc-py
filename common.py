import tabulate
import requests


def do_nothing(variable):
    pass


def print_response(resp, args):
    output = tabulate.tabulate(resp.json().items(), tablefmt=args.format)
    print(output)
