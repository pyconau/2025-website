import requests
from ruamel.yaml import YAML
import dateutil.parser
from datetime import timedelta
from parse import parse
from pprint import pprint
from markdown import Markdown
import bleach
from os import environ

PRETALX_TOKEN = environ["PRETALX_TOKEN"]

yaml = YAML()
md = Markdown()


def paginate(url):
    next_url = url
    while next_url:
        res = requests.get(
            next_url, headers={"Authorization": f"Token {PRETALX_TOKEN}"},
        )
        res.raise_for_status()
        data = res.json()
        next_url = data["next"]
        yield from data["results"]


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
            "h2",
            "h3",
        ),
    )


rooms = {
    "Curlyboi Theatre": 1,
    "Python 2 Memorial Concert Hall": 2,
    "Flip Floperator Pavillion": 3,
    "The One Obvious Room": 4,
}

seen_speakers = set()

for session in paginate("https://pretalx.com/api/events/pycon-au-2020/talks/"):
    speakers = [x["code"] for x in session["speakers"]]
    seen_speakers.update(speakers)
    with open(f'data/Session/{session["code"]}.yml', "w") as f:
        start = dateutil.parser.isoparse(session["slot"]["start"]).replace(tzinfo=None)
        end = dateutil.parser.isoparse(session["slot"]["end"]).replace(tzinfo=None)
        yaml.dump(
            {
                "title": session["title"],
                "start": start,
                "end": end,
                "room": rooms[session["slot"]["room"]["en"]],
                "abstract": parse_markdown(session["abstract"]),
                "description": parse_markdown(session["description"]),
                "code": session["code"],
                "speakers": speakers,
            },
            f,
        )


for speaker in paginate("https://pretalx.com/api/events/pycon-au-2020/speakers/"):
    if speaker["code"] not in seen_speakers:
        continue
    with open(f'data/Person/{speaker["code"]}.yml', "w") as f:
        yaml.dump(
            {
                "name": speaker["name"],
                "pronouns": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == 474
                    ),
                    None,
                ),
                "bio": parse_markdown(speaker["biography"] or ""),
            },
            f,
        )

