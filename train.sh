DATADIR=./text
VOCABDIR=./bpe_model
thumt-trainer \
  --input $DATADIR/ja_train.bpe $DATADIR/zh_train.bpe \
  --vocabulary $VOCABDIR/vocab_50000_zh_ja.txt $VOCABDIR/vocab_50000_zh_ja.txt \
  --model transformer \
  --validation $DATADIR/ja_test.bpe \
  --references $DATADIR/zh_segment_test.txt \
  --parameters=batch_size=4096,device_list=[0],update_cycle=2,shared_source_target_embedding=True \
  --hparam_set base
