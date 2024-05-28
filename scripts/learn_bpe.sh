#! /bin/bash

scripts=$(dirname "$0")
base=$scripts/..
data=$base/data

models=$base/models
configs=$base/configs

cat $data/train.en $data/train.de > $data/train_cat.txt

subword-nmt learn-joint-bpe-and-vocab --input $data/train_cat.txt -t -s 4000 -o $data/codes4000.bpe \
--write-vocabulary $data/joint_vocab_counts_4k.txt

cut -f1 -d' ' $data/joint_vocab_counts_4k.txt > $data/joint_vocab_4k.txt


mkdir -p $models

for MODEL in words
do
    ./scripts/train.sh $MODEL
done