def remove_variants(entries):
    for entry in entries:
        old_meanings = entry.meanings
        new_meanings = []
        for meaning_index in range(len(old_meanings)):
            meaning = old_meanings[meaning_index]
            if "variant of" not in meaning:
                new_meanings.append(meaning)
        entry.meanings = new_meanings

    filtered_entries = []
    for entry_index in range(len(entries)):
        entry = entries[entry_index]
        if len(entry.meanings) > 0:
            filtered_entries.append(entry)

    return filtered_entries
