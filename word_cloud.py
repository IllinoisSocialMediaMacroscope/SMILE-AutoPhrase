import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import random
import numpy as np
import os

def word_cloud(words, scores):

    lower, upper = 8, 25
    frequency = [(((x - min(scores)) / (max(scores) - min(scores))) ** 4) * (
                upper - lower) + lower for x in scores]
    colors = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for
              i in range(30)]

    # set location
    x = list(np.arange(0, 10, 0.5))
    y = [i for i in range(30)]
    random.shuffle(x)
    random.shuffle(y)

    data = go.Scatter(
        x=x,
        y=y,
        mode='text',
        text=words,
        hovertext=['{0} {1}'.format(w, s, format(s, '.2%')) for w, s in
                   zip(words, scores)],
        hoverinfo='text',
        textfont={
            'size': frequency,
            'color': colors,
            'family': 'Arial'

        }
    )

    layout = go.Layout(
        {
            'title': 'Top 30 Phrases',
            'font': {'size': 12},
            'xaxis':
                {
                    'showgrid': False,
                    'showticklabels': False,
                    'zeroline': False,
                    'range': [-5, 15]
                },
            'yaxis':
                {
                    'showgrid': False,
                    'showticklabels': False,
                    'zeroline': False,
                    'range': [-5, 35]
                }
        })

    fig = go.Figure(data=[data], layout=layout)

    # save the plot
    div = plot(fig, output_type="div", image='png', auto_open=False,
               image_filename="word_cloud_img")
    fname_div = 'div.html'
    with open(os.path.join('results', fname_div), "w") as f:
        f.write(div)


if __name__ == '__main__':

    phrases = pd.read_csv('./results/AutoPhrase.txt', delimiter='\t', header=None,
                          names=['ranking_score', 'phrases'])

    # instead of directly plotting the words with the existing socre we need to first get all the words that have
    # score bigger than 0.9;
    # then get their frequency and plot based on their frequeny
    phrases = phrases[phrases.ranking_score >= 0.9]['phrases'].to_list()
    phrase_count = [0 for p in phrases]

    with open("data/raw_train.txt", encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for row in lines:
            for i in range(len(phrases)):
                if str(row).lower().find(phrases[i]) > 0:
                    phrase_count[i] += 1

    phrase_count_norm = [float(i) / max(phrase_count) for i in phrase_count]
    word_cloud(phrases, phrase_count_norm)