import time

from lib.append_hsk import append_hsk
from lib.file_operations import load_cedict, save_cedict
from lib.generate_sentences import generate_sentences
from lib.generate_sounds import generate_sounds
from lib.remove_variants import remove_variants
from lib.simplify_entries import simplify_entries


def main():
    print("starting script...")
    timestamp = int(time.time())
    print(timestamp)

    print("Loading vocabulary...")
    entries = load_cedict()

    print("Simplifying entries...")
    entries = simplify_entries(entries)

    print("Removing variants...")
    entries = remove_variants(entries)

    print("Appending HSK levels...")
    append_hsk(entries)

    print("Saving modified dictionary checkpoint...")
    save_cedict(entries, f"output/{timestamp}", "dict_checkpoint")

    print("Generating sentences...")
    # TODO
    # generate_sentences(entries, 1)

    print("Saving modified dictionary with sentences...")
    # save_cedict(entries, f"output/{timestamp}", "dict")

    print("Generating vocabulary sounds...")
    # generate_sounds(entries)

    print("Generating example sentence sounds...")
    # TODO
    # One character can differ

    print("...ending script")


if __name__ == '__main__':
    main()
