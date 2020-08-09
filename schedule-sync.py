import requests
from ruamel.yaml import YAML
import dateutil.parser
from datetime import timedelta
from parse import parse

yaml = YAML()

rooms = {
    'Red Track': 1,
    'Green Track': 2,
    'Purple Track': 3,
    'BoF': 4,
}

SCHEDULE_URL = 'https://pretalx.com/juliacon2020/schedule/export/schedule.json'

sched_data = requests.get(SCHEDULE_URL).json()

for day in sched_data['schedule']['conference']['days']:
    for room_name, room_sched in day['rooms'].items():
        for session in room_sched:
            with open(f'data/Session/{session["slug"]}.yml', 'w') as f:
                start = dateutil.parser.isoparse(session['date'])
                hr, min_ = parse('{:d}:{:d}', session['duration'])
                duration = timedelta(hours=hr, minutes=min_)
                yaml.dump({
                    "title": session['title'],
                    "start": start,
                    "end": start + duration,
                    'room': rooms[session['room']],
                }, f)