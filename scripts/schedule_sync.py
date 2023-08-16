import os
import os.path
import pathlib
from datetime import timedelta
from os import environ
from pprint import pprint

import bleach
import dateutil.parser
import dateutil.tz
import requests
from markdown import Markdown
from parse import parse
from ruamel.yaml import YAML

PRETALX_TOKEN = environ["PRETALX_TOKEN"]
ACST = dateutil.tz.gettz("Australia/Adelaide")
CONTENT_DIR = pathlib.Path("../src/content")
SESSIONS_DIR = CONTENT_DIR / "sessions"
PEOPLE_DIR = CONTENT_DIR / "people"
PUBLIC_DIR = pathlib.Path("../public")
PEOPLE_IMGS_DIR = PUBLIC_DIR / "people"

TAG_IDS_TO_SKIP = {798}

yaml = YAML()
md = Markdown()


def paginate(url):
    next_url = url
    while next_url:
        res = requests.get(
            next_url,
            headers={"Authorization": f"Token {PRETALX_TOKEN}"},
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
            "s",
            "del",
            "ins",
        ),
    )


rooms = {
    "Hall A": "a",
    "Hall B": "b",
    "Hall C (Plenary)": "c",
    "Hall E": "e",
}

tracks = {
    "Our Connected Universe": "ocu",
    "All Things Data!": "data",
    "Education": "education",
    "DjangoCon AU": "djangocon",
    "Main Conference": None,
}

answers = {
    "Presentation Format": 853,
    "Content Warning": 2459,
    "Pronouns": 2461,
    "Twitter": 2455,
    "Fedi": 2506,
}

format_answer = {
    1062: "L",  # live
    1063: "P",  # prerecord
}

types = {
    "Talk": "talk",
    "PyCon Fair stall": "stall",
    "Opening/Closing": "open-close",
    "Special": "special",
    "Keynote": "keynote",
}

seen_speakers = set()

yt_resp = requests.get(
    "https://portal.nextdayvideo.com.au/main/C/pyconau/S/pyconau_2021.json"
)
yt_resp.raise_for_status()
youtube_slugs = {
    x["conf_key"]: x["host_url"].rsplit("/", 1)[1]
    for x in yt_resp.json()
    if x["host_url"] is not None
}

for entry in SESSIONS_DIR.glob("*"):
    entry.unlink()


for session in paginate(
    "https://pretalx.com/api/events/pyconau-2023/submissions/?state=confirmed&questions=2459"
):
    # Do not schedule backups
    # TODO manually add backups if they are unscheduled after the event.
    # if rooms[session["slot"]["room"]["en"]] == 0:
    #    print("not scheduling backup")
    #    continue
    print(session["code"])

    if TAG_IDS_TO_SKIP.intersection(session["tag_ids"]):
        print("skipping due to tag id")
        continue

    speakers = [x["code"] for x in session["speakers"]]
    seen_speakers.update(speakers)
    with (SESSIONS_DIR / f'{session["code"]}.yml').open("w") as f:
        if session["slot"] and session["slot"]["start"] and session["slot"]["end"]:
            start = dateutil.parser.isoparse(session["slot"]["start"]).astimezone(ACST)
            end = dateutil.parser.isoparse(session["slot"]["end"]).astimezone(ACST)
        else:
            start = None
            end = None
        # type_answer_id = format_answer[next(
        #        x["options"][0]["id"] for x in session["answers"] if x["question"]["id"] == answers["Presentation Format"]
        #    )]
        cw = next(
            (
                x["answer"]
                for x in session["answers"]
                if x["question"]["id"] == answers["Content Warning"]
            ),
            None,
        )
        twitter = next(
            (
                x["answer"]
                for x in session["answers"]
                if x["question"]["id"] == answers["Twitter"]
            ),
            None,
        )
        fedi = next(
            (
                x["answer"]
                for x in session["answers"]
                if x["question"]["id"] == answers["Fedi"]
            ),
            None,
        )
        track = session["track"]
        if track is not None:
            track = tracks[track["en"]]
        else:
            print(f"!!! {session['code']} has no track assigned")
        yaml.dump(
            {
                "title": session["title"],
                "start": start,
                "end": end,
                "room": rooms[session["slot"]["room"]["en"]]
                if session["slot"] and session["slot"]["room"]
                else None,
                "track": track,
                "type": types[session["submission_type"]["en"]],
                # "type": type_answer_id,
                "abstract": parse_markdown(session["abstract"]),
                "description": parse_markdown(session["description"]),
                "code": session["code"],
                "speakers": speakers,
                "cw": parse_markdown(cw) if cw is not None else None,
                "youtube_slug": youtube_slugs.get(session["code"]),
            },
            f,
        )

from io import BytesIO

from PIL import Image

with (CONTENT_DIR / "_people_etags.yml").open("r") as f:
    etags = yaml.load(f)

# etags none? ensure empty
if not etags:
    etags = {}

for speaker in paginate(
    "https://pretalx.com/api/events/pyconau-2023/speakers/?questions=2461,2455,2506"
):
    if speaker["code"] not in seen_speakers:
        continue
    has_pic = False
    try:
        if speaker["avatar"] is not None:
            etag = etags.get(speaker["code"], None)
            print(speaker["avatar"])
            avatar_resp = requests.get(
                speaker["avatar"],
                headers={"If-None-Match": etag} if etag is not None else {},
            )
            if avatar_resp.status_code == 304:
                print("ETag match")
                has_pic = True
            else:
                avatar_resp.raise_for_status()
                if "ETag" in avatar_resp.headers:
                    etags[speaker["code"]] = avatar_resp.headers["ETag"]
                im = Image.open(BytesIO(avatar_resp.content))
                im = im.convert("RGB")
                im.thumbnail((128, 128))
                im.save(str(PEOPLE_IMGS_DIR / f'{speaker["code"]}.jpg'))
                has_pic = True
    except Exception as e:
        print(speaker["code"], speaker["avatar"], e)

    speaker_file = PEOPLE_DIR / f'{speaker["code"]}.yml'
    with speaker_file.open("w") as f:
        yaml.dump(
            {
                "name": speaker["name"],
                "pronouns": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == answers["Pronouns"]
                    ),
                    None,
                ),
                "twitter": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == answers["Twitter"]
                    ),
                    None,
                ),
                "fedi": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == answers["Fedi"]
                    ),
                    None,
                ),
                "bio": parse_markdown(speaker["biography"] or ""),
                "has_pic": has_pic,
            },
            f,
        )

with (CONTENT_DIR / "_people_etags.yml").open("w") as f:
    yaml.dump(etags, f)
