import os
from tqdm import tqdm
import sys
from load_zh_jp_transfer import load_transfer


zh2jp, jp2zh = load_transfer()
def convert_ja2zh(line):
    opt_line = []
    for ch in line:
        if ch in jp2zh:
            opt_line.append(jp2zh[ch])
        else:
            opt_line.append(ch)
    return "".join(opt_line)

def search_list(lines, target):
    output_index = []
    output_index_dict = {}
    for index, line in enumerate(lines):
        target_count = line.count(target)
        if target_count > 0:
            output_index_dict[index] = target_count
            output_index.append(index)
    return output_index, output_index_dict

def split_list(original, split):
    # return original-split
    if len(split) == 0:
        #print(original)
        return [original]

    output_list = []
    for i in range(len(split)):
        if i == 0:
            if split[i][0] == 0:
                output_list.append([])
            else:
                output_list.append(original[0:split[i][0]])
        else:
            output_list.append(original[split[i-1][-1] + 1:split[i][0]])
        if i == len(split) - 1:
            if split[i] == len(original):
                output_list.append([])
            else:
                output_list.append(original[split[i][-1] + 1:])
    return output_list
    

def match(zh_lines, ja_lines, level=0):
    """
    Match Priority:
    ◆
    「」
    Equal name
    。
    len(zh_lines) == len(ja_lines)
    """
    #print(len(zh_lines), len(ja_lines), level)

    if len(zh_lines) == 0 or len(ja_lines) == 0 or level > 4:
        return [], []
    if isinstance(zh_lines, str) and isinstance(ja_lines, str):
        return [zh_lines], [ja_lines]
    if len(zh_lines) == len(ja_lines) == 1:
        return zh_lines, ja_lines

    all_match_zh = []
    all_match_ja = []

    if level == 0:
        zh_index, _ = search_list(zh_lines, "◆")
        ja_index, _ = search_list(ja_lines, "◆")
        zh_index = [[x] for x in zh_index]
        ja_index = [[x] for x in ja_index]
        if len(zh_index) == len(ja_index):
            new_zh_line_list = split_list(zh_lines, zh_index)
            new_ja_line_list = split_list(ja_lines, ja_index)
            all_match_zh = [zh_lines[index[0]] for index in zh_index]
            all_match_ja = [ja_lines[index[0]] for index in ja_index]
        else:
            new_zh_line_list = zh_lines
            new_ja_line_list = ja_lines

    if level == 1:
        zh_left_index, _ = search_list(zh_lines, "「")
        zh_right_index, _ = search_list(zh_lines, "」")
        ja_left_index, _ = search_list(ja_lines, "「")
        ja_right_index, _ = search_list(ja_lines, "」")
        zh_index = []
        ja_index = []
        if len(zh_left_index) == len(zh_right_index) == len(ja_left_index) == len(ja_right_index):
            for i in range(len(zh_left_index)):
                all_match_zh.append("".join(zh_lines[zh_left_index[i]:zh_right_index[i]+1]))
                all_match_ja.append("".join(ja_lines[ja_left_index[i]:ja_right_index[i]+1]))
                zh_index.append(list(range(zh_left_index[i], zh_right_index[i]+1)))
                ja_index.append(list(range(ja_left_index[i], ja_right_index[i]+1)))
            new_zh_line_list = split_list(zh_lines, zh_index)
            new_ja_line_list = split_list(ja_lines, ja_index)
        else:
            new_zh_line_list = zh_lines
            new_ja_line_list = ja_lines

    if level == 2:
        ja_lines_new = [convert_ja2zh(line) for line in ja_lines]
        now_start = 0
        zh_index = []
        ja_index = []
        for i in range(len(zh_lines)):
            for j in range(now_start, len(ja_lines)):
                if zh_lines[i] == ja_lines_new[j] and 1 <= len(zh_lines[i]):
                    zh_index.append([i])
                    ja_index.append([j])
                    all_match_zh.append(zh_lines[i])
                    all_match_ja.append(ja_lines[j])
                    now_start = j
                    continue
        new_zh_line_list = split_list(zh_lines, zh_index)
        new_ja_line_list = split_list(ja_lines, ja_index)

    if level == 3:
        zh_punc_index, zh_punc_index_dict = search_list(zh_lines, "。")
        ja_punc_index, ja_punc_index_dict = search_list(ja_lines, "。")
        zh_punc_count = 0
        ja_punc_count = 0
        j = -1
        zh_index = []
        ja_index = []
        if sum(zh_punc_index_dict.values()) == sum(ja_punc_index_dict.values()):
            for i in zh_punc_index:
                zh_punc_count += zh_punc_index_dict[i]
                while ja_punc_count < zh_punc_count:
                    j += 1
                    ja_punc_count += ja_punc_index_dict[ja_punc_index[j]]
                if zh_punc_index_dict[i] == ja_punc_index_dict[ja_punc_index[j]] and ja_punc_count == zh_punc_count:
                    zh_index.append([i])
                    ja_index.append([ja_punc_index[j]])
                    all_match_zh.append(zh_lines[i])
                    all_match_ja.append(ja_lines[ja_punc_index[j]])
        new_zh_line_list = split_list(zh_lines, zh_index)
        new_ja_line_list = split_list(ja_lines, ja_index)


    if level == 4:
        if len(zh_lines) == len(ja_lines) and len(zh_lines) <= 10:
            return zh_lines, ja_lines
        else:
            return [], []
    
    #if not len(new_zh_line_list) == len(new_ja_line_list):
    #    print(len(zh_lines), len(ja_lines), len(zh_index), len(ja_index), level, len(new_zh_line_list), len(new_ja_line_list))


    sub_result = [match(new_zh_line_list[i], new_ja_line_list[i], level + 1) for i in range(len(new_zh_line_list))]
    for res in sub_result:
        all_match_zh.extend(res[0])
        all_match_ja.extend(res[1])
    #print(len(all_match_zh))
    return all_match_zh, all_match_ja


def align_dc2pc():
    os.system("touch ./dc2pc_zh.txt")
    os.system("touch ./dc2pc_ja.txt")

    zh_all = []
    ja_all = []

    all_zh_count = 0
    all_ja_count = 0
    match_count = 0
    for file in tqdm(os.listdir("./dc2pc")):
        if file[-2:] == "zh":
            zh_file = file
            ja_file = file[0:-2] + "ja"
            with open(f"./dc2pc/{zh_file}", "r", encoding="utf-8") as f:
                zh_lines = f.readlines()
            with open(f"./dc2pc/{ja_file}", "r", encoding="utf-8") as f:
                ja_lines = f.readlines()
            zh_lines = [line.replace("\n", "").replace("\r", "") for line in zh_lines]
            ja_lines = [line.replace("\n", "").replace("\r", "") for line in ja_lines]
        
            zh_match, ja_match = match(zh_lines, ja_lines)
            zh_all.extend(zh_match)
            ja_all.extend(ja_match)
            all_zh_count += len(zh_lines)
            all_ja_count += len(ja_lines)
            match_count += len(zh_match)

    with open("./dc2pc_zh.txt", "w", encoding="utf-8") as f:
        for line in zh_all:
            f.write(line.strip() + "\n")
    with open("./dc2pc_ja.txt", "w", encoding="utf-8") as f:
        for line in ja_all:
            f.write(line.strip() + "\n")

    print("Zh lines:", all_zh_count)
    print("Ja lines:", all_ja_count)
    print("Match lines:", match_count)

def main():
    align_dc2pc()

if __name__ == "__main__":
    main()
