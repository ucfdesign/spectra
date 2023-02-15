

def build_new_data_parser(parser):
    #parser.add_argument('object', help='New thing to create')
    subparsers = parser.add_subparsers(help="Thing to create. Run 'spectra new <thing> --help' for additional information.")
    parser.set_defaults(func=new_data_command_handler)

    # spectra new data surveys ...
    # e.g. spectra new data surveys -s <section_id> 
    #parser_new_section = subparsers.add_parser('section', help='Create a new section')
    #build_new_section_parser(parser_new_section)

    # spectra new data zoom-report -s <section_id> -in zoom_report.csv
    #parser_survey_links = subparsers.add_parser('links', help='Makes survey links')
    #build_links_parser(parser_survey_links)

    
def new_data_command_handler(args):
    print("Invalid command. Run 'spectra new raw-data --help' for more info.")
