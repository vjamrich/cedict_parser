import re


def remove_variants(entries):
    for entry in entries:
        old_meanings = entry.meanings
        new_meanings = []
        for meaning_index in range(len(old_meanings)):
            meaning = old_meanings[meaning_index]
            if "CL:" in meaning:
                extracted_meaning = re.sub(r"\(CL:.*?\)", "", meaning).strip()
                if extracted_meaning != meaning:
                    new_meanings.append(extracted_meaning)
            elif "variant of" not in meaning:
                new_meanings.append(meaning)
        entry.meanings = new_meanings

    filtered_entries = []
    for entry_index in range(len(entries)):
        entry = entries[entry_index]
        if len(entry.meanings) > 0:
            filtered_entries.append(entry)

    return filtered_entries
