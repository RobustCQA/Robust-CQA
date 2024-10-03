import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/5a')

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
    newtable = table.transpose()
    newtable.columns = newtable.iloc[0]
    newtable = newtable.drop(newtable.index[0])

    plt.figure(figsize=(20, 10))

    for col in range(0, newtable.shape[1]):
        plt.plot(newtable.index, newtable.iloc[:, col], label=newtable.columns[col], color = colors[col % len(colors)])

    if newtable.index.dtype == 'O' :
        plt.xticks(newtable.index, [textwrap.fill(e, 8) for e in newtable.index], rotation=0)
    else:
        plt.xticks(newtable.index, rotation=0)

    plt.legend()
    plt.ylabel(y_label)
    plt.title(textwrap.fill(title,120))
    plt.tight_layout()
    plt.savefig(os.path.join('../plots/5a', csv.replace('.csv', '.png')))
    plt.close()