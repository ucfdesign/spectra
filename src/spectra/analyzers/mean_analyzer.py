import os
import pandas as pd
from rich import print as rprint

class MeanAnalyzer:
    """This analyzer is based on an algorithm proposed by ChatGPT.
    
    """

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')
        parser.add_argument('-i', '-in', '--survey-id', required=True, help='The survey ID')



    @staticmethod
    def run(args):
        # Print consoler header ingo
        h1 = '[bold cyan]Mean Analyzer[/bold cyan]'
        section = f'[yellow]{args.section}[/yellow]'
        survey = f'[yellow]{args.survey_id}[/yellow]'
        h2 = f'[bold white]Analyzing survey {section} / {survey} ...[/bold white]'
        rprint(f'\n{h1} - {h2}\n')

        # The section root path
        section_path = os.path.join('spectra-data', args.section)

        # Load the survey record
        surveys_path = os.path.join(section_path, 'data', 'surveys', 'proc')
        records_path = os.path.join(surveys_path, f'{args.survey_id}.records.csv')
        print(f'  + Reading data from {records_path} ...')
        
        # Load the data into a pandas dataframe
        df = pd.read_csv(records_path)
        #print(df.head())

        # Filter on numerical data
        #df.query("answer_type == 'rating'", inplace=True)
        df.loc[df['answer_type'] == 'Number']
        df['answer_number'] = df['answer_number'].astype(float)
        print('  + Completed type checking')
    
        print('  + Doing math ...')

        MEAN_THRESHOLD = 4.5
        STD_DEV_THRESHOLD = 0.0 

        # Calculate the average score for each team
        avg_scores = df.groupby('team')['answer_number'].mean()

        # Calculate the standard deviation of scores for each team
        std_scores = df.groupby('team')['answer_number'].std()

        # Identify teams with low average scores and high standard deviations
        problem_teams = avg_scores[(avg_scores < MEAN_THRESHOLD) & (std_scores > STD_DEV_THRESHOLD)].index.tolist()

        # Look at the individual scores for each team member
        print('')
        for team in problem_teams:
            team_df = df[df['team'] == team]
            low_scores = team_df[team_df['answer_number'] < MEAN_THRESHOLD]
            
            # Look for patterns in low-scoring team members
            patterns = low_scores.groupby(['question_meta_peer_name', 'question_id'])['answer_number'].count()
            rprint('[bold red]Problematic team: [/bold red]', team)
            #rprint('[bold blue]\nLow scores: [/bold blue]')
            #print(low_scores[['name', 'question_meta_peer_name', 'survey_uid', 'answer']])
            #rprint('[bold blue]\nPatterns in low scores: [/bold blue]')
            #print(patterns)

