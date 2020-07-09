import pandas as pd

data = pd.read_csv('./Data/type.txt', sep=',', header=None, names=['head', 'relation', 'tail'],
                   keep_default_na=False, encoding='utf-8')

out_file = open('./Data/entity.txt', 'w', encoding='utf-8')
ent_set = set()
for i in data.values:
    if '@en' in i[0]:
        ent_set.add(i[0][:-3])
    else:
        ent_set.add(i[0])

for i in ent_set:
    out_file.write(i+'\n')
out_file.close()