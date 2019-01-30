import json

def read(path: str) -> dict:
    with open(path, 'r') as fh:
        return json.load(fh)
