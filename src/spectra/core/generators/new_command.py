import json
import os
from spectra.core.transform.roster import Roster

def build_new_parser(parser):
    #parser.add_argument('object', help='New thing to create')
    subparsers = parser.add_subparsers(help="Thing to create. Run 'spectra new <thing> --help' for additional information.")
    
    # spectra new 
    parser_new_section = subparsers.add_parser('section', help='Create a new section')
    build_new_section_parser(parser_new_section)
    parser.set_defaults(func=new_command_handler)


def new_command_handler(args):
    print("Invalid command. Run 'spectra new --help' for more info.")


def build_new_section_parser(parser):
    parser.set_defaults(func=new_section_handler)
    parser.add_argument('-r', '--roster', required=True, help="The roster.csv file from Canvas.")
    parser.add_argument('--name', required=True, help="The section name.")


def new_section_handler(args):
    print('Creating new section ...')
    roster = Roster(args.roster)
    dirname = f'.spectra-data/sections/{args.name}'
    os.makedirs(dirname)
    with open(f'{dirname}/roster.json', 'w') as f:
        f.write(json.dumps(roster.to_dict(), sort_keys=True, indent=4))

    