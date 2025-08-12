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
PRETALX_EVENT_SHORT_FORM = "pycon-au-2025"
EVENT_TIMEZONE = dateutil.tz.gettz("Australia/Melbourne")
ROOMS = {
    "Ballroom 1": "ballroom1",
    "Ballroom 2": "ballroom2",
    "Ballroom 3": "ballroom3",
    "Junior Ballroom": "juniorballroom",
    "Stradbroke Room": "stradbroke",
}
TRACKS = {
    "Data & AI": "data-ai",
    "Education": "education",
    "Scientific Python": "scientific",
    "Main Conference": None,
    "Development Sprints": None
}
# Question IDs
CONTENT_WARNING_QUESTION_ID = 5326
PRONOUNS_QUESTION_ID = 5332
BLUESKY_QUESTION_ID = 5329
FEDIVERSE_QUESTION_ID = 5328

TAG_IDS_TO_SKIP = {1679}

NDV_JSON = "https://portal.nextdayvideo.com.au/main/C/pyconau/S/pyconau_2025.json"

# End per-year configuration

PRETALX_BASE_URL = f"https://pretalx.com/api/events/{PRETALX_EVENT_SHORT_FORM}"
CONTENT_DIR = pathlib.Path("../src/content")
SESSIONS_DIR = CONTENT_DIR / "sessions"
BREAKS_DIR = CONTENT_DIR / "breaks"
PEOPLE_DIR = CONTENT_DIR / "people"
PUBLIC_DIR = pathlib.Path("../public")
PEOPLE_IMGS_DIR = PUBLIC_DIR / "people"

yaml = YAML()
md = Markdown()


def paginate(url, pretalx_version="LEGACY"):
    next_url = url
    while next_url:
        res = requests.get(
            next_url,
            headers={
                "Authorization": f"Token {PRETALX_TOKEN}",
                "Pretalx-Version": pretalx_version,
            },
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

def get_answer(question_id, speaker_code=None, submission_code=None):
    if speaker_code:
        response = requests.get(
            f"{PRETALX_BASE_URL}/answers/?person={speaker_code}&question={question_id}",
            headers={"Authorization": f"Token {PRETALX_TOKEN}"},
        )
    elif submission_code:
        response = requests.get(
            f"{PRETALX_BASE_URL}/answers/?submission={submission_code}&question={question_id}",
            headers={"Authorization": f"Token {PRETALX_TOKEN}"},
        )
    else:
        raise Exception("Need a code to get an answer")
    if response.ok:
        data = response.json()
        if data["count"] > 0:
            return data["results"][0]["answer"]
    return None

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
    "Education Keynote": "education-keynote",
    "Flash talk": "flash-talk",
    "Waitlist": "waitlist",
    "Backup": "backup",
}

seen_speakers = set()

yt_resp = requests.get(NDV_JSON)
if yt_resp.ok:
    youtube_slugs = {
        x["conf_key"]: x["host_url"].rsplit("/", 1)[1]
        for x in yt_resp.json()
        if x["host_url"] is not None
    }
else:
    youtube_slugs = {}

for entry in SESSIONS_DIR.glob("*"):
    entry.unlink()


for session in paginate(
    f"{PRETALX_BASE_URL}/submissions/?state=confirmed"
):
    print(f"session {session['code']}")
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
    cw = get_answer(CONTENT_WARNING_QUESTION_ID, submission_code=session['code'])
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
                "youtube_slug": youtube_slugs.get(session["code"]),
            },
            f,
        )

BREAKS_DIR.mkdir(exist_ok=True)
for entry in BREAKS_DIR.glob("*"):
    entry.unlink()

# If a schedule is published, collect breaks
schedule = requests.get(
    f"{PRETALX_BASE_URL}/schedules/latest/",
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
    f"{PRETALX_BASE_URL}/speakers/",
    pretalx_version='v1'
):
    if speaker["code"] not in seen_speakers:
        continue
    print(f"speaker {speaker['code']}")
    has_pic = False
    try:
        if speaker["avatar_url"] is not None:
            etag = etags.get(speaker["code"], None)
            if speaker["avatar_url"]:
                avatar_resp = requests.get(
                    speaker["avatar_url"],
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
        print(speaker["code"], speaker["avatar_url"], e)

    speaker_file = PEOPLE_DIR / f'{speaker["code"]}.yml'
    with speaker_file.open("w") as f:
        yaml.dump(
            {
                "name": speaker["name"],
                "pronouns": get_answer(PRONOUNS_QUESTION_ID, speaker_code=speaker["code"]),
                "bluesky": get_answer(BLUESKY_QUESTION_ID, speaker_code=speaker["code"]),
                "fedi": get_answer(FEDIVERSE_QUESTION_ID, speaker_code=speaker["code"]),
                "bio": parse_markdown(speaker["biography"] or ""),
                "has_pic": has_pic,
            },
            f,
        )

with (CONTENT_DIR / "_people_etags.yml").open("w") as f:
    yaml.dump(etags, f)
