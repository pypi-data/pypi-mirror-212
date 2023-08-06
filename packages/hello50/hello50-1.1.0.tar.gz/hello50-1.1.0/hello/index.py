import json
import os.path

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')


def say_hi():
    return 'hello mother f'

def the_json():
    with open(f'{DB_PATH}/quran_uthmani.json', 'r', encoding="utf8") as file:
        return json.load(file)
