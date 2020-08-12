import requests
from ruamel.yaml import YAML
import dateutil.parser
from datetime import timedelta
from parse import parse
from pprint import pprint
from markdown import Markdown
import bleach

yaml = YAML()
md = Markdown()


def parse_markdown(text):
    html = md.convert(text)
    return bleach.clean(
        html,
        tags=(
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "p",
        ),
    )


rooms = {
    "Curlyboi Theatre": 1,
    "Python 2 Memorial Concert Hall": 2,
    "Flip Floperator Pavillion": 3,
    "The One Obvious Room": 4,
}

SCHEDULE_URL = "https://pretalx.com/pycon-au-2020/schedule/export/schedule.json"

sched_data = requests.get(SCHEDULE_URL).json()

seen_speakers = set()

for day in sched_data["schedule"]["conference"]["days"]:
    for room_name, room_sched in day["rooms"].items():
        for session in room_sched:
            pprint(session)
            with open(f'data/Session/{session["slug"]}.yml', "w") as f:
                start = dateutil.parser.isoparse(session["date"]).replace(tzinfo=None)
                hr, min_ = parse("{:d}:{:d}", session["duration"])
                duration = timedelta(hours=hr, minutes=min_)
                yaml.dump(
                    {
                        "title": session["title"],
                        "start": start,
                        "end": start + duration,
                        "room": rooms[session["room"]],
                        "abstract": parse_markdown(session["abstract"]),
                        "description": parse_markdown(session["description"]),
                        "code": session["url"][-7:-1],
                        "speakers": [x["code"] for x in session["persons"]],
                    },
                    f,
                )

            for speaker in session["persons"]:
                if speaker["code"] not in seen_speakers:
                    seen_speakers.add(speaker["code"])
                    with open(f'data/Person/{speaker["code"]}.yml', "w") as f:
                        yaml.dump(
                            {
                                "name": speaker["public_name"],
                                "bio": parse_markdown(speaker["biography"] or ""),
                            },
                            f,
                        )

