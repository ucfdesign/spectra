import argparse 
from rich import print as rprint
from .ascii_art import get_logo

from spectra import version
from spectra.core.commands import init_command
from spectra.core.commands import new_command
from spectra.core.commands import transform_command
from spectra.core.commands import analyzer_command
from spectra.core import ingesters

def main():
    # Initialize the parser and subparsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar='sub-command', help='')

    # spectra help
    parser_help = subparsers.add_parser('help', help='Prints the help text')
    parser_help.set_defaults(parser=parser, func=print_help)

    # spectra version
    parser_version = subparsers.add_parser('version', help='Prints the spectra version')
    parser_version.set_defaults(func=print_version)

    # spectra info
    parser_info = subparsers.add_parser('info', help='Pretty prints Specta info')
    parser_info.set_defaults(func=print_info)

    # spectra init
    parser_init = subparsers.add_parser('init', help="Initializes the current directory as a Spectra project")
    init_command.build_init_parser(parser_init)
    
    # spectra new 
    parser_new = subparsers.add_parser('new', help="Create new objects")
    new_command.build_new_parser(parser_new)

    # spectra ingest
    parser_ingest = subparsers.add_parser('ingest', help="Ingest data")
    ingesters.build_ingest_parser(parser_ingest)

    # spectra transform
    parser_transform = subparsers.add_parser('transform', help="Transform data")
    transform_command.build_transform_parser(parser_transform)

    # spectra analyze
    parser_analyze = subparsers.add_parser('analyze', help="Analyze data")
    analyzer_command.build_analyze_parser(parser_analyze)

    # Parse CLI args and execute default function
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        print_info(args)
        parser.print_help()
        exit()
    args.func(args)


def print_help(args):
    print_info(args)
    args.parser.print_help()
    exit()


def print_version(args):
    print(version)


def print_info(args):
    print('')
    rprint('[dim yellow bold]' + '-'*74 + '[/dim yellow bold]')
    logo = get_logo(
        'dim cyan bold', 
        'dim white bold', 
        'dim white bold', 
        'yellow bold', 
        'cyan bold',
        'dim white',
        'dim yellow bold'
    )
    logo = '[white]' + logo + '[/white]'
    rprint(logo)
    print('\n')
    rprint('[dim yellow bold]' + '-'*74 + '[/dim yellow bold]')
    print('')


if __name__ == '__main__':
    pass