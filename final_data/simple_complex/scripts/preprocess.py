import pandas as pd
import os 
import csv 
import numpy as np

csvs = [f for f in os.listdir('../tables') if f.endswith('.csv')]
os.system('mkdir -p ../tables')

for csv in csvs:
    csv_path = os.path.join('../tables', csv)
    table = pd.read_csv(csv_path)

    characters_to_replace = ['%', ',', '$']

    for i in range(1, len(table.columns)):
        if table.iloc[:, i].dtype == 'O':
            print('Processing table:', csv, 'column:', table.columns[i])
            for char in characters_to_replace:
                table.iloc[:, i] = table.iloc[:, i].str.replace(char, '')
            # check if the column values have a -
            if table.iloc[:, i].str.contains('-').any():
                for j in range(len(table.iloc[:, i])):
                    if '-' in table.iloc[j, i][-1]:
                        table.iloc[j, i] = np.nan
            table.iloc[:, i] = table.iloc[:, i].astype(float)
    
    for i in range(1, len(table.columns)):
        table[table.columns[i]] = table[table.columns[i]].fillna(0)
    
    table.to_csv(os.path.join('../tables', csv), index=False)
