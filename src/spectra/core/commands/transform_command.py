from spectra.core.transform.survey import build_transform_survey_parser

def build_transform_parser(parser):
    subparsers = parser.add_subparsers(help="Transform some data. Run 'spectra transform <type> --help' for additional information.")
    parser.set_defaults(func=default_transform_handler)
    
    # spectra ingest surveys
    parser_transform_surveys = subparsers.add_parser('survey', help='Transform survey files')
    build_transform_survey_parser(parser_transform_surveys)
    

def default_transform_handler(args):
    print("Invalid command. Run 'spectra transform --help' for more info.")