import os
import sys
from tokenize_util import segment_janome, segment_mecab, convert_ja2zh


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def translate_one_sentence(ja_line, ja_method="mecab"):
    return translate_sentences([ja_line], ja_method)

def translate_sentences(ja_lines, ja_method="mecab", verbose=False):
    if ja_method == "janome":
        seg_ja_lines = [" ".join(segment_janome(line)) for line in ja_lines]
    if ja_method == "mecab":
        seg_ja_lines = [" ".join(segment_mecab(line)) for line in ja_lines]
    ja_lines_new = [convert_ja2zh(line) for line in seg_ja_lines]

    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    with open("./temp/ja_segment_predict.txt", "w", encoding="utf-8") as f:
        for line in ja_lines_new:
            f.write(line.strip() + "\n")

    os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_50000_bpe.model < ./temp/ja_segment_predict.txt > ./temp/ja_predict.bpe")
    
    verbose_tag = ""
    if not verbose:
        verbose_tag = " > ./temp/thumt-translator.log"
    os.system("thumt-translator \
                   --models transformer \
                   --input ./temp/ja_predict.bpe \
                   --output ./temp/zh_predict.txt \
                   --vocabulary ./bpe_model/vocab_50000_ja.txt ./bpe_model/vocab_50000_zh.txt \
                   --checkpoints train/eval \
                   --parameters=device_list=[0],decode_alpha=1.2" + verbose_tag)
    os.system("sed -r 's/(@@ )|(@@ ?$)//g' < ./temp/zh_predict.txt > ./temp/output.txt")
    with open("./temp/output.txt", "r", encoding="utf-8") as f:
        output_lines = f.readlines()
    output = [line.strip() for line in output_lines]
    return output

def main(argv):
    if len(argv) == 1:
        print("Please provide a sentence or a file to translate.")
        print("Example:")
        print("python predict.py あなたは私のマースタか。")
        print("python predict.py あなたは私のマースタか。 異議あり！")
        print("python predict.py ja.txt")
        print("python predict.py ja.txt zh.txt")
        sys.exit()
    input_text = argv[1]
    if os.path.exists(input_text):
        with open(input_text, "r", encoding="utf-8") as f:
            lines = f.readlines()
        zh_lines = translate_sentences(lines)
        if len(argv) > 2:
            output_path = argv[2]
            with open(output_path, "w", encoding="utf-8") as f:
                for line in zh_lines:
                    f.write(line.strip() + "\n")
        else:
            for line in zh_lines:
                print(line.strip() + "\n")
    else:
        ja_lines = []
        for i in range(len(argv) - 1):
            ja_line = argv[i + 1]
            ja_lines.append(ja_line)
        zh_lines = translate_sentences(ja_lines)
        for line in zh_lines:
            print(line.strip() + "\n")

if __name__ == "__main__":
    main(sys.argv)
