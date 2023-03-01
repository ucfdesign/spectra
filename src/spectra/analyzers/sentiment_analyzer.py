import os
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from rich import print as rprint

class SentimentAnalyzer:
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
        h1 = '[bold cyan]Sentiment Analyzer[/bold cyan]'
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

        # Filter on comments only
        df = df[df['question_id'] == 'cmnt']
        df['comment'] = df['answer'].astype(str)

        # Clean the comments
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()

        def clean_comment(comment):
            tokens = word_tokenize(comment.lower())
            tokens = [stemmer.stem(token) for token in tokens if token not in stop_words and token.isalpha()]
            return ' '.join(tokens)

        df['clean_comment'] = df['comment'].apply(clean_comment)

        # Perform frequency analysis
        vectorizer = CountVectorizer()
        counts = vectorizer.fit_transform(df['clean_comment'])
        word_freq = pd.DataFrame(counts.sum(axis=0), columns=vectorizer.get_feature_names()).T
        word_freq.columns = ['count']
        word_freq = word_freq.sort_values('count', ascending=False)

        # Perform sentiment analysis
        sia = SentimentIntensityAnalyzer()
        df['sentiment'] = df['comment'].apply(lambda x: sia.polarity_scores(x)['compound'])
        df['sentiment_neg'] = df['comment'].apply(lambda x: sia.polarity_scores(x)['neg'])
        df['sentiment_neu'] = df['comment'].apply(lambda x: sia.polarity_scores(x)['neu'])
        df['sentiment_pos'] = df['comment'].apply(lambda x: sia.polarity_scores(x)['pos'])

        # Perform topic modeling
        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        topic_model = lda.fit_transform(counts)
        df['topic'] = topic_model.argmax(axis=1)


        # Sort the sentiment scores in descending order
        df_sorted = df.sort_values('sentiment', ascending=False)

        # Print the sentiment scores sorted by score value
        for index, row in df_sorted.iterrows():
            tag = get_sentiment_color_tag(row['sentiment'])
            tag_n = get_sentiment_color_tag(row['sentiment_neg'], invert=True)
            tag_u = get_sentiment_color_tag(row['sentiment_neu'])
            tag_p = get_sentiment_color_tag(row['sentiment_pos'])
            print('')
            sep = f'[dim white] | [/dim white]'
            team = f"[bold cyan]{row['team']}[/bold cyan]"
            score = f"[{tag}]{row['sentiment']}[/{tag}] {sep} [{tag_n}]{row['sentiment_neg']}[/{tag_n}] {sep} [{tag_u}]{row['sentiment_neu']}[/{tag_u}] {sep }[{tag_p}]{row['sentiment_pos']}[/{tag_p}]"
            people = f"[white dim]{row['name']} -> {row['question_meta_peer_name']}[/white dim] "
            rprint(f"{score:34s}  {team}  {people}")
            rprint(f"[bold white]{row['comment']}[/bold white]")
        
        #print(df_sorted[['answer', 'sentiment']])

        # Group the data by reviewers or teams and calculate the average sentiment and pattern counts for each group
        reviewer_stats = df.groupby('name').agg({'sentiment': 'mean'})
        reviewee_stats = df.groupby('question_meta_peer_name').agg({'sentiment': 'mean'})
        team_stats = df.groupby('team').agg({'sentiment': 'mean'})

        # Print the reviewer and team stats
        print('')
        print('Reviewer Stats:')
        print(reviewer_stats.sort_values('sentiment', ascending=True).head())
        print('\nReviewed Stats:')
        print(reviewee_stats.sort_values('sentiment', ascending=True).head())
        print('\nTeam Stats:')
        print(team_stats.sort_values('sentiment', ascending=False))

        # Print by topic
        #by_topics = df.groupby('topic')
        #for topic_id, topic_df in by_topics:
        #    print(topic_df[['answer']])


def get_sentiment_color_tag(value, invert=False):
    multiplier = -1 if invert else 1
    score = multiplier * value
    tag = 'bold white'
    if score > 0.5:
        tag = 'bold green'
    elif 0.20 < score < 0.5:
        tag = 'bold green'
    elif -0.5 < score < -0.20:
        tag = 'bold yellow'
    elif score < -0.5:
        tag = 'bold red'
    return tag