DATADIR=./text
thumt-trainer \
  --input $DATADIR/ja.bpe $DATADIR/zh.bpe \
  --vocabulary $DATADIR/vocab_50000_ja.txt $DATADIR/vocab_50000_zh.txt \
  --model transformer \
  --validation $DATADIR/ja_test.bpe \
  --references $DATADIR/zh_segment_test.txt \
  --parameters=batch_size=4096,device_list=[0],update_cycle=2 \
  --hparam_set base