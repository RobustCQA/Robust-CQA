import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import numpy as np

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/7dv')

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
    for bar in range(1, table.shape[1]):
        ax.bar(x + width * (bar - 1), table.iloc[:, bar], width, label=table.columns[bar])

    ax.set_ylabel(y_label)
    ax.set_title(textwrap.fill(title,120))

    if table.iloc[:, 0].dtype == 'O':
        ax.set_xticks(x - width/2 + width * (table.shape[1] - 1) / 2, [textwrap.fill(e, 8) for e in table.iloc[:, 0]])
    else:
        ax.set_xticks(x - width/2 + width * (table.shape[1] - 1) / 2, table.iloc[:, 0])
        
    ax.legend()

    for i in range(table.shape[0]):
        for j in range(1, table.shape[1]):
            ax.text(i + width * (j - 1), table.iloc[i, j], table.iloc[i, j], ha='center', va='bottom')
    plt.yticks([])

    fig.tight_layout()
    plt.savefig(os.path.join('../plots/7dv', csv.replace('.csv', '.png')))
    plt.close()