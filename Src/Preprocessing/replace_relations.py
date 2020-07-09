import pandas as pd
import csv

data = pd.read_csv('./Data/replaced_data.txt', sep=',', header=None, names=['head', 'relation', 'tail'],
                       keep_default_na=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

out_file = open('./Data/replaced_data_2.txt', 'w', encoding='utf-8')
for i in data.values:
    if 'http://www.openkg.cn/COVID-19/research/property/P18' in i[1]:
        out_file.write(i[0]+","+"produce"+","+i[2])
    elif 'http://www.openkg.cn/COVID-19/research/property/P19' in i[1]:
        out_file.write(i[0] + "," + "effect" + "," + i[2])
    elif 'http://www.openkg.cn/COVID-19/research/property/P20' in i[1]:
        out_file.write(i[0] + "," + "interaction" + "," + i[2])
    elif 'http://www.openkg.cn/COVID-19/research/property/P21' in i[1]:
        out_file.write(i[0] + "," + "binding" + "," + i[2])
    elif 'http://www.openkg.cn/COVID-19/research/property/P22' in i[1]:
        out_file.write(i[0] + "," + "belong_to" + "," + i[2])
    else:
        out_file.write(i[0] + "," + i[1] + "," + i[2])
    out_file.write('\n')
out_file.close()