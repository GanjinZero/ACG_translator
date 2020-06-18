import os
import codecs
import re
from sklearn.utils import shuffle


def find_language_ass(language, text):
    language = language.lower()
    zh_mark = ["zh", "ch", "cn"]
    ja_mark = ["ja", "jp"]
    zh_ja_mark = ["Default"]
    special_mark = ["op", "ed"]
    for sp in special_mark:
        if language.find(sp) >= 0:
            return "special"
    for zh in zh_mark:
        if language.find(zh) >= 0:
            return "zh"
    for ja in ja_mark:
        if language.find(ja) >= 0:
            return "ja"
    for zh_ja in zh_ja_mark:
        if language.find(zh_ja) >= 0:
            return "zh_ja"
    return "Unknown"

def load_ass(file_path):
    f = codecs.open(file_path, 'r', encoding='utf-8', errors='ignore')
    lines = f.readlines()
    f.close()
    lines = [line for line in lines if line[0:8] == "Dialogue"]

    zh_list = []
    ja_list = []

    zh_temp_dict = {}
    ja_temp_dict = {}
    for line in lines:
        line_split = line.strip().split(",")
        """
        line_split:
        0 -> Dialogue: 1
        1 -> Start time -> 0:03:35.54
        2 -> End time -> 0:03:39.17
        3 -> Language -> text-ch
        ...
        -1 -> Text -> 你在想什么 天草四郎
        """
        time_code = line_split[1] + "|" + line_split[2]
        language = line_split[3]
        text = line_split[-1]
        lang = find_language_ass(language, text)
        if lang == "zh_ja":
            text = text.replace("\\N", "")
            text = re.sub(u"\\{.*?\\}", "\t", text)
            try:
                zh, ja = text.split("\t")
                zh_list.append(zh)
                ja_list.append(ja)
            except BaseException:
                pass
        else:
            text = re.sub(u"\\{.*?\\}", "", text)
            if lang == "zh":
                if time_code in ja_temp_dict:
                    zh_list.append(text)
                    ja_list.append(ja_temp_dict[time_code])
                    ja_temp_dict.pop(time_code)
                else:
                    zh_temp_dict[time_code] = text
            if lang == "ja":
                if time_code in zh_temp_dict:
                    zh_list.append(zh_temp_dict[time_code])
                    ja_list.append(text)
                    zh_temp_dict.pop(time_code)
                else:
                    ja_temp_dict[time_code] = text
    
    return zh_list, ja_list

def load_ass_all():
    zh_ass = []
    ja_ass = []
    for root, dirs, files in os.walk("./text/ass/"):
        for name in files:
            if len(name) > 4:
                if name[-4:] == ".ass":
                    zh_tmp, ja_tmp = load_ass(os.path.join(root, name))
                    zh_ass.extend(zh_tmp)
                    ja_ass.extend(ja_tmp)

    print(f"Load from ass:{len(zh_ass)}")

    return zh_ass, ja_ass

def load_lrc(file_path):
    f = codecs.open(file_path, 'r', encoding='utf-8', errors='ignore')
    lines = f.readlines()
    f.close()
    lines = [line.strip() for line in lines if line.find("|") != -1]
    zh_lrc = []
    ja_lrc = []
    for line in lines:
        st_index = line.find("]")
        use_line = line[st_index + 1:]
        try:
            ja_tmp, zh_tmp = use_line.split("|")
            if len(zh_tmp) > 0:
                zh_lrc.append(zh_tmp)
                ja_lrc.append(ja_tmp)
        except BaseException:
            pass
    
    return zh_lrc, ja_lrc

def load_lrc_all():
    zh_lrc = []
    ja_lrc = []
    for root, dirs, files in os.walk("./text/Lyrics/lrc/"):
        for name in files:
            if len(name) > 4:
                if name[-4:] == ".lrc":
                    zh_tmp, ja_tmp = load_lrc(os.path.join(root, name))
                    zh_lrc.extend(zh_tmp)
                    ja_lrc.extend(ja_tmp)

    print(f"Load from lyrics:{len(zh_lrc)}")

    return zh_lrc, ja_lrc

def load_zh_ja():
    zh_list = []
    ja_list = []
    f = codecs.open('./text/general/zh-ja.bicleaner05.txt', 'r', encoding='utf-8', errors='ignore')
    lines = f.readlines()
    f.close()

    for line in lines:
        _, _, zh, ja = line.strip().split("\t")
        zh_list.append(zh)
        ja_list.append(ja)

    print(f"Load from general:{len(zh_list)}")
    
    return zh_list, ja_list

def main():
    zh_all = []
    ja_all = []
    use_list = ["lrc", "ass", "general"]

    if "lrc" in use_list:
        zh_lrc, ja_lrc = load_lrc_all()
        zh_all.extend(zh_lrc)
        ja_all.extend(ja_lrc)

    if "ass" in use_list:
        zh_ass, ja_ass = load_ass_all()
        zh_all.extend(zh_ass)
        ja_all.extend(ja_ass)

    if "general" in use_list:
        zh_list, ja_list = load_zh_ja()
        zh_all.extend(zh_list)
        ja_all.extend(ja_list)

    # Add shuffle
    zh_all, ja_all = shuffle(zh_all, ja_all)

    with open("./text/zh.txt", "w", encoding="utf-8") as f:
        for line in zh_all:
            f.write(line + "\n")

    with open("./text/ja.txt", "w", encoding="utf-8") as f:
        for line in ja_all:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
