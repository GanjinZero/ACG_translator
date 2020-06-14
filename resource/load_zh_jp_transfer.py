import os


def load_transfer():
    with open("./resource/zh_jp_transfer.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip() != ""]

    zh2jp = dict()
    jp2zh = dict()

    for i in range(len(lines) // 2):
        c_line = lines[i * 2]
        j_line = lines[i * 2 + 1]
        for index, zh in enumerate(list(c_line)):
            jp = j_line[index]
            if not zh == "":
                zh2jp[zh] = jp
                jp2zh[jp] = zh
    
    print("Load", len(zh2jp), "characters from zh_jp_transfer.txt.")
    return zh2jp, jp2zh

if __name__ == "__main__":
    zh2jp, jp2zh = load_transfer()
