from lib.cedict_parser import CedictEntry
from lib.get_dictionary import get_dictionary


def simplify_entries(entries):
    dictionary = get_dictionary(entries)

    simplified_entries = []
    for key, value in dictionary.items():
        new_entries = []
        group_key = []
        for entry in value:
            new_entry = CedictEntry.make(entry["raw_line"])
            new_entries.append(new_entry)
            group_key.append(entry["simplified"] + entry["traditional"] + entry["pinyin"])

        if len(group_key) != len(set(group_key)):
            grouped_entries = {}
            repeating_entries = dictionary[key]
            for entry in repeating_entries:
                grouped_key = entry["simplified"] + entry["traditional"]
                if grouped_key in grouped_entries:
                    grouped_entries[grouped_key].append(entry)
                else:
                    grouped_entries[grouped_key] = [entry]

            merged_entries = []
            for _, entries in grouped_entries.items():
                unique_pinyin_entries = {}
                for entry in entries:
                    if entry["pinyin"] not in unique_pinyin_entries:
                        unique_pinyin_entries[entry["pinyin"]] = CedictEntry.make(entry["raw_line"])
                        unique_pinyin_entries[entry["pinyin"]].raw_line = None
                    else:
                        unique_pinyin_entries[entry["pinyin"]].meanings += entry["meanings"]

                for _, entry in unique_pinyin_entries.items():
                    # Put extra long meanings at the end
                    for meaning in entry.meanings:
                        if len(meaning) > 64:
                            entry.meanings.remove(meaning)
                            entry.meanings.append(meaning)
                    # Put surnames at the end - even behind all the long meanings
                    for meaning in entry.meanings:
                        if "surname " in meaning:
                            entry.meanings.remove(meaning)
                            entry.meanings.append(meaning)

                    merged_entries.append(entry)

            # add grouped_entries to simplified_entries
            simplified_entries += merged_entries

        else:
            simplified_entries += new_entries

    return simplified_entries
