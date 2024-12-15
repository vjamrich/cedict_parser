import uuid


def get_dictionary(entries):
    dictionary = {}
    for entry in entries:
        simplified = entry.simplified
        if simplified not in dictionary:
            dictionary[simplified] = []

        entry_map = {
            "simplified": entry.simplified,
            "traditional": entry.traditional,
            "pinyin": entry.pinyin,
            "meanings": entry.meanings,
            "raw_line": entry.raw_line,
        }
        if entry.hsk is not None:
            entry_map["hsk"] = entry.hsk
        if entry.sentence is not None:
            entry_map["sentence"] = entry.sentence

        dictionary[simplified].append(entry_map)

    return dictionary


def get_dictionary_as_uuids(entries):
    dictionary = {}
    for entry in entries:
        entry_map = {
            "simplified": entry.simplified,
            "traditional": entry.traditional,
            "pinyin": entry.pinyin,
            "meanings": entry.meanings,
        }
        if entry.hsk is not None:
            entry_map["hsk"] = entry.hsk
        if entry.sentence is not None:
            entry_map["sentence"] = entry.sentence

        key = str(uuid.uuid5(
            namespace=uuid.NAMESPACE_X500,
            name=f"{entry.simplified}_{entry.traditional}_{entry.pinyin.replace(' ', '')}",
        ))

        if key in dictionary:
            print("ERROR, THE SAVED KEYS ARE NOT UNIQUE")
        dictionary[key] = entry_map

    return dictionary
