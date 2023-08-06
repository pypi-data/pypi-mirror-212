import json, requests
import os.path

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')


def say_hi():
    return 'hello mother f'

def the_json():
    print(DB_PATH)
    with open(f'{DB_PATH}/quran_simple.json', 'r', encoding="utf8") as file:
        return json.load(file)

def req():
    return requests.get('https://api.quran.com/api/v4/quran/verses/uthmani').json()