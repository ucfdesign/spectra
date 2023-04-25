import os
import json
import pandas as pd
from rich import print as rprint

class AttendanceAggregator:
    """This analyzer aggregates the UCF Here attendance data into a single JSON file.
    
    """

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')

    @staticmethod
    def run(args):
        PRESENT = 0
        ABSENT = 1
        absences = {}

        # Load the roster
        rosterpath = os.path.join('spectra-data', args.section, 'roster.json')
        roster = json.load(open(rosterpath))

        # The directory containing the attendance data
        directory = os.path.join('spectra-data', args.section, 'data', 'ucf-here')

        # The output directory
        output_dir = os.path.join('spectra-data', args.section, 'outputs')

        # Loop over each file in the directory
        for filename in os.listdir(directory):
            # Get the date from the filename
            date = '-'.join(filename.split('-')[0:3])
            # Read in the JSON data from this file
            with open(os.path.join(directory, filename), 'r') as f:
                data = json.load(f)['attendance_data']
            # Loop over each item in the JSON array
            for item in data:
                student_id = str(item['student'])
                # If this is the first time we've seen this student, initialize their absence count to 0
                if student_id not in absences:
                    absences[student_id] = {
                        'student_id': student_id,
                        'absences': [], 
                        'present': []
                    }
                # If the student was absent, increment their absence count
                if item['state'] == ABSENT:
                    absences[student_id]['absences'].append(date)
                elif item['state'] == PRESENT:
                    absences[student_id]['present'].append(date)

        # Print absence summary
        results = sorted(absences.values(), key=lambda x: len(x['absences']), reverse=True)   

        # Do some side-effects - add metadata to each result
        for r in results:
            student_id = r['student_id']
            count = len(r['absences'])
            student = roster['CanvasIndex'][student_id]     
            r['name'] = student['name']
            r['team'] = student['team']

        for r in results:
            student_id = r['student_id']
            count = len(r['absences'])
            tag = 'bold yellow' if count > 4 else 'bold green'
            pct = -1*(count - 4)*5 if count > 4 else 0
            rprint(f"[{tag}]{pct}%[/{tag}] {count} {r['name']}")

        # Write data to outputs
        fpath = os.path.join(output_dir, 'absences.json')
        with open(fpath, 'w') as f:
            json.dump(results, f, indent=4)
        print(f'Data written to {fpath}')

        return absences