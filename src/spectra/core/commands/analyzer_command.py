from spectra.analyzers import __all__ as analyzers

def build_analyze_parser(parser):
    subparsers = parser.add_subparsers(help="Analyze some data. Run 'spectra analyzer <type> --help' for additional information.")
    parser.set_defaults(func=default_analyze_handler)

    for analyzer in analyzers:
        sp = subparsers.add_parser(analyzer.__name__, help=analyzer.__doc__)
        analyzer.build_parser(sp)
    

def default_analyze_handler(args):
    print("Invalid command. Run 'spectra analyzer --help' for more info.")
    