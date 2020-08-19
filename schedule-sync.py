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

session_types = {
    720: "L",
    721: "P",
    722: "RL",
    723: "RP",
}

seen_speakers = set()

for session in paginate("https://pretalx.com/api/events/pycon-au-2020/talks/"):
    speakers = [x["code"] for x in session["speakers"]]
    seen_speakers.update(speakers)
    with open(f'data/Session/{session["code"]}.yml', "w") as f:
        start = dateutil.parser.isoparse(session["slot"]["start"]).replace(tzinfo=None)
        end = dateutil.parser.isoparse(session["slot"]["end"]).replace(tzinfo=None)
        try:
            type_answer_id = next(
                x["options"][0]["id"]
                for x in session["answers"]
                if x["question"]["id"] == 549
            )
        except (StopIteration, IndexError):
            type_answer_id = None
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
                "type": session_types[type_answer_id] if type_answer_id else None,
            },
            f,
        )

from PIL import Image
from io import BytesIO

for speaker in paginate("https://pretalx.com/api/events/pycon-au-2020/speakers/"):
    if speaker["code"] not in seen_speakers:
        continue
    has_pic = False
    try:
        if speaker["avatar"] is not None:
            im = Image.open(BytesIO(requests.get(speaker["avatar"]).content))
            im = im.convert("RGB")
            im.thumbnail((128, 128))
            im.save(f'assets/people/{speaker["code"]}.jpg')
            has_pic = True
    except Exception as e:
        print(speaker["code"], speaker["avatar"], e)
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
                "has_pic": has_pic,
            },
            f,
        )

