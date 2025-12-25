import json
import os
import sys

include_path = os.path.join(os.getcwd(), "src")
sys.path.insert(0, include_path)


class ReadMockFile:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.mock_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
        self.file = os.path.join(self.mock_path, self.file_name)

        with open(self.file, "r") as f:
            self.mock_parsed = f.read()
            if ".json" in self.file_name:
                self.mock_parsed = json.loads(self.mock_parsed)
