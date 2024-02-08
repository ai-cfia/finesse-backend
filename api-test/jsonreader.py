import json
from typing import Iterator, Dict
import os

class JSONReader(Iterator):
    "Read test data from JSON files using an iterator"

    def __init__(self, directory):
        self.directory = directory
        self.file_list = [f for f in os.listdir(directory) if f.endswith('.json')]
        if not self.file_list:
            raise FileNotFoundError(f"No JSON files found in the directory '{directory}'")
        self.current_file_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_file_index >= len(self.file_list):
            raise StopIteration

        file_path = os.path.join(self.directory, self.file_list[self.current_file_index])

        with open(file_path, 'r') as f:
            data = json.load(f)
            self.current_file_index += 1
            return data


class JSONDictReader(Iterator[Dict]):
    "Read test data from JSON files using an iterator, returns rows as dicts"

    def __init__(self, directory):
        self.reader = JSONReader(directory)

    def __iter__(self):
        return self

    def __next__(self):
        data = next(self.reader)
        if isinstance(data, list):
            return data[0]  # Assuming each JSON file contains a list of dictionaries
        elif isinstance(data, dict):
            return data
        else:
            raise ValueError("Invalid JSON format")

