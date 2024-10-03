import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/7dii')

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
    plt.figure(figsize=(20, 10))

    for col in range(1, table.shape[1]):
        plt.plot(table.iloc[:, 0], table.iloc[:, col], label=table.columns[col])
    
    if table.iloc[:, 0].dtype == 'O':
        plt.xticks(table.iloc[:, 0], [textwrap.fill(e, 8) for e in table.iloc[:, 0]], rotation=0)
    else:
        plt.xticks(table.iloc[:, 0], rotation=0)

    plt.legend()
    plt.ylabel(y_label)
    plt.title(textwrap.fill(title,120))

    # for i in range(table.shape[0]):
    #     for j in range(1, table.shape[1]):
    #         plt.text(i, table.iloc[i, j], table.iloc[i, j])
    for i in range(table.shape[0]):
        for j in range(1, table.shape[1]):
            plt.annotate(f'{table.iloc[i, j]:.2f}', (table.iloc[i, 0], table.iloc[i, j]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.yticks([])
    
    plt.tight_layout()
    plt.savefig(os.path.join('../plots/7dii', csv.replace('.csv', '.png')))
    plt.close()