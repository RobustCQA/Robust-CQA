import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import random

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/4eiv')

markers = [".", "o", "v", "^", "<", ">", "1", "2", "s", "p", "P", "*", "h", "+", "x", "X", "D", "|"]
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
    marker = random.choice(markers)
    color_list = random.sample(colors, table.shape[1] - 1)

    plt.figure(figsize=(20, 10))

    for col in range(1, table.shape[1]):
        plt.step(table.iloc[:, 0], table.iloc[:, col], label=table.columns[col], color=color_list[col - 1], marker=marker)

    if table.iloc[:, 0].dtype == 'O':
        plt.xticks(table.iloc[:, 0], [textwrap.fill(e, 8) for e in table.iloc[:, 0]], rotation=0)
    else:
        plt.xticks(table.iloc[:, 0], rotation=0)

    plt.legend()
    plt.ylabel(y_label)
    plt.title(textwrap.fill(title,120))
    plt.tight_layout()
    plt.savefig(os.path.join('../plots/4eiv', csv.replace('.csv', '.png')))
    plt.close()