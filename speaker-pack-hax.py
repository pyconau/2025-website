import jinja2
import itertools
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from os.path import split

TEMPLATE = 'data/SpeakerPack/_template.md.j2'

def rebuild():
    with open(TEMPLATE) as f:
        templ = jinja2.Template(f.read())

    for typ, room, day in itertools.product(('pre-record', 'live'), ('curlyboi', 'other'), ('specialist', 'main')):
        with open(f'data/SpeakerPack/{typ}-{room}-{day}.md', 'w') as f:
            f.write(templ.render({'type': typ, 'room': room, 'day': day}))
    pass

def watch():
    rebuild()
    class Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.src_path == TEMPLATE:
                print('Rebuilding speaker packs')
                rebuild()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, split(TEMPLATE)[0])
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'watch':
        watch()
    else:
        rebuild()