import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import numpy as np
import random

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/2bii1')

color_values = ['#000000', '#808080', '#C0C0C0', '#BC8F8F', '#F08080', '#A52A2A', '#FF0000', '#FF7F50', '#FF4500', '#A0522D', '#D2B48C', '#FFA500', '#DAA520', '#F0E68C', '#808000', '#FFFF00', '#9ACD32', '#556B2F', '#8FBC8F', '#90EE90', '#006400', '#008000', '#00FF00', '#7FFFD4', '#2F4F4F', '#008080', '#00FFFF', '#ADD8E6', '#708090', '#4169E1', '#000080', '#0000FF', '#4B0082', '#D8BFD8', '#800080', '#FF00FF', '#DC143C', '#FFC0CB']

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

    x = np.arange(table.shape[0])
    width = 0.10

    fig, ax = plt.subplots(figsize=(20, 10))
    color_starting = random.randint(0, len(color_values) - table.shape[1])
    for bar in range(1, table.shape[1]):
        ax.bar(x + width * (bar - 1), table.iloc[:, bar], width, label=table.columns[bar], color=color_values[color_starting + bar - 1])
    
    ax.set_ylabel(y_label)
    ax.set_title(textwrap.fill(title, 120))
    
    plt.rcParams.update({'font.size': 18})

    if table.iloc[:, 0].dtype == 'O' :
        ax.set_xticks(x - width/2 + width * (table.shape[1] - 1) / 2, [textwrap.fill(e, 8) for e in table.iloc[:, 0]])
    else:
        ax.set_xticks(x - width/2 + width * (table.shape[1] - 1) / 2, table.iloc[:, 0])
        
    ax.legend()
    ax.legend(facecolor=color_values[color_starting + table.shape[1] - 1])

    fig.tight_layout()
    plt.savefig(os.path.join('../plots/2bii1', csv.replace('.csv', '.png')))
    plt.close()