import os
import json
import time
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from rich import print as rprint


class SurveyReport:
    """This analyzer converts a single survey to a PDF report.
    
    """

    @staticmethod
    def run(args):
        h1 = '[bold cyan]SurveyReport[/bold cyan]'
        section = f'[yellow]{args.section}[/yellow]'
        survey = f'[yellow]{args.survey_id}[/yellow]'
        h2 = f'[bold white]Analyzing survey {section} / {survey} ...[/bold white]'
        rprint(f'\n{h1} - {h2}\n')

        # The section root path
        section_path = os.path.join('spectra-data', args.section)

        # Make output directory
        report_name = f'SurveyReport_{args.section}_{args.survey_id}'
        output_dir = os.path.join(section_path, 'outputs', report_name)
        assets_dir = os.path.join(output_dir, 'assets')
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)
        
        # Load the roster file
        roster_path = os.path.join(section_path, 'roster.json')
        with open(roster_path) as f:
            roster = json.load(f)

        # Load the survey record
        surveys_path = os.path.join(section_path, 'data', 'surveys', 'proc')
        records_path = os.path.join(surveys_path, f'{args.survey_id}.records.json')
        with open(records_path) as f:
            records = json.load(f)

        teams = roster['Teams']
        markdown = '# Results by Team\n'
        sorted_teams = sorted(teams.items(), key=lambda x: x[1]['name'])
        for team_id, team in sorted_teams:
            pre = '[dim white]+[/dim white]'
            team_color_tag = 'blue'
            rprint(f'{pre} Processing team [{team_color_tag}]{team.get("name")}[/{team_color_tag}] ...')
            markdown += SurveyReport.process_team_records(team_id, team, records, output_dir)
            markdown += '\n$\pagebreak$\n'
        
        # Write report as Markdown
        output_path = os.path.join(output_dir, 'index.md')
        with open(output_path, 'w') as f:
            f.write(markdown)
        
        print('')
        print('If using Endeavor for document generation, add the document.yaml file alongside the report. Them convert the report to PDF using the following command:')
        print('')
        print(f'evdoc spectra-data/{args.section}/outputs/{report_name}')
        print('')


    @classmethod
    def process_team_records(cls, team_id, team, records, output_dir):
        result = ''
        filter_func = SurveyReport.filter_by_team_id(team_id)
        filtered = filter(filter_func, records)
        records_for_team = [i for i in filtered ] 

        #result += '\n### Average Peer Evaluation\n\n'
        result += f"\n\n## {team['name']}\n"

        result += '### Team Members\n\n'
        result += '| Name |  NID  |  Canvas ID  |\n'
        result += '|:--|:--|:--|\n'
        for m in team['members']:
            result += f"| {m['name']} | {m['nid']} | {m['canvas_user_id']} |\n"
        result += '\n'

        result += '\n\n### Peer Evaluation Averages\n\n'

        result += SurveyReport.generate_team_report(team_id, team, records, output_dir)

        result += '\n\n$\pagebreak$\n\n'

        result += '\n\n### Peer Review Breakdown\n\n'

        questions = {
            'prof': 'Professionalism', 
            'attp': 'Attendance and Preparedness', 
            'qnty': 'Quantity of Contributions', 
            'qlty': 'Quality of Contributions', 
            'comm': 'Communication', 
            'tmwk': 'Teamwork'
        }
        result += '|   |   |\n'
        result += '|:--|:--|\n'
        for q, label in questions.items():
            #result += f'### Scores by Dimension: {label}\n'
            md = SurveyReport.generate_team_report(team_id, team, records, output_dir, question=q, label=label)
            result += f'| {md}{{ width=42% }} '
            # Add newline after every two images
            if q in ['attp', 'qlty', 'tmqk']:
                result += '|\n'

        result += '\n\n$\pagebreak$\n\n'

        
        # Create a comments data frame and group for printing
        comments = [r for r in records if r['group_id'] == team_id and r['question_id'] == 'cmnt']
        df = pd.DataFrame.from_dict(comments)

        result += '\n\n### Comments\n\n'
        
        if df.empty:
            result += '\n\nNo comments or error processing comments.\n\n'
        else:
            comment_groups = df.groupby(['question_meta_peer_name', 'name'])

            # Loop over each group and print the comments
            last_peer = ''
            for group_name, group_data in comment_groups:
                peer_name, name = group_name
                if last_peer != peer_name:
                    result += f'\n\n**Feedback for {peer_name}**\n\n'
                    result += '| Reviewer |  Comment |\n'
                    result += '|:--|:--------|\n'
                    last_peer = peer_name
                for comment in group_data['answer']:
                    result += f'| {name} | {comment} |\n'

        return result
    

    @staticmethod
    def generate_team_report(team_id, team, records, output_dir, question=None, label='Average'):
        #team = roster['Teams'][team_id]
        markdown = ''

        # Filter peer eval records for the team
        _start = time.time()
        is_matrix = lambda x: x['question_type'] == 'matrix'
        is_number = lambda x: x['answer_type'] == 'Number'
        docs = [r for r in records if r['group_id'] == team_id and is_matrix(r) and is_number(r)]
        if question is not None:
            docs = [ d for d in docs if d['question_id'] == question ]
        _end = time.time()
        total = len(docs)
        elapsed_ms = (_end - _start)*1000
        #print(f'Got {total} results in {elapsed_ms:.3f} ms.')

        # Compute the average review
        N = len(team['members'])
        A = np.zeros((N, N))
        for i, reviewer in enumerate(team['members']):
            for j, peer in enumerate(team['members']):
                reviewer_name = reviewer['name']
                peer_name = peer['name']
                all_ratings = []
                for d in docs:
                    if d['name'] == reviewer_name and d['question_meta_peer_name'] == peer_name:
                        all_ratings.append(d['answer_number'])
                #print(all_ratings)
                avg = np.mean(all_ratings)
                A[i][j] = avg

        #print(A)
        names = [ reviewer['name'] for  reviewer in team['members'] ]
        #print(names)

        fig, ax = plt.subplots()
        im = ax.imshow(A, cmap='RdYlGn', vmin=1, vmax=5)

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(len(names)), labels=names)
        ax.set_yticks(np.arange(len(names)), labels=names)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=25, ha="right",
                rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(names)):
            for j in range(len(names)):
                text = ax.text(j, i, f'{A[i][j]:.2f}',
                            ha="center", va="center", color="k")

        ax.set_title(f"{label} for {team['name']}")
        fig.tight_layout()
        #plt.show()

        plt.ylabel('Reviewer')
        plt.xlabel('Peer Reviewed')

        if question is not None:
            question_bit = question
        else:
            question_bit = 'avg'
        fname = f'team-matrix_{team_id}_{question_bit}.png'
        fpath = os.path.join(output_dir, 'assets', fname)
        plt.savefig(fpath, format="png")
        plt.close()

        markdown += f'![{label}](./assets/{fname})'
        return markdown
    

    @staticmethod
    def sort(x):
        return 'prof' > 'attp' > 'qnty' > 'qlty' > 'comm' > 'tmwk' > 'cmnt'
        

    @staticmethod
    def filter_by_team_id(team_id):
        def fun(record):
            return record.get('group_id', False) == team_id
        return fun

    @staticmethod
    def filter_by_person_id(person_id):
        def fun(record):
            val = record.get('person_id', False)
            print(f'Cmp {val} == {person_id}')
            if record.get('person_id', False) == person_id:
                return True
            else:
                return False
        return fun

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')
        parser.add_argument('-i', '-in', '--survey-id', required=True, help='The survey ID')


    
    @staticmethod
    def get_document_yaml():
        return f''