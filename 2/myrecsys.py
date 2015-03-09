"""myrecsys.py: a recommender system suite

Implements a set of different collaborative filtering algorithms and evaluates
them.

#Usage

On unixs.cssd.pitt.edu, run
    /usr/local/python3.4.2/bin/python3 myrecsys.py <training_data> <test_data> <algorithm>

Accepts the following algorithms as arguments:
    average
    user-euclidean
    user-pearson
    item-cosine
"""

__author__ = 'elm139'

import sys
import logging
logging.basicConfig(level=logging.INFO)
import argparse
from operator import attrgetter, itemgetter
import itertools
from pprint import pprint, pformat
import time

class Rating:
    def __init__(self, user, item, stars, timestamp=None):
        self.user = user
        self.item = item
        self.stars = int(stars)
        self.timestamp = float(timestamp) if timestamp else None

    def __repr__(self):
        return ('Rating(user={!r}, item={!r}, stars={!r}, timestamp={!r})'
                .format(self.user, self.item, self.stars, self.timestamp))
    
def _average(r_table, vector, neighbor):
    """Algorithm: estimates similarity of the neighbor to the vector.
    
    Returns 1 (all neighbors have equal weight).
    """
    return 1

def _euclidean(r_table, vector, neighbor):
    """Algorithm: estimates similarity of the neighbor to the vector.
    
    Uses the Euclidean n-dimensional distance algorithm.
    Args:
        vector: A key to the first level of the nested dict.
        neighbor: A key of the same type as vector.
        r_table (dict): A nested dict: user -> item -> stars.
    """
    d_2 = 0
    for dim in r_table[vector]:
        if dim in r_table[neighbor]:
            d_2 += (r_table[vector][dim] - r_table[neighbor][dim])**2
    return 1/(1 + d_2**.5)

def _pearson(r_table, vector, neighbor):
    """Algorithm: estimates similarity of the neighbor to the vector.
    
    Returns the Pearson correlation coefficient.
    Args:
        vector: A key to the first level of the nested dict.
        neighbor: A key of the same type as vector.
        r_table (dict): A nested dict: user -> item -> stars.
    """
    xs = ys = x_2 = y_2 = xy = n = 0
    for dim in r_table[vector]:
        if dim in r_table[neighbor]:
            x = norm(r_table[vector][dim], 1, 5)
            y = norm(r_table[neighbor][dim], 1, 5)
            xs += x     
            ys += y     
            xy += x * y 
            n += 1      
            x_2 += x**2 
            y_2 += y**2 
    denom = ((n * x_2 - (xs**2))*(n * y_2 - (ys**2)))**.5
    r = 0 if denom == 0 else (n * xy - (xs * ys))/denom
    logging.debug(r)
    return r

def _cosine(r_table, vector, neighbor):
    """Algorithm: estimates similarity of the neighbor to the user.
    
    Returns the cosine correlation coefficient.
    Args:
        vector: A key to the first level of the nested dict.
        neighbor: A key of the same type as vector.
        r_table (dict): A nested dict: user -> item -> stars.
    """
    x = y = x_2 = y_2 = x_times_y = 0
    logging.debug("{}, {}".format(vector, neighbor))
    for dim in r_table[vector]:
        if dim in r_table[neighbor]:
            x = r_table[vector][dim]
            y = r_table[neighbor][dim]
            x_2 += x**2
            y_2 += y**2
            x_times_y += x * y
    denom = (x_2 * y_2)**.5
    ret = 0 if denom == 0 else x_times_y / denom
    logging.debug(ret)
    return ret

def _neighborhood(sim, r_table, vector):
    """Gets the most similar non-identity vectors in r_table as a list.
    
    :arg sim: is a :class SimilarityAlgorithm:.
    """
    k = 100
    all_neighbors = [n for n in r_table if n != vector]
    if not sim.neighborhood:
        return all_neighbors
    return [n for n in sorted(all_neighbors, 
                    key=lambda n: abs(sim(r_table, vector, n)), 
                    reverse=True)][:k]

def norm(s, min_r, max_r):
    return (2 * (s - min_r) - (max_r - min_r))/float(max_r - min_r)

def denorm(s, min_r, max_r):
    return .5 * ((s + 1) * (max_r - min_r)) + min_r

def _estimation(similarity, r_table, vector, dim):
    neighborhood = _neighborhood(similarity, r_table, vector)
    est = total_weight = 0
    avg = lambda n: sum(r_table[n].values())/len(r_table[n])
    min_r = 1
    max_r = 5
    logging.debug('vector: {}'.format(vector))
    for neighbor in neighborhood:
        logging.debug('r_table of: {}, {}'.format(neighbor, dim))
        if dim in r_table[neighbor]:
            weight = similarity(r_table, vector, neighbor)
            if similarity.normalized:
                est += weight * norm(r_table[neighbor][dim], min_r, max_r)
                logging.debug('weight: {}'.format(weight))
                logging.debug('value: {}'.format(r_table[neighbor][dim]))
                total_weight += abs(weight)
            else:
                est += weight * r_table[neighbor][dim]
                total_weight += weight
    ret = 0 if total_weight == 0 else est/total_weight
    if similarity.normalized:
        logging.debug('ret from _estimation: {}'.format(ret))
        ret = denorm(ret, min_r, max_r)
    return ret

def _RMSE(algorithm, r_table, test):
    """Gives the root mean squared error for an algorithm.

    Args:
        algorithm (function): The algorithm in question
        r_table (dict): A nested dict.
        test (list): Rating list of the test data.
    """
    vector = attrgetter(algorithm.vector)
    dim = attrgetter(algorithm.dim)
    return (sum([(r.stars-_estimation(algorithm, r_table, vector(r), dim(r)))**2
                  for r in test])/len(test))**.5

class SimilarityAlgorithm:
    def __init__(self, name):
        self.neighborhood = False if name == 'average' else True
        self.dim = 'user' if self.vector == 'item' else 'item'
    
    # Memoized.
    def __call__(self, r_table, vector, neighbor, _d={}):
        if frozenset((vector, neighbor)) in _d:
            #logging.debug('remembered: {}'.format(_d[frozenset((vector, neighbor))]))
            return _d[frozenset((vector, neighbor))]
        if vector not in r_table or neighbor not in r_table:
            result = 0
        else:
            result = self.__class__.algorithm(r_table, vector, neighbor) 
        #logging.debug('found: {}'.format(result))
        _d[frozenset((vector, neighbor))] = result
        return result

class Average(SimilarityAlgorithm):
    algorithm = _average
    vector = 'user'
    normalized = False

class UserEuclidean(SimilarityAlgorithm):
    algorithm = _euclidean
    vector = 'user'
    normalized = False

class UserPearson(SimilarityAlgorithm):
    algorithm = _pearson
    vector = 'user'
    normalized = True

class ItemCosine(SimilarityAlgorithm):
    algorithm = _cosine
    vector = 'item'
    normalized = True

def main():
    algorithm_dict = {
            'average': Average,
            'user-pearson': UserPearson,
            'user-euclidean': UserEuclidean,
            'item-cosine': ItemCosine
            }
    parser = argparse.ArgumentParser(
            description='A recommender system algorithm test suite.')
    parser.add_argument('training_data', help='the training data')
    parser.add_argument('test_data', help='the test data')
    parser.add_argument('alg_name', help='the algorithm to use', 
                        metavar='algorithm',
                        choices=algorithm_dict.keys())
    args = parser.parse_args()
    get_ratings = lambda f: [Rating(*l.split()) 
                                 for l in open(f, 'r').read().splitlines()]
    training = get_ratings(args.training_data)
    sim_alg = algorithm_dict[args.alg_name](args.alg_name)
    v = attrgetter(sim_alg.vector)
    d = attrgetter(sim_alg.dim)
    r_table = {k : {d(r):r.stars for r in l}
                for k, l in itertools.groupby(sorted(training, key=v), v)}
    test = get_ratings(args.test_data)
    print("MYRESULTS Training = {}".format(args.training_data))
    print("MYRESULTS Testing = {}".format(args.test_data))
    print("MYRESULTS Algorithm = {}".format(args.alg_name))
    t0 = time.time()
    print("MYRESULTS RMSE = {:.10}".format(_RMSE(sim_alg, r_table, test)))
    #logging.info(time.time() - t0)

if __name__ == "__main__":
    if sys.version_info.major < 3:
        raise Exception("Python version not supported.\n"
                "Please run this program with Python 3.\n"
                "On unixs.cssd.pitt.edu, you can use "
                "/usr/local/python3.4.2/bin/python3\n")
    main()
