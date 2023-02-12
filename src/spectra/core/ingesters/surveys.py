##
##
import base64 
import json
import os
from rich import print as rprint

# This is where we can add subcommand parser commands
def build_ingest_surveys_parser(parser): 
    parser.set_defaults(func=surveys_ingester)
    parser.add_argument('section_id', help='The section ID')
    parser.add_argument('survey_id', help='The survey ID')

    
# The surveys ingestion handler
def surveys_ingester(args):
    rprint('[bold magenta]Ingesting surveys ...[/bold magenta]\n')

    indent_prefix = '[dim white]+[/dim white]'
    path_tag = lambda p: f'[dim yellow]{p}[/dim yellow]'
    h1 = lambda x: f'[bold blue]{x}[/bold blue]'
    rprint(f'{indent_prefix} {h1("Reading form files")} for [bold white]{args.section_id}[/bold white] / [bold white]{args.survey_id} ...[/bold white]')
    data, err, warn = read_survey_form_files(args.section_id, args.survey_id)
    rprint(f'  {indent_prefix} Successfully processed {len(data)} records.')
    rprint(f'  {indent_prefix} Failed to process {len(err)} records.')

    rprint(f'{indent_prefix} {h1("Storing processed records")} to disk ...')
    dest = write_data_to_processed_file(args.section_id, args.survey_id, data)
    rprint(f'  {indent_prefix} Processed data written to {path_tag(dest)}')
    dest = write_warnings_json_file(args.section_id, args.survey_id, data, err, warn)
    rprint(f'  {indent_prefix} Processed warnings written to {path_tag(dest)}')

    rprint(f'{indent_prefix} {h1("Writing logs")} and reports ...')
    dest = write_processing_logs_file(args.section_id, args.survey_id, data, err, warn)
    rprint(f'  {indent_prefix} Processed logs written to {path_tag(dest)}')

    rprint('\n[bold green]Complete.[/bold green]')

    out = dest.replace('.md', '.pdf')
    cmd = f'pandoc -V geometry:margin=1in {dest} -o {out}'
    rprint(f'\nRun the following command to generate a PDF report:')
    print(f'\n    {cmd}\n\n')
    

def write_warnings_json_file(section, survey, data, err, warn):
    filename = f'.spectra-data/data/{section}/proc/{survey}.warnings.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(warn, indent=4))
    return filename


def write_processing_logs_file(section, survey, data, err, warn):
    filename    = f'.spectra-data/data/{section}/proc/{survey}.logs.md'
    successes   = len(data)
    failures    = len(err)
    total       = successes + failures
    warn_nosub  = [ w for w in warn if w['type'] == 'NOT_SUBMITTED' ]
    warn_late   = [ w for w in warn if w['type'] == 'LATE' ]
    noncompliance = len(warn_nosub) + len(warn_late)

    with open( f'.spectra-data/sections/{section}/roster.json') as f:
        roster = json.load(f)
    total_people = len(roster['CanvasIndex'].keys())
    noncomp_rate  = (noncompliance / total_people) * 100

    with open(filename, 'w') as f:
        f.write(f'# Processing Logs for {section} / {survey}\n\n')
        f.write('## Overview\n\n')
        f.write(f'Successfully processes {len(data)} records with {len(err)} errors.\n')
        f.write(f'There were {noncompliance} ({noncomp_rate:.1f}%) compliance issues.\n')
        f.write(f'Of these {len(warn_late)} were late, {len(warn_nosub)} were not submitted.\n')
        f.write('\n')

        f.write('## Processing Errors\n\n')
        for e in err:
            f.write(f"  - {e['message']}\n")
        if len(err) == 0:
            f.write('There were 0 processing errors.\n')
        f.write('\n')

        f.write('## User Warnings\n\n')
        for w in sorted(warn, key=lambda x: x['name']):
            f.write(f"  - {w['message']}\n")
        if len(warn) == 0:
            f.write('There were 0 user warnings.\n')
        f.write('\n')
    return filename


def write_data_to_processed_file(section, survey, data):
    filename = f'.spectra-data/data/{section}/proc/{survey}.records.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=4))
    return filename


def read_survey_form_files(section, survey):
    result    = []
    err       = []
    warn      = []
    directory = f'.spectra-data/data/{section}/raw/{survey}'
    done      = {}

    roster_file = f'.spectra-data/sections/{section}/roster.json'
    with open(roster_file) as f:
        roster = json.load(f)

    for filename in os.listdir(directory):
        if filename.endswith(".tdform"):
            form_file = os.path.join(directory, filename)
            with open(form_file) as f:
                # Read the tdform file
                form_data = base64.b64decode(f.read())
                form_data = json.loads(form_data)

                # Parse any file-level metadata
                date_str  = '-'.join(survey.split('-')[:2])
                date_str  = f'{date_str}T12:00.000'
                user_id   = filename.replace('LATE_', '').split('_')[1]
                done[user_id] = True

                # Late flags
                if filename.split('_')[1] == 'LATE':
                    person = roster['CanvasIndex'][user_id]
                    name = roster['CanvasIndex'][user_id]['name']
                    team = roster['CanvasIndex'][user_id]['team']
                    warn.append({
                        'type': 'LATE',
                        'message': f'Late submission from **{name}**, {team}.',
                        'dt': date_str,
                        'name': name,
                        'person_id': user_id,
                        'team': team,
                        'survey': survey,
                        'section': section
                    })
                
                # Go through each question key-value pair and make a record of it
                for key, value in form_data['results'].items():
                    record = make_record(filename, section, date_str, user_id, form_data, roster, key, value)
                    if record is not None:
                        result.append(record)    
                    else:
                        err.append({
                            'type': 'PROC_FAILURE',
                            'message': f'Failed to process question key {key} in file {filename}'
                        })
    
    # No submission warning
    for canvas_id, person in roster['CanvasIndex'].items():
        if canvas_id not in done:
            warn.append({
                'type': 'NOT_SUBMITTED',
                'message': f'No submission from **{person["name"]}**, {team}.',
                'dt': date_str,
                'name': person['name'],
                'person_id': user_id,
                'team': person['team'],
                'survey': survey,
                'section': section
            })
    return result, err, warn


def make_record(filename, section, date_str, user_id, data, roster, key, value):
    record = {
        "dt"            : f'{date_str}',
        'survey_uid'    : key,
        "source_file"   : filename,
        "section"       : section,
        "name"          : roster['CanvasIndex'][user_id]['name'],
        "fname"         : roster['CanvasIndex'][user_id]['fname'],
        "lname"         : roster['CanvasIndex'][user_id]['lname'],
        "team"          : roster['CanvasIndex'][user_id]['team'],
        "group_id"      : roster['CanvasIndex'][user_id]['group_id'],
        "nid"           : roster['CanvasIndex'][user_id]['nid'],
        "person_id"     : user_id
    }

    question_metadata = None
    if key.startswith('i_'):
        question_metadata = extract_linear_question_metadata(key, data, filename)
    elif key.startswith('m_'):
        question_metadata = extract_matrix_question_metadata(key, data, roster, filename)
    else:
        print(f'WARNING: Failure processing question key {key} in file {filename}')
        return None

    if question_metadata:
        record.update(question_metadata)
        answer_metadata = extract_answer_metadata(value)
        if answer_metadata:
            record.update(answer_metadata)
            return record
    return None
    


def extract_linear_question_metadata(key, data, filename):
    question_id = key.split('_')[1]
    for question in data['survey']['linear']['q']:
        if question['id'] == question_id:
            return {
                "question_id": question_id,
                "question_type": 'linear', 
                "question_text": question['text'],
                "input_type": question['type']
            }
    print(f'WARNING: Failure processing question key metadata {key} in file {filename}')
    return None


def extract_matrix_question_metadata(key, data, roster, filename):
    question_id = key.split('_')[2]
    question_meta_peer_id = key.split('_')[1]
    for question in data['survey']['matrix']['y']:
        if question['id'] == question_id:
            return {
                "question_id": question_id,
                "question_type": 'matrix',
                "question_meta_peer_id": question_meta_peer_id,
                "question_meta_peer_name": roster['CanvasIndex'][question_meta_peer_id]['name'],
                "question_text": question['label'],
                "input_type": question['type']
            }
    print(f'WARNING: Failure processing question key metadata {key} in file {filename}')
    return None


def extract_answer_metadata(value):
    if isinstance(value, int) or isinstance(value, float):
        return {'answer_number': value, 'answer_type': 'Number', 'answer': str(value)}
    elif isinstance(value, str):
        return {'answer_string': value, 'answer_type': 'String', 'answer': str(value)}
    elif isinstance(value, bool):
        return {'answer_bool': value, 'answer_type': 'Boolean', 'answer': str(value)}
    elif value is None:
        return {'answer_type': 'Null', 'answer': str(value)}
    else:
        print(f'ERROR: Unable to extract metadata for answer value {value} of type {type(value)}')
        return None