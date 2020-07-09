import pandas as pd
import csv

data = pd.read_csv('./Data/replaced_data.txt', sep=',', header=None, names=['head', 'relation', 'tail'],
                   keep_default_na=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

out_file = open('./Data/type.txt', 'w', encoding='utf-8')
for i in data.values:
    if 'type' in i[1]:
        out_file.write(i[0]+','+i[1]+','+i[2]+'\n')
out_file.close()