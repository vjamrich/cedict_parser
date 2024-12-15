import json
import os

from lib.cedict_parser import CedictParser
from lib.get_dictionary import get_dictionary_as_uuids


def load_cedict():
    parser = CedictParser()
    entries = parser.parse()

    return entries


def save_cedict(entries, path="output", name="dict"):
    dictionary = get_dictionary_as_uuids(entries)

    os.makedirs(path, exist_ok=True)
    path = fr"{path}/{name}.json"
    with open(path, "w") as json_file:
        json.dump(
            dictionary,
            json_file,
            separators=(",", ":")
        )
