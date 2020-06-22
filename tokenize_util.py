from janome.tokenizer import Tokenizer as janome_tokenizer
import jieba
import MeCab
from tqdm import tqdm
from random import sample
try:
    from resource.langconv import Converter
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
except BaseException:
    pass


j_t = janome_tokenizer()
def segment_janome(line):
    seg = [token for token in j_t.tokenize(line, wakati=True)]
    return [word for word in seg if word != ""]

m_t = MeCab.Tagger()
def segment_mecab(line):
    m = m_t.parseToNode(line)
    output_list = []
    while m:
        if not m.surface == "":
            output_list.append(m.surface)
        m = m.next
    return [word for word in output_list if word != ""]

def segment_jieba(line):
    try:
        line = Converter('zh-hans').convert(line).encode('utf-8')
    except BaseException:
        pass
    seg = list(jieba.cut(line))
    return [word for word in seg if word != ""]

def main(zh_method="jieba", ja_method="janome"):
    with open("./text/zh.txt", "r", encoding="utf-8") as f:
        zh_lines = f.readlines()
        seg_zh_lines = [" ".join(segment_jieba(line)) for line in tqdm(zh_lines)]

    with open("./text/ja.txt", "r", encoding="utf-8") as f:
        ja_lines = f.readlines()
        """
        Mecab is at least 30x quicker than janome.
        """
        if ja_method == "janome":
            seg_ja_lines = [" ".join(segment_janome(line)) for line in tqdm(ja_lines)]
        if ja_method == "mecab":
            seg_ja_lines = [" ".join(segment_mecab(line)) for line in tqdm(ja_lines)]

    ja_lines_new = [convert_ja2zh(line) for line in seg_ja_lines]

    total_count = len(seg_zh_lines)
    test_index = sample(range(total_count), 1000)

    with open("./text/zh_segment.txt", "w", encoding="utf-8") as f:
        with open("./text/zh_segment_test.txt", "w", encoding="utf-8") as f_test:
            for index, line in enumerate(seg_zh_lines):
                if not index in test_index:
                    f.write(line.strip() + "\n")
                else:
                    f_test.write(line.strip() + "\n")

    with open("./text/ja_segment.txt", "w", encoding="utf-8") as f:
        with open("./text/ja_segment_test.txt", "w", encoding="utf-8") as f_test:
            for index, line in enumerate(ja_lines_new):
                if not index in test_index:
                    f.write(line.strip() + "\n")
                else:
                    f_test.write(line.strip() + "\n")

if __name__ == "__main__":
    main(zh_method="jieba", ja_method="mecab")

