"""Rest Helper program.

Usage:
  rest_helper.py -c <config_file> [-n <number> | --num=<number>]
  rest_helper.py -h | --help

Options:
  -h --help                                  Show this help message.
  -c=<config_file> --config=<config_file>    Configuration file (required).
  -n=<number> --num=<number>                 Specify a number. Default is 100.
"""
import itertools
import sys
import configparser
from docopt import docopt


RED = '\033[31m'
YELLOW = '\033[33m'
URLS = "Urls"
DATA = "Data"


class ParserError(Exception):
    pass


class SectionNotFoundException(Exception):
    pass


class BadUserInputError(Exception):
    pass


def print_error(message, color):
    color_reset = '\033[0m'
    sys.stderr.write(color + message + color_reset + '\n')


def generate_entries(config_file, limit):
    parser = configparser.ConfigParser()
    parser.read(config_file)

    sections = parser.sections()
    if not sections:
        raise ParserError
    if URLS not in sections or DATA not in sections:
        raise SectionNotFoundException

    url_path, user = get_config_data_values(parser)

    url_options = parser.options(URLS)
    for option in itertools.islice(url_options, limit):
        protocol, domain = parser.get(URLS, option).split('://')
        yield "{}://{}@{}{}".format(protocol, user, domain, url_path)


def get_config_data_values(parser):
    config_data = {}
    data_keys = parser.options(DATA)
    for key in data_keys:
        if parser.has_option(DATA, key):
            config_data[key] = parser.get(DATA, key)
    user, url_path = config_data.get("username") or "no_user", config_data.get("urlpath") or ""
    return url_path, user


def get_cli_input():
    args = docopt(__doc__)
    config_file, line_number = args.get('--config'), args.get('--num') or 100
    try:
        line_number = int(line_number)
    except ValueError:
        raise BadUserInputError()
    return config_file, line_number


def main():
    try:
        config_file, line_number = get_cli_input()
        entries = generate_entries(config_file=config_file, limit=int(line_number))
        print('\n'.join(str(entry) for entry in entries))
    except ParserError:
        print_error(message="Provided file: {} could not be parsed.".format(config_file), color=RED)
    except SectionNotFoundException:
        print_error(message="Required sections not found", color=YELLOW)
    except BadUserInputError:
        print_error(message="Argument for -n | --num could not be parsed. Please provide a number.", color=RED)
    except Exception as e:
        print_error(message="Unhandled exception: \n\t{}".format(e.__repr__()), color=RED)


if __name__ == '__main__':
    main()
