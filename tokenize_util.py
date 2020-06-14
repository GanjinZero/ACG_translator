from janome.tokenizer import Tokenizer as janome_tokenizer
import jieba
import MeCab
from tqdm import tqdm
from resource.langconv import Converter


j_t = janome_tokenizer()
def segment_janome(line):
    return [token for token in j_t.tokenize(line, wakati=True)]

m_t = MeCab.Tagger()
def segment_mecab(line):
    m = m_t.parseToNode(line)
    output_list = []
    while m:
        if not m.surface == "":
            output_list.append(m.surface)
        m = m.next
    return output_list

def segment_jieba(line):
    line = Converter('zh-hans').convert(line).encode('utf-8')
    return list(jieba.cut(line))

def main(zh_method="jieba", ja_method="janome"):
    with open("./text/zh.txt", "r", encoding="utf-8") as f:
        zh_lines = f.readlines()
        seg_zh_lines = [" ".join(segment_jieba(line)) for line in tqdm(zh_lines)]
    with open("./text/zh_segment.txt", "w", encoding="utf-8") as f:
        for line in seg_zh_lines:
            f.write(line.strip() + "\n")

    with open("./text/ja.txt", "r", encoding="utf-8") as f:
        ja_lines = f.readlines()
        if ja_method == "janome":
            seg_ja_lines = [" ".join(segment_janome(line)) for line in tqdm(ja_lines)]
        if ja_method == "janome":
            seg_ja_lines = [" ".join(segment_mecab(line)) for line in tqdm(ja_lines)]
    with open("./text/ja_segment.txt", "w", encoding="utf-8") as f:
        for line in seg_ja_lines:
            f.write(line.strip() + "\n")

if __name__ == "__main__":
    main(zh_method="jieba", ja_method="janome")
