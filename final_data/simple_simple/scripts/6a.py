import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import numpy as np
import random

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/6a')

colors = ["#FF7F0E", "#1F78B4", "#2CA02C", "#D62728", "#9467BD", "#8C564B", "#7F7F7F", "#BCBD22", "#17BECF", "#FFFF00", "#800080", "#008080", "#FF69B4",  "#000080", "#800000", "#4B00D2", "#FF2F5F", "#5CFF3F", "#003F3F", "#FF002F", "#FFCF20", "#BFBFBF", "#DF7F0E"]

for csv in csvs:
    csv_path = os.path.join('../tables', csv)
    json_name = csv.replace('.csv', '.json')
    json_path = os.path.join('../annotations', json_name)
    table = pd.read_csv(csv_path)

    title = ''
    y_label = ''

    try:    
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                annotations = json.load(f)
                gen_info = annotations['general_figure_info']
                if 'title' in gen_info:
                    title = gen_info['title']['text']
                if 'y_axis' in gen_info:
                    if 'label' in gen_info['y_axis']:
                        y_label = gen_info['y_axis']['label']['text']
    except:
        pass


    print(f'Creating plot for {csv}')
    plt.rcParams.update({'font.size': 18})
    colors_list = random.sample(colors, table.shape[1])

    x = np.arange(table.shape[0])
    width = 0.10

    fig, ax = plt.subplots(figsize=(20, 10))

    count = 1
    for bar in range(1, table.shape[1], 3):
        ax.bar(x + width * (count - 1), table.iloc[:, bar], width, label=table.columns[bar], color=colors_list[bar - 1])
        count += 1
    
    mid = x - width/2 + width * (count - 1) / 2

    for line in range(2, table.shape[1], 3):
        ax.plot(mid, table.iloc[:, line], label=table.columns[line], color=colors_list[line - 1])

    for scatter in range(3, table.shape[1], 3):
        ax.scatter(mid, table.iloc[:, scatter], label=table.columns[scatter], color=colors_list[scatter - 1])

    ax.set_ylabel(y_label)
    ax.set_title(textwrap.fill(title,120))

    if table.iloc[:, 0].dtype == 'O':
        ax.set_xticks(mid, [textwrap.fill(e, 8) for e in table.iloc[:, 0]])
    else:
        ax.set_xticks(mid, table.iloc[:, 0])
      
    ax.legend()

    fig.tight_layout()
    plt.savefig(os.path.join('../plots/6a', csv.replace('.csv', '.png')))
    plt.close()