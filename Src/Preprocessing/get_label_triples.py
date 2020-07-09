import pandas as pd

filename = './Data/triples.csv'
raw_data = pd.read_csv(filename, sep=',', header=None, names=['head', 'relation', 'tail'],
                       keep_default_na=False, encoding='utf-8')

# 获取所有label三元组
output_file_label = open('./Data/label.txt', 'w', encoding='utf-8')
for i in raw_data.values:
    if 'label' in i[1]:
        output_file_label.write(i[0]+','+i[1]+','+i[2] + '\n')
output_file_label.close()