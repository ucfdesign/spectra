import os
import json
from spectra.core.transform.roster import Roster


def build_new_section_parser(parser):
    parser.set_defaults(func=new_section_handler)
    parser.add_argument('-r', '--roster', required=True, help="The roster.csv file from Canvas.")
    parser.add_argument('-s', '--section', required=True, help="The section ID/name.")


def new_section_handler(args):
    print('Creating new section ...')
    roster = Roster(args.roster)
    dirname = f'spectra-data/{args.section}'
    os.makedirs(dirname)
    with open(f'{dirname}/roster.json', 'w') as f:
        f.write(json.dumps(roster.to_dict(), sort_keys=True, indent=4))

    os.makedirs(os.path.join(dirname, 'data'))
    os.makedirs(os.path.join(dirname, 'outputs'))

    