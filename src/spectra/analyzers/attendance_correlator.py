import os
import json
import pandas as pd
from rich import print as rprint

class AttendanceCorrelator:
    """This analyzer correlates the aggregated attendance data with the Zoom
    report flags and provides and adjusted attendance report.

    The AttendanceAggregator and ZoomReport analyzers must be run first. 
    This analyzer expects to find `absences.json` and `zoom-flags.json` in the
    `spectra-data/<section>/outputs` directory.

    To run those analyzers, run:

    spectra analyze AttendanceAggregator -s `<section>`
    spectra analyze ZoomReport -s <section> --output raw
    
    """

    @classmethod
    def build_parser(cls, parser):
        parser.set_defaults(func=cls.run)
        parser.add_argument('-s', '--section', required=True, help='The section ID')

    @staticmethod
    def run(args):
        # The output directory
        output_dir = os.path.join('spectra-data', args.section, 'outputs')

        # Load the roster
        rosterpath = os.path.join('spectra-data', args.section, 'roster.json')
        roster = json.load(open(rosterpath))

        # Load the attendance data
        attendancepath = os.path.join(output_dir, 'absences.json')
        attendance = json.load(open(attendancepath))

        # Load the Zoom report flags
        flagspath = os.path.join(output_dir, 'zoom-flags.json')
        flags = json.load(open(flagspath))

        # Preprocess the flags and match them to roster records
        match_failures = []
        for date, flag in flags.items():
            for student in flag:
                # Try to find a roster match
                match = AttendanceCorrelator.find_match(student, roster)
                if match is None:
                    match_failures.append(student)
                    continue
                # If match is found, add it to the student record
                student['record'] = match

        # Loop over each student in attendance data
        for student in attendance:
            student['additionalAbsences'] = []
            for date in student['present']:
                # If the student was flagged for this date, mark them absent
                if date not in flags:
                    continue

                # Look at each flagged student on this date's flags
                for flagged_student in flags[date]:
                    record = flagged_student.get('record', {})
                    roster_id = record.get('canvas_user_id', None)

                    # If the student was flagged on that date, add absences
                    if student['student_id'] == roster_id:
                        student['additionalAbsences'].append(date)
        
        # Write the adjusted attendance data
        adjusted_attendance_path = os.path.join(output_dir, 'adjusted-absences.json')
        with open(adjusted_attendance_path, 'w') as f:
            json.dump(attendance, f, indent=4)

        # Log the match failures
        match_fail_output = os.path.join(output_dir, 'zoom_match.errors.json')
        with open(match_fail_output, 'w') as f:
            json.dump(match_failures, f, indent=4)

        # Summarize counts
        for student in attendance:
            n_absences = len(student['absences'])
            n_additional_absences = len(student['additionalAbsences'])
            n_total_absences = n_absences + n_additional_absences
            student['nAbsences'] = n_absences
            student['nAdditionalAbsences'] = n_additional_absences
            student['nTotalAbsences'] = n_total_absences

        # Write the summary data to CSV
        summary_path = os.path.join(output_dir, 'attendance-summary.csv')
        df = pd.DataFrame(attendance)
        df.to_csv(summary_path, index=False)

        # Print the summary
        rprint(f"[bold white]{'Name':38} {'Abs':8} {'Adj Abs':8} {'Total':8} {'Team'}[/bold white]")
        print('-' * 80)
        for student in sorted(attendance, key=lambda s: s['nTotalAbsences'], reverse=True):
            name = student['name']
            team = student['team']
            nAbsences = student['nAbsences']
            nAdditionalAbsences = student['nAdditionalAbsences']
            nTotalAbsences = student['nTotalAbsences']

            # Skip printing students with no absences
            if nTotalAbsences == 0:
                continue

            tag2 = 'bold white' 
            if nAdditionalAbsences >= 3: 
                tag2 = 'bold red'
            elif nAdditionalAbsences > 0:
                tag2 = 'bold yellow'
            
            tag3 = 'bold white' 
            if nTotalAbsences >= 8: 
                tag3 = 'bold red'
            if nTotalAbsences >= 5: 
                tag3 = 'bold yellow'
            elif nTotalAbsences > 0:
                tag3 = 'bold green'
            rprint(
                f'[bold cyan]{name:38}[/bold cyan] ' + 
                f'[white]{nAbsences:8}[/white] ' + 
                f'[{tag2}]{nAdditionalAbsences:8}[/{tag2}] ' + 
                f'[{tag3}]{nTotalAbsences:8}[/{tag3}] ' + 
                f'[bold blue]{team:40}[/bold blue]'
            )

    @staticmethod
    def find_match(student, roster):
        for record in roster['CanvasIndex'].values():
            # If student name is an exact match, return the record
            if student.get('name', '') == record.get('name', None):
                return record
            # If email is an exact match, return the record
            if student.get('email', '') == record.get('email', None):
                return record
            
            # Try to match on re-ordering of first and last name
            lname = student.get('name', '').split(' ')[-1]
            fname = student.get('name', '').split(' ')[0]
            if record['lname'] == lname and record['fname'].startswith(fname):
                return record
        return None
       