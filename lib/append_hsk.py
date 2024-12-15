import csv
from tqdm import tqdm


def append_hsk(entries):
    hsk_levels = _load_hsk()

    # Pre-normalize entries and create a set for faster lookups
    entry_set = {
        (_normalise(entry.simplified), _normalise(entry.pinyin))
        for entry in entries
    }

    not_matching_levels = []
    for hsk_level in tqdm(hsk_levels):
        normalized_word = _normalise(hsk_level.word)
        normalized_pinyin = _normalise(hsk_level.pinyin)

        if (normalized_word, normalized_pinyin) in entry_set:
            # Update entry directly using set membership
            for entry in entries:
                if _normalise(entry.simplified) == normalized_word and _normalise(entry.pinyin) == normalized_pinyin:
                    if entry.hsk is None:
                        entry.hsk = {"2010": None, "2021": None}
                    entry.hsk["2010"] = hsk_level.hsk_2010 or entry.hsk["2010"]
                    entry.hsk["2021"] = hsk_level.hsk_2021 or entry.hsk["2021"]
                    break  # Exit inner loop once match is found
        else:
            not_matching_levels.append(hsk_level)

    unmatchable_levels = []
    for hsk_level in not_matching_levels:
        matching_entries = [
            entry
            for entry in entries
            if _normalise(entry.simplified) == _normalise(hsk_level.word)
        ]
        if len(matching_entries) == 1:
            entry = matching_entries[0]
            if entry.hsk is None:
                entry.hsk = {"2010": None, "2021": None}
            entry.hsk["2010"] = hsk_level.hsk_2010 or entry.hsk["2010"]
            entry.hsk["2021"] = hsk_level.hsk_2021 or entry.hsk["2021"]
        else:
            unmatchable_levels.append(hsk_level)

    for hsk_level in unmatchable_levels:
        print(f"{hsk_level.word}: {hsk_level.pinyin}")


def _normalise(input_string):
    normalised_input = (input_string
                        .replace(" ", "")
                        .replace(" ", "")
                        .replace("’", "")
                        .replace("·", "")
                        .replace("·", "")
                        .replace("¹", "")
                        .replace("²", "")
                        .replace("…", "")
                        .lower())

    return normalised_input


def _load_hsk():
    hsk_paths = {
        1: {
            "2010": r"data/hsk/hsk1.csv",
            "2021": r"data/hsk/HSK2021_1.csv",
        },
        2: {
            "2010": r"data/hsk/hsk2.csv",
            "2021": r"data/hsk/HSK2021_2.csv",
        },
        3: {
            "2010": r"data/hsk/hsk3.csv",
            "2021": r"data/hsk/HSK2021_3.csv",
        },
        4: {
            "2010": r"data/hsk/hsk4.csv",
            "2021": r"data/hsk/HSK2021_4.csv",
        },
        5: {
            "2010": r"data/hsk/hsk5.csv",
            "2021": r"data/hsk/HSK2021_5.csv",
        },
        6: {
            "2010": r"data/hsk/hsk6.csv",
            "2021": r"data/hsk/HSK2021_6.csv",
        }
    }

    hsk_levels = []
    for hsk_level in hsk_paths:
        old_hsk_path = hsk_paths[hsk_level]["2010"]
        new_hsk_path = hsk_paths[hsk_level]["2021"]

        with open(old_hsk_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                chinese = row["Chinese"]
                pinyin = row["Pinyin"]
                meaning = row["English"]
                # character sometimes contains "｜" which divides multiple words with the same level - 弟弟｜弟
                # character sometimes contains "（" + char + "）" to indicate who knows what - 白（形）
                words = chinese.split("｜")
                pinyins = pinyin.split("｜")
                for word in words:
                    pinyin = pinyins[words.index(word)].split("（")[0]
                    word = word.split("（")[0]
                    hsk_levels.append(HSKEntry(
                        word=word,
                        pinyin=pinyin,
                        meaning=meaning,
                        hsk_2010=hsk_level,
                        hsk_2021=None,
                    ))

        with open(new_hsk_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            for row in reader:
                chinese = row["Chinese"]
                pinyin = row["Pinyin"]
                meaning = row["English"]
                # character sometimes contains "｜" which divides multiple words with the same level - 弟弟｜弟
                # character sometimes contains "（" + char + "）" to indicate who knows what - 白（形）
                words = chinese.split("｜")
                pinyins = pinyin.split("｜")
                for word in words:
                    pinyin = pinyins[words.index(word)].split("（")[0]
                    word = word.split("（")[0]
                    hsk_levels.append(HSKEntry(
                        word=word,
                        pinyin=pinyin,
                        meaning=meaning,
                        hsk_2010=None,
                        hsk_2021=hsk_level,
                    ))

    return hsk_levels


class HSKEntry:
    def __init__(self, word, pinyin, meaning, hsk_2010, hsk_2021):
        self.word = word
        self.pinyin = pinyin
        self.meaning = meaning
        self.hsk_2010 = hsk_2010
        self.hsk_2021 = hsk_2021

# NOT FOUND IN CEDICT
#
# 车上 - chē shàng - in the car
# 好玩儿 - hǎo wánr - fun; interesting
# 面条儿 - miàn tiáor - noodles
# 那里 - nà lǐ - there
# 男孩儿 - nán háir - boy
# 女孩儿 - nǚ háir - girl
# 起来 - qǐlái - get up
# 小孩儿 - xiǎo háir - child; kid
# 一块儿 - yí kuàir - together
# 一下儿 - yí xiàr - a little bit
# 一点儿 - yīdiǎnr - a little bit
# 打篮球 - dá lán qiú - Play basketball
# 不太 - bú tài - not too; not very much
# 不一会儿 - bù yī huìr - in a moment; in a little while; soon
# 干活儿 - gànhuór - work on a job
# 见过 - jiàn guò - seen; have seen
# 快点儿 - kuài diǎnr - hurry up
# 送到 - sòng dào - sent to (place)
# 笑话儿 - xiào huàr - joke
# 有空儿 - yǒu kòngr - be free; at leisure
# 这时候 - zhè shí hou  - at this moment; at this time
# 放到 - fàng dào - put to; put into
# 纪录 - jìlù - Record
# 能不能 - néng bù néng - can or not
# 恶心 - ěxin - disgusting
# 名牌儿 - míng páir - famous brand
# 眼里 - yǎn lǐ - within one’s vision; in one’s eyes
# 有劲儿 - yǒu jìnr - strong; energetic
# 干活儿 - gàn huó r - to work
# 系领带 - jì lǐng dài - to tie one's necktie
# 纪录 - jì lù - record
# 使劲儿 - shǐ jìn ér - Rearing
# 城里 - chéng lǐ - inside the city; in town
# 大伙儿 - dàhuǒr - you all; everybody
# 胡同儿 - hú tòngr - alley; lane; bystreet
# 小偷儿 - xiǎo tōur - thief
# 一下儿 - yí xiàr - a little bit; a little while
# 大伙儿 - dà huǒ r - erhua variant of 大伙[dà huǒ]
# 啰唆 - luō suō - see 囉嗦|啰嗦[luō suo]
# 墨水儿 - mò shuǐ r - erhua variant of 墨水
# 纳闷儿 - nà mèn r - puzzled
# 纽扣儿 - niǔ kòu ér - Buttons children
# 摊儿 - tān r - erhua variant of 攤|摊[tān]
# 玩意儿 - wán yì r - erhua variant of 玩意[wán yì]
# 贤惠 - xián huì - chaste
# 馅儿 - xiàn r - erhua variant of 餡|馅
# 致力于 - zhì lì yú - Committed to
# 很难说 - hěn nán shuō - hard to say
# 聊天儿 - liáo tiānr - chat
# 一番 - yì fān - some; one time
# 指着 - zhǐ zhe - point; pointing
