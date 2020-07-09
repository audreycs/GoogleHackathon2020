from dataset import KnowledgeGraph
from model import TransE
import numpy as np

import tensorflow as tf
import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def main():
    parser = argparse.ArgumentParser(description='TransE')
    parser.add_argument('--data_dir', type=str, default='../data/')
    parser.add_argument('--embedding_dim', type=int, default=50)
    parser.add_argument('--margin_value', type=float, default=1.0)
    parser.add_argument('--score_func', type=str, default='L1')
    parser.add_argument('--batch_size', type=int, default=512)
    parser.add_argument('--learning_rate', type=float, default=0.01)
    parser.add_argument('--n_generator', type=int, default=4)
    parser.add_argument('--n_rank_calculator', type=int, default=8)
    parser.add_argument('--summary_dir', type=str, default='../summary/')
    parser.add_argument('--max_epoch', type=int, default=300)
    parser.add_argument('--eval_freq', type=int, default=20)
    args = parser.parse_args()
    print(args)
    kg = KnowledgeGraph(data_dir=args.data_dir)
    kge_model = TransE(kg=kg, embedding_dim=args.embedding_dim, margin_value=args.margin_value,
                       score_func=args.score_func, batch_size=args.batch_size, learning_rate=args.learning_rate,
                       n_generator=args.n_generator, n_rank_calculator=args.n_rank_calculator)
    gpu_config = tf.GPUOptions(allow_growth=True)
    sess_config = tf.ConfigProto(gpu_options=gpu_config)
    with tf.Session(config=sess_config) as sess:
        print('-----Initializing tf graph-----')
        tf.global_variables_initializer().run()
        print('-----Initialization accomplished-----')
        # kge_model.check_norm(session=sess)
        summary_writer = tf.summary.FileWriter(logdir=args.summary_dir, graph=sess.graph)
        for epoch in range(args.max_epoch):
            print('=' * 30 + '[EPOCH {}]'.format(epoch+1) + '=' * 30)
            kge_model.launch_training(session=sess, summary_writer=summary_writer)
            # if (epoch + 1) % args.eval_freq == 0:
            #     kge_model.launch_evaluation(session=sess)
        np.save('../res/ent_embeddings', kge_model.entity_embedding.eval(session=sess))
        np.save('../res/rel_embeddings', kge_model.relation_embedding.eval(session=sess))


if __name__ == '__main__':
    main()
