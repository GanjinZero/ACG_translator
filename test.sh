DATADIR=./text
VOCABDIR=./bpe_model
thumt-translator \
  --models transformer \
  --input $DATADIR/ja_test.bpe \
  --output $DATADIR/zh_test_predict.txt \
  --vocabulary $VOCABDIR/vocab_50000_ja.txt $VOCABDIR/vocab_50000_zh.txt \
  --checkpoints train/eval \
  --parameters=device_list=[0],decode_alpha=1.2
