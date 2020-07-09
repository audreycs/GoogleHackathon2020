import os
import pandas as pd
import numpy as np
import random


class KnowledgeGraph:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.entity_dict = {}
        self.entities = []
        self.relation_dict = {}
        self.n_entity = 0
        self.n_relation = 0
        self.training_triples = []  # list of triples in the form of (h, t, r)
        # self.test_triples = []
        self.n_training_triple = 0
        # self.n_test_triple = 0
        '''load dicts and triples'''
        self.load_dicts()
        self.load_triples()
        '''construct pools after loading'''
        self.training_triple_pool = set(self.training_triples)
        self.golden_triple_pool = set(self.training_triples)

    def load_dicts(self):
        entity_dict_file = 'entity2id.txt'
        relation_dict_file = 'relation2id.txt'
        print('-----Loading entity dict-----')
        entity_df = pd.read_csv(str(self.data_dir+entity_dict_file), sep='\t', header=None, names=['name', 'id'],
                                keep_default_na=False, encoding='utf-8')
        self.entity_dict = dict(zip(entity_df['name'], entity_df['id']))
        self.n_entity = len(self.entity_dict)
        self.entities = list(self.entity_dict.values())
        print('#entity: {}'.format(self.n_entity))
        print('-----Loading relation dict-----')
        relation_df = pd.read_csv(str(self.data_dir+relation_dict_file), sep='\t', header=None, names=['name', 'id'],
                                  keep_default_na=False, encoding='utf-8')
        self.relation_dict = dict(zip(relation_df['name'], relation_df['id']))
        self.n_relation = len(self.relation_dict)
        print('#relation: {}'.format(self.n_relation))

    def load_triples(self):
        training_file = 'all_triples.txt'
        # test_file = 'test.txt'
        print('-----Loading training triples-----')
        training_df = pd.read_csv(str(self.data_dir+training_file), sep='\t', header=None, names=['head', 'relation', 'tail'],
                                  keep_default_na=False, encoding='utf-8')
        self.training_triples = list(zip([self.entity_dict[h] for h in training_df['head']],
                                         [self.entity_dict[t] for t in training_df['tail']],
                                         [self.relation_dict[r] for r in training_df['relation']]))
        self.n_training_triple = len(self.training_triples)
        print('#training triple: {}'.format(self.n_training_triple))
        # print('-----Loading test triples------')
        # test_df = pd.read_csv(str(self.data_dir+test_file), sep='\t', header=None, names=['head', 'relation', 'tail'],
        #                       keep_default_na=False, encoding='utf-8')
        # self.test_triples = list(zip([self.entity_dict[h] for h in test_df['head']],
        #                              [self.entity_dict[t] for t in test_df['tail']],
        #                              [self.relation_dict[r] for r in test_df['relation']]))
        # self.n_test_triple = len(self.test_triples)
        # print('#test triple: {}'.format(self.n_test_triple))

    def next_raw_batch(self, batch_size):
        rand_idx = np.random.permutation(self.n_training_triple)
        start = 0
        while start < self.n_training_triple:
            end = min(start + batch_size, self.n_training_triple)
            yield [self.training_triples[i] for i in rand_idx[start:end]]
            start = end

    def generate_training_batch(self, in_queue, out_queue):
        while True:
            raw_batch = in_queue.get()
            if raw_batch is None:
                return
            else:
                batch_pos = raw_batch
                batch_neg = []
                corrupt_head_prob = np.random.binomial(1, 0.5)
                for head, tail, relation in batch_pos:
                    head_neg = head
                    tail_neg = tail
                    while True:
                        if corrupt_head_prob:
                            head_neg = random.choice(self.entities)
                        else:
                            tail_neg = random.choice(self.entities)
                        if (head_neg, tail_neg, relation) not in self.training_triple_pool:
                            break
                    batch_neg.append((head_neg, tail_neg, relation))
                out_queue.put((batch_pos, batch_neg))
