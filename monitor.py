import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Reloader(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None

    def on_modified(self, event):
        if event is None or event.src_path.endswith(self.script_path):
            print(f"{self.script_path} has been modified. Reloading...")
            if self.process:
                self.process.terminate()
            self.process = subprocess.Popen(["python", self.script_path])

def main():
    script_path = "webui.py"  # Replace with the path to your main script
    event_handler = Reloader(script_path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    # Initial run
    event_handler.on_modified(None)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
