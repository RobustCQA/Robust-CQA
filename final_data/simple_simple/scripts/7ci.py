import matplotlib.pyplot as plt
import pandas as pd
import os 
import json
import textwrap
import random

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../plots/7ci')

color_names = ['black', 'grey', 'silver', 'rosybrown', 'lightcoral', 'brown', 'red', 'coral', 'orangered', 'sienna', 'tan', 'orange', 'goldenrod', 'khaki', 'olive', 'yellow', 'yellowgreen', 'darkolivegreen', 'darkseagreen', 'lightgreen', 'darkgreen', 'green', 'lime', 'aquamarine', 'darkslategrey', 'teal', 'cyan', 'lightblue', 'slategrey', 'royalblue', 'navy', 'blue', 'indigo', 'thistle', 'purple', 'magenta', 'crimson', 'pink']
colors = ['#000000', '#808080', '#C0C0C0', '#BC8F8F', '#F08080', '#A52A2A', '#FF0000', '#FF7F50', '#FF4500', '#A0522D', '#D2B48C', '#FFA500', '#DAA520', '#F0E68C', '#808000', '#FFFF00', '#9ACD32', '#556B2F', '#8FBC8F', '#90EE90', '#006400', '#008000', '#00FF00', '#7FFFD4', '#2F4F4F', '#008080', '#00FFFF', '#ADD8E6', '#708090', '#4169E1', '#000080', '#0000FF', '#4B0082', '#D8BFD8', '#800080', '#FF00FF', '#DC143C', '#FFC0CB']

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
    colors_index = random.sample(range(0, len(colors)), table.shape[1] - 1)
    colors_list = [colors[i] for i in colors_index]
    colors_list_names = [color_names[i] for i in colors_index]

    col_labels = ['Color', 'Entity']
    legend_table = []

    plt.figure(figsize=(20, 10))

    for col in range(1, table.shape[1]):
        plt.plot(table.iloc[:, 0], table.iloc[:, col], label=table.columns[col], color=colors_list[col - 1])
        legend_table.append([colors_list_names[col - 1], table.columns[col]])

    if table.iloc[:, 0].dtype == 'O':
        plt.xticks(table.iloc[:, 0], [textwrap.fill(e, 8) for e in table.iloc[:, 0]], rotation=0)
    else:
        plt.xticks(table.iloc[:, 0], rotation=0)

    for i in range(len(legend_table)):
        legend_table[i][1] = textwrap.fill(legend_table[i][1], 40)

    my_table = plt.table(cellText=legend_table, colLabels=col_labels, loc='upper right', colWidths=[0.1, 0.3])
    my_table.auto_set_font_size(False)
    my_table.set_fontsize(18)

    my_table.scale(1, 2)
    
    plt.ylabel(y_label)
    plt.title(textwrap.fill(title,120))
    plt.tight_layout()
    plt.savefig(os.path.join('../plots/7ci', csv.replace('.csv', '.png')))
    plt.close()