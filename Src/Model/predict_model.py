import math
import timeit
import numpy as np
import tensorflow as tf
from dataset import KnowledgeGraph


class TransE:
    def __init__(self, kg: KnowledgeGraph, score_func):
        self.kg = kg
        self.entity_num = self.kg.n_entity
        self.relation_num = self.kg.n_relation
        self.score_func = score_func
        '''embeddings'''
        self.entity_embedding = tf.constant(np.load('../res/ent_embeddings.npy'))
        self.relation_embedding = tf.constant(np.load('../res/rel_embeddings.npy'))

    def predict_head(self, t_id, r_id):
        tail = tf.nn.embedding_lookup(self.entity_embedding, t_id)
        relation = tf.nn.embedding_lookup(self.relation_embedding, r_id)
        distance_head_prediction = self.entity_embedding + relation - tail
        values_head_prediction, idx_head_prediction = tf.nn.top_k(-tf.reduce_sum(tf.abs(distance_head_prediction), axis=1),
                                                                  k=20)
        return idx_head_prediction

    def predict_tail(self, h_id, r_id):
        head = tf.nn.embedding_lookup(self.entity_embedding, h_id)
        relation = tf.nn.embedding_lookup(self.relation_embedding, r_id)
        distance_tail_prediction = self.entity_embedding - relation - head
        values_tail_prediction, idx_tail_prediction = tf.nn.top_k(-tf.reduce_sum(tf.abs(distance_tail_prediction), axis=1),
                                                                  k=10)
        return idx_tail_prediction
