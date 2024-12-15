"""
Parser for dictionary meanings to find and replace all pinyin withing them
"""


from lib.decode_pinyin import *


def decode_meanings(meanings):
    meanings_copy = meanings

    for meaning_index in range(len(meanings)):
        meaning = meanings[meaning_index]
        results = re.findall(r'\[(.*?)]', meaning)
        for result_index in range(len(results)):
            result = results[result_index]
            if has_numbers(result):
                meanings_copy[meaning_index] = meanings_copy[meaning_index].replace(result, decode_pinyin(result))

    return meanings_copy
