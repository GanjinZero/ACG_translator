import os
from resource.load_zh_jp_transfer import load_transfer


zh2jp, jp2zh = load_transfer()

def convert_ja2zh(line):
    opt_line = []
    for ch in line:
        if ch in jp2zh:
            opt_line.append(jp2zh[ch])
        else:
            opt_line.append(ch)
    return "".join(opt_line)

def main():
    with open("./text/zh_segment.txt", "r", encoding="utf-8") as f:
        zh_lines = f.readlines()
    with open("./text/ja_segment.txt", "r", encoding="utf-8") as f:
        ja_lines = f.readlines()
    ja_lines_new = [convert_ja2zh(line) for line in ja_lines]
    with open("./text/bpe_train.txt", "w", encoding="utf-8") as f:
        for line in zh_lines:
            f.write(line.strip() + "\n")
        for line in ja_lines_new:
            f.write(line.strip() + "\n")
    os.system("subword-nmt learn-bpe -s 40000 < ./text/bpe_train.txt > ./bpe_model/zh_ja.model")
