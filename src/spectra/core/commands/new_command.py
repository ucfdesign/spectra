from spectra.core.generators.section import build_new_section_parser
from spectra.core.generators.links import build_links_parser
from spectra.core.generators.raw_data import build_new_data_parser

def build_new_parser(parser):
    #parser.add_argument('object', help='New thing to create')
    subparsers = parser.add_subparsers(help="Thing to create. Run 'spectra new <thing> --help' for additional information.")
    parser.set_defaults(func=new_command_handler)

    # spectra new data
    parser_new_data = subparsers.add_parser('raw-data', help='Add new raw data to a project')
    build_new_data_parser(parser_new_data)

    # spectra new section
    parser_new_section = subparsers.add_parser('section', help='Create a new section')
    build_new_section_parser(parser_new_section)

    # spectra new links
    parser_survey_links = subparsers.add_parser('links', help='Makes survey links')
    build_links_parser(parser_survey_links)

    
def new_command_handler(args):
    print("Invalid command. Run 'spectra new --help' for more info.")



    