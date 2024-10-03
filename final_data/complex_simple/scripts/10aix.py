import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import math

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/10aix')

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
    num_plots = table.shape[1] - 1
    nearest_sq = math.ceil(math.sqrt(num_plots))
    fig, ax = plt.subplots(nearest_sq, nearest_sq, figsize=(10 * nearest_sq, 5 * nearest_sq))

    for col in range(1, table.shape[1]):
        ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].scatter(table.iloc[:, 0], table.iloc[:, col], label=table.columns[col])
        ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].set_title(textwrap.fill(table.columns[col],60))
        ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].set_ylabel(y_label)
        if table.iloc[:, 0].dtype == 'O':
            ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].set_xticklabels([textwrap.fill(e, 8) for e in table.iloc[:, 0]], rotation=0)
        else:
            ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].set_xticklabels(table.iloc[:, 0], rotation=0)
        ax[(col - 1) // nearest_sq, (col - 1) % nearest_sq].legend()

    fig.suptitle(textwrap.fill(title,120))
    plt.savefig(os.path.join('../plots/10aix', csv.replace('.csv', '.png')))
    plt.close()