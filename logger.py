import json
import time

class Logger:
    def __init__(self, filename="telemetry.json"):
        self.filename = filename
        self.file = open(self.filename, "w", encoding="utf-8")

    def log(self, data):
        """Adds a timestamp and writes the dictionary with 4-space indentation."""
        data["timestamp"] = time.time()

        pretty_json = json.dumps(data, indent=4, sort_keys=True)

        self.file.write(pretty_json + "\n\n")
        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()
