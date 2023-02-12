from .surveys import build_ingest_surveys_parser, surveys_ingester


def build_ingest_parser(parser):
    #parser.add_argument('object', help='New thing to create')
    subparsers = parser.add_subparsers(help="Ingest some data. Run 'spectra ingest <type> --help' for additional information.")
    parser.set_defaults(func=default_ingest_handler)
    
    # spectra ingest surveys
    parser_ingest_surveys = subparsers.add_parser('surveys', help='Ingest survey files')
    build_ingest_surveys_parser(parser_ingest_surveys)
    


def default_ingest_handler(args):
     print("Invalid command. Run 'spectra ingest --help' for more info.")