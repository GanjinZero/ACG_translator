import os
import json
from collections import OrderedDict


def learn_bpe(num_operations, vocabulary_threshold, bpe_model_overwrite=False):
    print("Learn BPE")
    if not os.path.exists("./bpe_model/"):
        os.makedirs("bpe_model")
    if os.path.exists(f"./bpe_model/zh_ja_{num_operations}_bpe.model") and not bpe_model_overwrite:
        print(f"Found ./bpe_model/zh_ja_{num_operations}_bpe.model")
    else:
        os.system(f"subword-nmt learn-bpe -v -s {num_operations} < ./text/bpe_train.txt > ./bpe_model/zh_ja_{num_operations}_bpe.model")
    
    print("Apply BPE")
    if vocabulary_threshold is None:
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model < ./text/zh_segment.txt > ./text/zh_train.bpe")
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model < ./text/ja_segment.txt > ./text/ja_train.bpe")
        #os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model < ./text/zh_segment_test.txt > ./text/zh_test.bpe")
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model < ./text/ja_segment_test.txt > ./text/ja_test.bpe")
    else:
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model --vocabulary-threshold {vocabulary_threshold} < ./text/zh_segment.txt > ./text/zh_train.bpe")
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model --vocabulary-threshold {vocabulary_threshold} < ./text/ja_segment.txt > ./text/ja_train.bpe")
        #os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model --vocabulary-threshold {vocabulary_threshold} < ./text/zh_segment_test.txt > ./text/zh_test.bpe")
        os.system(f"subword-nmt apply-bpe -c ./bpe_model/zh_ja_{num_operations}_bpe.model --vocabulary-threshold {vocabulary_threshold} < ./text/ja_segment_test.txt > ./text/ja_test.bpe")

    print("Build dictionary")
    #os.system(f"python build_dictionary.py ./text/zh_train.bpe ./text/ja_train.bpe")
    os.system(f"python build_vocab.py ./text/zh_train.bpe ./bpe_model/vocab_{num_operations}_zh")
    os.system(f"python build_vocab.py ./text/ja_train.bpe ./bpe_model/vocab_{num_operations}_ja")

    """
    print("Build zh_ja dictionary")
    zh_bpe_json = json.load(open('./text/zh_train.bpe.json', 'r', encoding="utf-8"))
    ja_bpe_json = json.load(open('./text/ja_train.bpe.json', 'r', encoding="utf-8"))
    zh_dict = [word for word, index in zh_bpe_json.items()]
    ja_dict = [word for word, index in ja_bpe_json.items()]
    zh_ja_dict = set(zh_dict + ja_dict)

    zh_ja_dict = zh_ja_dict - set(['<EOS>', '<GO>', '<UNK>'])

    worddict = OrderedDict()
    worddict['<EOS>'] = 0
    worddict['<GO>'] = 1
    worddict['<UNK>'] = 2
    # FIXME We shouldn't assume <EOS>, <GO>, and <UNK> aren't BPE subwords.
    for ii, ww in enumerate(zh_ja_dict):
        worddict[ww] = ii + 3

    # Save word2id, id2word as json
    word2id = {word: index for index, word in enumerate(worddict)}
    id2word = {index: word for index, word in enumerate(worddict)}    
    with open('./text/word2id.json', 'w', encoding='utf-8') as f:
        json.dump(word2id, f, indent=2, ensure_ascii=False)
    with open('./text/id2word.json', 'w', encoding='utf-8') as f:
        json.dump(id2word, f, indent=2, ensure_ascii=False)
    """

    return

def main(num_operations=50000, vocabulary_threshold=None):
    with open("./text/zh_segment.txt", "r", encoding="utf-8") as f:
        zh_lines = f.readlines()
    with open("./text/ja_segment.txt", "r", encoding="utf-8") as f:
        ja_lines = f.readlines()
    with open("./text/bpe_train.txt", "w", encoding="utf-8") as f:
        for line in zh_lines:
            f.write(line.strip() + "\n")
        for line in ja_lines:
            f.write(line.strip() + "\n")
    
    learn_bpe(num_operations, vocabulary_threshold, bpe_model_overwrite=True)
    
if __name__ == "__main__":
    main()
