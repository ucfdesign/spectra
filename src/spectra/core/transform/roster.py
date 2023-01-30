"""

The roster serializer

"""

import csv
import json


class Roster:

    def __init__(self, fpath):
        if fpath.endswith('.json'):
            self.roster = json.loads(open(fpath).read())
        elif fpath.endswith('.csv'):
            roster = []
            # Serialize each row into roster list
            with open(fpath, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                skipped_first_row = False
                for row in reader:
                    if not skipped_first_row:
                        skipped_first_row = True
                        continue
                    data = self.row_serializer(row)
                    roster.append(data)

            # Create indexed roster object
            teams = {}
            canvas_index = {}
            for student in roster:
                # Add student to team
                team_key = student['group_id']
                if team_key not in teams.keys():
                    teams[team_key] = { 'name': student['team'], 'members': [] }
                teams[team_key]['members'].append(student)

                # Add student to canvas_id index
                canvas_id = student['canvas_user_id']
                if canvas_id not in canvas_index.keys():
                    canvas_index[canvas_id] = student
            output = {
                'Teams': teams,
                'CanvasIndex': canvas_index
            }
            self.roster = output

    def to_dict(self):
        return self.roster

    def row_serializer(self, row):
        name = row[0]
        fname = name.split(', ')[1]
        lname = name.split(', ')[0]
        nid = row[3]
        canvas_user_id = row[1]
        user_id = row[2]
        team = row[5]
        group_id = row[6]
        if team == '' or team is None:
            team = '_unassigned'
        if group_id == '' or group_id is None:
            group_id = '_unassigned'
        return {
            'name': name,
            'nid': nid,
            'team': team,
            'fname': fname,
            'lname': lname,
            'canvas_user_id': canvas_user_id,
            'user_id': user_id,
            'group_id': group_id
        }



