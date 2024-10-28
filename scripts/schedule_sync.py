import pathlib
from io import BytesIO
from os import environ

import bleach
import dateutil.parser
import dateutil.tz
import requests
from markdown import Markdown
from PIL import Image
from ruamel.yaml import YAML

PRETALX_TOKEN = environ["PRETALX_TOKEN"]

# Per-year configuration
EVENT_TIMEZONE = dateutil.tz.gettz("Australia/Melbourne")
ROOMS = {
    "Goldfields Theatre": "goldfields",
    "Eureka 2": "eureka2",
    "Eureka 3": "eureka3",
    "Chancellor 2 at the Grand Chancellor Hotel": "chancellor2",
    "Chancellor 4 at the Grand Chancellor Hotel": "chancellor4",
}
TRACKS = {
    "DevOops": "devoops",
    "Education": "education",
    "Scientific Python": "scientific",
    "Main Conference": None,
}
# Question IDs
# Question IDs on the *people* object
PRONOUN_QUESTION_ID = 3948
TWITTER_QUESTION_ID = 3950
FEDIVERSE_QUESTION_ID = 3949

# End per-year configuration

CONTENT_DIR = pathlib.Path("../src/content")
SESSIONS_DIR = CONTENT_DIR / "sessions"
BREAKS_DIR = CONTENT_DIR / "breaks"
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


answers = {
    "Content Warning": 3747,
}

# format_answer = {
#     1062: "L",  # live
#     1063: "P",  # prerecord
# }

types = {
    "Talk": "talk",
    # "PyCon Fair stall": "stall",
    "Opening/Closing": "open-close",
    "Special": "special",
    "Keynote": "keynote",
    "Waitlist": "waitlist",
    "Backup": "backup",
}

seen_speakers = set()

# yt_resp = requests.get(
#     "https://portal.nextdayvideo.com.au/main/C/pyconau/S/pyconau_2021.json"
# )
# yt_resp.raise_for_status()
# youtube_slugs = {
#     x["conf_key"]: x["host_url"].rsplit("/", 1)[1]
#     for x in yt_resp.json()
#     if x["host_url"] is not None
# }

for entry in SESSIONS_DIR.glob("*"):
    entry.unlink()


for session in paginate(
    "https://pretalx.com/api/events/pycon-au-2024/submissions/?state=confirmed&questions=3747"
):
    # Do not schedule backups
    # TODO manually add backups if they are unscheduled after the event.
    # if rooms[session["slot"]["room"]["en"]] == 0:
    #    print("not scheduling backup")
    #    continue

    if TAG_IDS_TO_SKIP.intersection(session["tag_ids"]):
        print("skipping due to tag id")
        continue

    speakers = [x["code"] for x in session["speakers"]]
    seen_speakers.update(speakers)
    if session["slot"] and session["slot"]["start"] and session["slot"]["end"]:
        start = dateutil.parser.isoparse(session["slot"]["start"]).astimezone(
            EVENT_TIMEZONE
        )
        end = dateutil.parser.isoparse(session["slot"]["end"]).astimezone(
            EVENT_TIMEZONE
        )
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
    track = session["track"]
    if track is None:
        print(f"!!! {session['code']} has no track assigned, skipping")
        continue
    elif "(waitlist)" in track["en"]:
        print(f"{session['code']} is waitlisted, skipping")
        continue
    else:
        track = TRACKS[track["en"]]

    with (SESSIONS_DIR / f'{session["code"]}.yml').open("w") as f:
        yaml.dump(
            {
                "title": session["title"],
                "start": start,
                "end": end,
                "room": ROOMS[session["slot"]["room"]["en"]]
                if session["slot"] and session["slot"]["room"]
                else None,
                "track": track,
                # "type": types[session["submission_type"]["en"]],
                # "type": type_answer_id,
                "abstract": parse_markdown(session["abstract"]),
                "description": parse_markdown(session["description"]),
                "code": session["code"],
                "speakers": speakers,
                "cw": parse_markdown(cw) if cw is not None else None,
                # "youtube_slug": youtube_slugs.get(session["code"]),
            },
            f,
        )

BREAKS_DIR.mkdir(exist_ok=True)
for entry in BREAKS_DIR.glob("*"):
    entry.unlink()

# If a schedule is published, collect breaks
schedule = requests.get(
    "https://pretalx.com/api/events/pycon-au-2024/schedules/latest/",
    headers={"Authorization": f"Token {PRETALX_TOKEN}"},
)
if schedule.ok:
    for break_ in schedule.json()["breaks"]:
        # We only want to copy across breaks that aren't actually breaks
        description = break_["description"]["en"]
        if "break" in description.lower() or "lunch" in description.lower():
            continue

        with (
            BREAKS_DIR / f"{break_['room_id']}-{break_['start'].replace(':','-')}.yml"
        ).open("w") as f:
            start = dateutil.parser.isoparse(break_["start"]).astimezone(EVENT_TIMEZONE)
            end = dateutil.parser.isoparse(break_["end"]).astimezone(EVENT_TIMEZONE)
            yaml.dump(
                {
                    "room": ROOMS[break_["room"]["en"]],
                    "start": start,
                    "end": end,
                    "description": break_["description"]["en"],
                },
                f,
            )


PEOPLE_IMGS_DIR.mkdir(exist_ok=True)

with (CONTENT_DIR / "_people_etags.yml").open("r") as f:
    etags = yaml.load(f)

# etags none? ensure empty
if not etags:
    etags = {}

for speaker in paginate(
    f"https://pretalx.com/api/events/pycon-au-2024/speakers/?questions={PRONOUN_QUESTION_ID},{FEDIVERSE_QUESTION_ID},{TWITTER_QUESTION_ID}"
):
    if speaker["code"] not in seen_speakers:
        continue
    has_pic = False
    try:
        if speaker["avatar"] is not None:
            etag = etags.get(speaker["code"], None)
            print(speaker["avatar"])
            if not speaker["avatar"]:
                continue
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
                im.thumbnail((225, 225))
                im.save(str(PEOPLE_IMGS_DIR / f'{speaker["code"]}.jpg'), quality=95)
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
                        if x["question"]["id"] == PRONOUN_QUESTION_ID
                    ),
                    None,
                ),
                "twitter": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == TWITTER_QUESTION_ID
                    ),
                    None,
                ),
                "fedi": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == FEDIVERSE_QUESTION_ID
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
