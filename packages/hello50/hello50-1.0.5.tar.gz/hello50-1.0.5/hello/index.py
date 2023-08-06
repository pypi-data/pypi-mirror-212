import json

def say_hi():
    return 'hello mother f'

def the_json():
    with open('./quran_uthmani.json', 'r', encoding="utf8") as file:
        return json.load(file)
