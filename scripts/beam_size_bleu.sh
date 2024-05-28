#! /bin/bash

scripts=$(dirname "$0")
base=$scripts/..

data=$base/data
configs=$base/configs

beam_experiments=$base/beam_experiments
translations=$beam_experiments/translations
bleu_scores=$beam_experiments/bleu_scores

mkdir -p $beam_experiments
mkdir -p $translations
mkdir -p $bleu_scores

src=en
trg=de

num_threads=10
device=0

SECONDS=0

model_name=bpe_4k_config

# optional user input: maximum beam size

max_beam=${1:-2}

gsed -i "s/beam_size: 5/beam_size: 0/g" configs/bpe_4k_config.yaml


for (( i=1; i<=${max_beam}; i++ )); do

    # modify beam size
    
    size_before=$(($i-1))
    gsed -i "s/beam_size: $size_before/beam_size: $i/g" configs/bpe_4k_config.yaml


    echo "########################################"
    echo "Beam size $i"

    # BPE level model

    CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python -m joeynmt translate $configs/$model_name.yaml < $data/test.$src > $translations/test.$i.$trg

    # compute case-sensitive BLEU on detokenized data

    cat $translations/test.$i.$trg | sacrebleu $data/test.$trg > $bleu_scores/bleu.$i.json


done

echo "time taken:"
echo "$SECONDS seconds"
