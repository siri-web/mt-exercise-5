#!usr/bin/env python3

# Script that creates plots to visualize the results from experimenting with different beam sizes for translation
# Path to directory with BLEU scores from experiment is hard-coded

import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
import json
import re


def main():

    path_experiments = Path('.') / Path('beam_experiments')
    path_bleu_scores = path_experiments / Path('bleu_scores')
    files = path_bleu_scores.glob('*')

    results = dict()

    for file in files:
    
        beam_size = re.search(r'bleu\.(\d+)', str(file)).group(1)

        with file.open('r', encoding='utf-8') as f:

            data = json.load(f)
            bleu = data["score"]
            verbose_score = data["verbose_score"]
            BP = re.search(r'BP = (\d+\.\d+)', verbose_score).group(1)
            ratio = re.search(r'ratio = (\d+\.\d+)', verbose_score).group(1)
            scores = [bleu, float(BP), float(ratio)]

            results[int(beam_size)] = scores

    df = pd.DataFrame.from_dict(results, orient='index', columns=["bleu", "bp", "ratio"])
    df = df.sort_index(axis=0)
    df = df.reset_index().rename(columns={"index": "beam"})
    df["time_to_generate"] = [76.3954, 66.1736] #114.9019, 155.5503, 203.7575, 245.9491, 276.8280, 320.1244, 381.0156, 428.8029]
    print(df)

    path_figures = path_experiments / Path('figures')
    path_figures.mkdir(exist_ok=True)

    # plot BLEU (y) over beam size (x)

    fig_beam_bleu, ax_beam_bleu = plt.subplots()
    ax_beam_bleu.scatter(df.beam, df.bleu)
    ax_beam_bleu.set_axisbelow(True)  # grid lines behind data points
    ax_beam_bleu.grid(linewidth=0.5)
    ax_beam_bleu.set_xlabel('Beam size')
    ax_beam_bleu.set_ylabel('BLEU')
    ax_beam_bleu.set_title('BLEU with different beam sizes')
    fig_beam_bleu.savefig(path_figures / Path('beam_vs_bleu.png'))

    # plot time (y) over beam size (x)

    fig_time_bleu, ax_time_bleu = plt.subplots()
    ax_time_bleu.scatter(df.beam, df.time_to_generate)
    ax_time_bleu.set_axisbelow(True)
    ax_time_bleu.grid(linewidth=0.5)
    ax_time_bleu.set_xlabel('Beam size')
    ax_time_bleu.set_ylabel('Time in seconds')
    ax_time_bleu.set_title('Time to generate with different beam sizes')
    fig_time_bleu.savefig(path_figures / Path('beam_vs_time.png'))

if __name__ == "__main__":
    main()

