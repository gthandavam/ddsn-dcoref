__author__ = 'gt'

import numpy as np
import itertools
from edu.sbu.eval.so.features.ft_extraction import get_sem_grouping
from edu.sbu.eval.so.data.prepare_data import sentSeparator


def get_score(weights, pairs, perm):
  '''
    score(x) = sum( i 1 to n, j i+1 to n   P(i,j))
  '''
  score = 0.0
  for i in xrange(len(perm)):
    for j in xrange(i+1, len(perm)):
      pair = str(i) + ',' + str(j)
      r_pair = str(j) + ',' + str(i)
      if pair in pairs:
        k = pairs.index(pair)
        score += weights[k][0]
      elif r_pair in pairs:
        k = pairs.index(r_pair)
        score += weights[k][1]

  return score
  pass

def get_best_order(weights, predicted_labels, pairs, number_of_nodes):
  '''
  API to get best order based on

  order = argmax( score(x) ) for all x belongs to permutations of no of nodes

  '''

  max_score = -1
  max_order = []

  for perm in itertools.permutations(xrange(number_of_nodes)):
    score = get_score(weights, pairs, perm)
    '''
    In case of a tie in max_score, picking the one lowest in lexicographical order
    '''
    if score > max_score:
      max_score = score
      max_order = perm
    pass

  print max_order
  return max_order
  pass

def pick_edge_weights(weights, predicted_labels, pairs, number_of_nodes):
  '''
  constructing adjacency matrix based on prediction probabilities
  '''
  ret = np.zeros((number_of_nodes, number_of_nodes))
  for i in xrange(len(pairs)):
    x,y = pairs[i].rstrip().split(',')
    x = int(x)
    y = int(y)
    #It is important to swap the precedence probabilities for 
    #the edges involved. prob(a precedes b) should be assigned to 
    #edge from b to a and vice versa

    # ret[x][y] = -1000 * math.log(weights[i][1], 2)
    # ret[y][x] = -1000 * math.log(weights[i][0], 2)
    ret[x][y] = weights[i][1]
    ret[y][x] = weights[i][0]
    #no need to assign weights based on pred labels, since we flip the indices (pairs) while preparing data
    # if(predicted_labels[i] == '+'):
    #   ret[x][y] = weights[i][1]
    #   ret[y][x] = weights[i][0]
    # elif predicted_labels[i] == '-':
    #   ret[x][y] = weights[i][0]
    #   ret[y][x] = weights[i][1]
    # else:
    #   print 'NOT POSSIBLE'

  return ret


def pick_stat_edge_weights(samples, pairs, number_of_nodes, stats_obj):
  '''
  constructing adjacency matrix based on CP1, CP2, CP3 and CP4
  '''
  ret = np.zeros((number_of_nodes, number_of_nodes))

  for i in xrange(len(pairs)):
    x,y = pairs[i].rstrip().split(',')
    x = int(x)
    y = int(y)

    sent1, sent2 = samples[i].split(sentSeparator)

    sem_group1 = get_sem_grouping(sent1)
    sem_group2 = get_sem_grouping(sent2)

    #probability of precedence should be flipped for TSP formulation
    #refer pick_edge_weights method for more details
    ret[x][y] = stats_obj.get_stat_based_edge_weight(sem_group2, sem_group1)
    ret[y][x] = stats_obj.get_stat_based_edge_weight(sem_group1, sem_group2)

    pass

  return ret
  pass


def prepare_tsp_solver_input(distances):
  '''
    Prepares adjacency matrix for the tsp instance
  '''
  return np.array(distances)


def tsp_solver(input):
  '''
    Solves the problem and returns the tsp solution
  '''
  import edu.sbu.eval.so.tsp.tsp_solver.src.tsp as tsp
  return tsp.solve_tsp_numpy(input, 10)


def tsp_dyn_solver(input):

  all_distances = input
  #initial value - just distance from 0 to every other point + keep the track of edges
  A = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in enumerate(all_distances[0][1:])}
  cnt = len(input[0])
  for m in range(2, cnt):
    B = {}
    for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
      for j in S - {0}:
        B[(S, j)] = min([(A[(S - {j}, k)][0] + all_distances[k][j], A[(S - {j}, k)][1] + [j]) for k in S if
                         k != 0 and k != j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
    A = B
  res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
  return res[1]
