import json
import csv
if __name__ == '__main__':
    with open('data/virusnetwokr.drug2.27.json','r',encoding='utf-8') as f:
        triples=[]
        data = json.load(f)
        key2ids = data["@context"]
        for item in data["@graph"]:
            id = item['@id']
            # print(item)
            for key,value in item.items():
                # print (key2ids[key])
                if key=='@id':
                    continue
                key_id = key2ids[key]["@id"]
                if isinstance(value,str):
                    triples.append((id,key_id,value))
                elif isinstance(value,dict):
                    # if key=='label' or key=='alias':
                    if "@language" in value:
                        value=value['@value']+"@"+value["@language"]
                    else:
                        value = value['@value']
                    triples.append((id, key_id, value))
                    # else:
                    #     print('error',key,value)
                elif isinstance(value,list):
                    for v in value:
                        if isinstance(v,str):
                            triples.append((id, key_id, v))
                        elif isinstance(v, dict):
                            # if key == 'label' or key == 'alias':
                            if "@language" in value:
                                v = v['@value'] + "@" + v["@language"]
                            else:
                                v = v['@value']
                            triples.append((id, key_id, v))
                            # else:
                            #     print('error', key, v)
                        else:
                            print('error', key, v)
    with open('data/triples.csv','w',encoding='utf-8',newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(triples)
        # for triple in triples:
        #     for t in triple:
        #         if not isinstance(t,str):
        #             print(triple)
        #     f.write(','.join(triple)+'\n')