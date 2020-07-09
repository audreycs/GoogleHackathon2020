import pandas as pd

raw_data = pd.read_csv('./Data/triples.csv', sep=',', header=None, names=['head', 'relation', 'tail'],
                       keep_default_na=False, encoding='utf-8')

label_file = pd.read_csv('./Data/label.txt', sep=',', header=None, names=['head', 'relation', 'tail'],
                       keep_default_na=False, encoding='utf-8')

label_dic = dict()
for i in label_file.values:
    # print(i[0])
    # print(i[2])
    label_dic[i[0]] = i[2]

out_file = open('./Data/replaced_data.txt', 'w', encoding='utf-8')
for i in raw_data.values:
    if 'label' not in i[1]:
        if label_dic.get(i[0]) is not None:
            out_file.write(label_dic[i[0]])
        else:
            out_file.write(i[0])
        out_file.write(','+i[1]+',')
        if label_dic.get(i[2]) is not None:
            out_file.write(label_dic[i[2]])
        else:
            out_file.write(i[2])
        out_file.write('\n')
out_file.close()