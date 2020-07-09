import pandas as pd

data = pd.read_csv('./Data/replaced_data_2.txt', sep=',', header=None, names=['head', 'relation', 'tail'],
                   keep_default_na=False, encoding='utf-8')

ent_set = set()
with open("./Data/entity.txt", 'r', encoding='utf-8') as f:
    for i in f.readlines():
        j = i.strip()
        ent_set.add(j)
print(ent_set.__len__())

out_file = open('./Data/final_triples.txt', 'w', encoding='utf-8')
for i in data.values:
    if 'produce' in i[1] or 'effect' in i[1] or 'interaction' in i[1] or 'binding' in i[1] or 'belong_to' in i[1]:
        if '@en' in i[0]:
            h = i[0][:-3]
        else:
            h = i[0]
        if '@en' in i[2]:
            t = i[2][:-3]
        else:
            t = i[2]
        if h in ent_set and t in ent_set:
            out_file.write(h+','+i[1]+','+t+'\n')
        else:
            print(i)
out_file.close()