import os
import json
import pandas as pd
from rich import print as rprint
import csv
from collections import defaultdict
from datetime import datetime, timedelta

class ZoomReport:
    """This analyzer analyzes Zoom reports and flags students who have 
    attempted to bypass the attendance system.
    
    """

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')
        parser.add_argument('-c', '--cutoff', type=int, default=20, help='The cutoff in minutes')
        parser.add_argument('--output', choices=['raw', 'raw-by-student', 'summary'], help='The output format')

    @staticmethod
    def run(args):
        # The section root path
        section_path = os.path.join('spectra-data', args.section)
        data_dir = os.path.join(section_path, 'data', 'zoom-reports')
        output_dir = os.path.join(section_path, 'outputs')

        reports = os.listdir(data_dir)
        flags = {}
        for report in reports:
            date = report.split('_')[0]
            report_path = os.path.join(data_dir, report)
            flags[date] = ZoomReport.flag_users(report_path, args.cutoff)

        if args.output == 'raw':
            print(json.dumps(flags, indent=4))
            output_file = os.path.join(output_dir, 'zoom-flags.json')
            with open(output_file, 'w') as f:
                json.dump(flags, f, indent=4)
        elif args.output == 'raw-by-student':
            summary_dict = ZoomReport.summarize_flags_by_user(flags)
            print(json.dumps(summary_dict, indent=4))
        elif args.output == 'summary':
            summary_dict = ZoomReport.summarize_flags_by_user(flags)
            summary = ZoomReport.summary_dict_to_sorted_list(summary_dict)
            for row in summary:
                if row[2] <= 1:
                    continue
                tag1 = 'bold cyan'
                tag2 = 'bold yellow'
                tag3 = 'dim white'
                fmt = f'[{tag1}]{row[0]:32}[/{tag1}] {row[1]:40} [{tag2}]{row[2]:4}[/{tag2}]   [{tag3}]{row[3]}[/{tag3}]'
                rprint(fmt)
        else:
            print('Unknown output format.')
        
    @staticmethod
    def flag_users(csv_file_path, cutoff):
        # Create a defaultdict to store the total duration for each user
        default = lambda: {'name': 'unknown', 'email': 'unknown', 'duration': 0, 'sessions': []}
        user_durations = defaultdict(default)

        # Read the CSV file
        with open(csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            NAME_KEY = '\ufeffName (Original Name)'
            EMAIL_KEY = 'User Email'
            DURATION_KEY = 'Duration (Minutes)'
            for row in reader:
                #print(row)
                # Parse the join_time and leave_time columns as datetime objects
                name = row[NAME_KEY]
                email = row[EMAIL_KEY]
                #02/09/2023 01:33:30 PM
                join_time = datetime.strptime(row['Join Time'], '%m/%d/%Y %H:%M:%S %p')
                leave_time = datetime.strptime(row['Leave Time'], '%m/%d/%Y %H:%M:%S %p')
                duration = int(row[DURATION_KEY])

                # Add the duration to the user's total duration
                user_durations[email]['name'] = name
                user_durations[email]['email'] = email
                user_durations[email]['duration'] += duration
                user_durations[email]['sessions'].append({
                    'join': join_time.isoformat(), 
                    'leave': leave_time.isoformat(), 
                    'duration': duration
                })

        # Flag users who attempt to bypass the attendance check
        flagged_users = []
        #print(json.dumps(user_durations, indent=4))
        for user, data in user_durations.items():
            first_join = datetime.fromisoformat(data['sessions'][0]['join'])
            #print(data['sessions'][0]['join'], first_join.hour, first_join.minute)
            after_130pm = first_join.hour >= 1 and first_join.minute > 30

            if (data['duration'] < cutoff and after_130pm):
                flagged_users.append(data)
        return flagged_users
    
    @staticmethod
    def summarize_flags_by_user(flagged_data):
        user_counts = {}
        # Loop over each date in the flagged_data dictionary
        for date, flagged_users in flagged_data.items():
            # Loop over each flagged user for this date
            for user in flagged_users:
                # If we haven't seen this user before, initialize their count to 0
                if user['email'] not in user_counts:
                    user_counts[user['email']] = {
                        'name': user['name'],
                        'nFlags': [],
                        'flaggedSessions': [],
                    }

                # Increment the user's count
                user_counts[user['email']]['nFlags'].append(date)
                user_counts[user['email']]['flaggedSessions'].append(user['sessions'])
        return user_counts

    @staticmethod
    def summary_dict_to_sorted_list(summary_dict):
        summary = []
        for email, user in summary_dict.items():
            summary.append([
                user['name'],
                email,
                len(user['nFlags']),
                ','.join(user['nFlags'])
            ])
        return sorted(summary, key=lambda x: x[2], reverse=True)
        
