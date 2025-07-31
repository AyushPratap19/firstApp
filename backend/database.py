import json

def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)
