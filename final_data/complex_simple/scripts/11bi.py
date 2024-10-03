import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import random

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/11bi')

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
    new_table = table.sort_values(by=table.columns[random.randint(1, table.shape[1] - 1)])

    plt.figure(figsize=(20, 10))

    for col in range(1, new_table.shape[1]):
        plt.plot(new_table.iloc[:, 0], new_table.iloc[:, col], label=new_table.columns[col])

    if new_table.iloc[:, 0].dtype == 'O' and len(new_table.iloc[:, 0].unique()) > 6:
        plt.xticks(new_table.iloc[:, 0], [textwrap.fill(e, 8) for e in new_table.iloc[:, 0]], rotation=0)
    else:
        plt.xticks(new_table.iloc[:, 0], rotation=0)

    plt.legend()
    plt.ylabel(y_label)
    plt.title(textwrap.fill(title,120))
    plt.tight_layout()
    plt.savefig(os.path.join('../plots/11bi', csv.replace('.csv', '.png')))
    plt.close()