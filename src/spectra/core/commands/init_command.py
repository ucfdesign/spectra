import os
from rich import print as rprint

def build_init_parser(parser):
    parser.set_defaults(func=init_handler)


def init_handler(args):
    rprint('[cyan bold]Initializing[/cyan bold] spectra project ...', end=' ')
    os.mkdir('.spectra')
    os.mkdir('spectra-data')
    os.mkdir('surveys')
    os.mkdir('analysis')
    os.mkdir('reports')
    os.mkdir('experiments')
    rprint('[green bold]OK[/green bold]')
    print('')