import os
import json
from rich import print as rprint

class NonComplianceSummarizer:
    """This analyzer summarizes the peer evaluation non-compliance data into a 
    single JSON file. It also generates a CSV file containing the non-compliance
    data for each student.
    
    """

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')
        parser.add_argument('--no-sub-pct-reduction', type=float, default=5.0)
        parser.add_argument('--nosub-percent-reduction', type=float, default=5.0)
        parser.add_argument('--late-percent-reduction', type=float, default=2.5)

    @staticmethod
    def run(args):
        # Print consoler header 
        h1 = '[bold cyan]Non-Compliance Summarizer[/bold cyan]'
        section = f'[yellow]{args.section}[/yellow]'
        h2 = f'[bold white]Analyzing section {section}  ...[/bold white]'
        rprint(f'\n{h1} - {h2}\n')

        section_path = os.path.join('spectra-data', args.section)
        surveys_path = os.path.join(section_path, 'data', 'surveys', 'proc')
        warnings_files = [] 
        for f in os.listdir(surveys_path):
            if f.endswith('.warnings.json'):
                rprint(f'  + Adding {f} ...')
                warnings_files.append(os.path.join(surveys_path, f)) 
        print('')

        # Aggregate all the warnings into one list
        all_warnings = []
        for filepath in warnings_files:
            data = json.load(open(filepath))
            all_warnings += data

        # Group warnings by person
        by_person = {}
        for warning in all_warnings:
            uid = warning.get('person_id')
            name = warning.get('name')
            team = warning.get('team')
            if name not in by_person.keys():
                by_person[name] = {
                    'uid': uid,
                    'name': name,
                    'team': team,
                    'events': []
                }
            by_person[name]['events'].append(warning)
        
        # Score them
        for warnings in by_person.values():
            name = warnings['name']
            n_late = len([ evt for evt in warnings['events'] if evt['type'] == 'LATE'])
            n_nosub = len([ evt for evt in warnings['events'] if evt['type'] == 'NOT_SUBMITTED'])
            nosub_weight = args.nosub_percent_reduction 
            late_weight = args.late_percent_reduction
            warnings['score'] = nosub_weight*n_nosub + late_weight*n_late
        
        # Sort by score and print them
        all_output = []
        all_output_list = []
        filtered = sorted(by_person.values(), key=lambda x: x['score'], reverse=True)
        for warnings in filtered:
            name = warnings['name']
            score = warnings['score']
            team = warnings['team']
            n_late = len([ evt for evt in warnings['events'] if evt['type'] == 'LATE'])
            n_nosub = len([ evt for evt in warnings['events'] if evt['type'] == 'NOT_SUBMITTED'])
            output = f'{-1*score:8.1f}     {n_late} late, {n_nosub} not submitted    {name:48} {team}'
            all_output.append(output)
            all_output_list.append([
              name,
              team,
              n_late,
              n_nosub,
              -1*score  
            ])
            print(output)

        # Save outputs to file
        output_path = os.path.join(section_path, 'outputs', f'non-compliance_flags_{args.section}.txt')
        with open(output_path, 'w') as f:
            f.write('\n'.join(all_output))

        # Save outputs to CSV file
        csv_output_path = os.path.join(section_path, 'outputs', f'non-compliance_flags_{args.section}.csv')
        with open(csv_output_path, 'w') as f:
            f.write('name,team,n_late,n_nosub,score\n')
            for row in all_output_list:
                f.write(','.join([f'"{str(x)}"' for x in row]) + '\n')


