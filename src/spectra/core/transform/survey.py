import os
import json

def build_transform_survey_parser(parser):
    parser.set_defaults(func=survey_transformer)
    parser.add_argument('-s', '--section', required=True, help='The section ID')
    parser.add_argument('-i', '-in', '--survey-id', required=True, help='The survey ID')
    parser.add_argument('-o', '--output', required=True, choices=['csv'], help='The output format')


def get_proc_dir_for_section(section):
    return f'spectra-data/{section}/data/surveys/proc'


def survey_transformer(args):
    proc_dir = get_proc_dir_for_section(args.section)
    filename = f'{args.survey_id}.records.json'
    filepath = os.path.join(proc_dir, filename)
    with open(filepath) as f:
        data = json.load(f)

    if args.output == 'csv':
        result = transform_to_csv(data)
    else:
        print('Unknown output type. Try running specta transform survey --help')
        exit(1)

    output_filepath = os.path.join(proc_dir, f'{args.survey_id}.records.{args.output}')
    with open(output_filepath, 'w') as f:
        f.write(result)


def transform_to_csv(data):
    all_keys = []
    for pt in data:
        for key in pt.keys():
            if key not in all_keys:
                all_keys.append(key)
        
    header = ','.join([key for key in all_keys])
    formatter = ','.join(['"{' + key + '}"' for key in all_keys])
    csv = header + '\n'
    for pt in data:
        row_data = _make_default_csv_row(all_keys)
        row_data.update(pt)
        csv += formatter.format(**row_data) + '\n'
    
    return csv


def _make_default_csv_row(keys):
    result = {}
    for key in keys:
        result[key] = ""
    return result
