import math
import sys
import time
import metapy
import pytoml
import numpy as np
from operator import itemgetter


def load_ranker(cfg_file,mu):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    
    # return metapy.index.JelinekMercer(0.5) 
    return metapy.index.DirichletPrior(mu) 


def score2(ranker, index, query, top_k, alpha):
    print("Scoring")
    # print("start")
    results = ranker.score(index, query, 1000)
    print(results)
    new_results = []
    new_scores = []
    updated_results = {}
    alpha = alpha        # all, 2500, 0.13, 0.666
    for res in results:
        doc_name = index.metadata(res[0]).get('doc_name')
        updated_results[doc_name] = (1-alpha) * res[1] + alpha * float(index.metadata(res[0]).get('prior'))
        new_scores.append(updated_results[doc_name])
    new_idx = np.argsort(np.array(new_scores))[::-1][:top_k]
       
    for idx in new_idx:
        new_results.append((results[idx][0], new_scores[idx]))
    return new_results, updated_results


def score1(ranker, index, query, top_k):
    results = ranker.score(index, query, top_k)
    new_results = []
    new_scores = []
    updated_results = {}
    
    for res in results:
        doc_name = index.metadata(res[0]).get('doc_name')
        updated_results[doc_name] = res[1]+float(index.metadata(res[0]).get('prior'))
        new_scores.append(updated_results[doc_name])
    new_idx = np.argsort(np.array(new_scores))[::-1][:10]
       
    for idx in new_idx:
        new_results.append((results[idx][0],new_scores[idx]))
    return new_results


if __name__ == '__main__':
    cfg = './para_idx_data/config.toml'
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
    print(cfg_d)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    with open("./para_idx_data/0.txt") as query_file:
        ranker = load_ranker(cfg, 2500)
        for line in query_file:
            query = metapy.index.Document()
            query.content(line.strip())
            res_num = 1

    new, update = score2(ranker, idx, query, 10, 0.34)
    # print(new)
    # print(sorted(update.items(), key=itemgetter(1)))

