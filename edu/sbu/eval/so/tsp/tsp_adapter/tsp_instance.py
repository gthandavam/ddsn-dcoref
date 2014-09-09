__author__ = 'gt'

import numpy as np
import math
import itertools

def pick_edge_weights(weights, predicted_labels, pairs, nodes):
  ret = np.zeros((nodes, nodes))
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

  return ret


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
