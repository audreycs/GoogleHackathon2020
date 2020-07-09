import numpy as np
from dataset import KnowledgeGraph
from predict_model import TransE
import tensorflow as tf
from xmlrpc.server import SimpleXMLRPCServer


kg = KnowledgeGraph(data_dir='../../Data/TrainingData/')
ent_dic = kg.entity_dict
rel_dic = kg.relation_dict
model = TransE(kg=kg, score_func='L1')
type_dic = dict()
with open('../../Data/TrainingData/type.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        s = i.strip().split('\t')
        type_dic[s[0]] = s[1]


def predict_drug(t):
    r_id = int(rel_dic.get('effect'))
    t_id = int(ent_dic.get(t))
    top_k_id = model.predict_head(r_id, t_id)
    top_k = list()
    new_ent_dic = dict(zip(ent_dic.values(), ent_dic.keys()))
    sess = tf.Session()
    with sess.as_default():
        for i in top_k_id.eval():
            top_k.append(new_ent_dic.get(i))
    print()
    result = list()
    count = 0
    for name in top_k:
        if count < 5:
            if type_dic.get(name) == 'Drug':
                result.append(name)
                count += 1
        else:
            break
    return result


def predict_interaction_protein(h):
    r_id = int(rel_dic.get('interaction'))
    h_id = int(ent_dic.get(h))
    top_10_id = model.predict_tail(h_id, r_id)
    top_10 = list()
    new_ent_dic = dict(zip(ent_dic.values(), ent_dic.keys()))
    sess = tf.Session()
    with sess.as_default():
        for i in top_10_id.eval():
            top_10.append(new_ent_dic.get(i))
    result = list()
    for name in top_10:
        if type_dic.get(name) == 'VirusProtein':
            result.append(name)
    return result


def predict_binding_protein(h):
    r_id = int(rel_dic.get('binding'))
    h_id = int(ent_dic.get(h))
    top_10_id = model.predict_tail(h_id, r_id)
    top_10 = list()
    new_ent_dic = dict(zip(ent_dic.values(), ent_dic.keys()))
    sess = tf.Session()
    with sess.as_default():
        for i in top_10_id.eval():
            top_10.append(new_ent_dic.get(i))
    result = list()
    for name in top_10:
        if type_dic.get(name) == 'HostProtein':
            result.append(name)
    return result


if __name__ == '__main__':

    # server = SimpleXMLRPCServer(('114.212.85.127', 8888))
    # server.register_function(predict_drug, "predictDrug")
    # server.register_function(predict_binding_protein, "predictBindingProtein")
    # server.register_function(predict_interaction_protein, "predictInteractionProtein")
    # print("Listening...")
    # server.serve_forever()

    result = predict_drug('Human_adenovirus_28')
    print(result)
    result = predict_interaction_protein('TOR1A')
    print(result)
    result = predict_binding_protein('PB2')
    print(result)

