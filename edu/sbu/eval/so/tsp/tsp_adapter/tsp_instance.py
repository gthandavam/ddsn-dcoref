__author__ = 'gt'

import numpy as np
import itertools
from edu.sbu.eval.so.features.ft_extraction import get_sem_grouping
from edu.sbu.eval.so.data.prepare_data import sentSeparator
import math

def log(n):
  return -100 if n == 0 else math.log(n)


def get_score(weights, pairs, perm):
  '''
    score(x) = sum( i 1 to n, j i+1 to n   P(i,j))
  '''
  score = 0.0
  for i in xrange(len(perm)):
    for j in xrange(i+1, len(perm)):
      pair = str(perm[i]) + ',' + str(perm[j])
      r_pair = str(perm[j]) + ',' + str(perm[i])
      if pair in pairs:
        k = pairs.index(pair)
        score += weights[k][0]
      elif r_pair in pairs:
        k = pairs.index(r_pair)
        score += weights[k][1]
      else:
        print 'not possible ' + pair

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

  print 'obj order:' + str(max_order)
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

    ret[x][y] = log(weights[i][0])
    ret[y][x] = log(weights[i][1])

  for i in range(number_of_nodes):
    ret[i][i] = -100.0

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

    #making use of log( values for min formulation
    p = stats_obj.get_stat_based_edge_prob(sem_group1, sem_group2)

    if p == 0 :
      ret[x][y] =  -100
    else:
      ret[x][y] = math.log(p)


    p = stats_obj.get_stat_based_edge_prob(sem_group2, sem_group1)
    if p == 0:
      ret[y][x] =  -100
    else:
      ret[y][x] = math.log(p)


    pass

  for i in range(number_of_nodes):
    ret[i][i] = -100.0

  return ret
  pass


def prepare_tsp_solver_input(distances):
  '''
    Prepares adjacency matrix for the tsp instance
  '''
  return np.array(distances)


def linKernSolver(distances, dishName, index, tsp_exp):
  '''
  Uses Concorde's Lin-Kernighan solver to find an approximate solution
  '''
  import os
  TSP_WORK_DIR = '/home/gt/Documents/TSP/' + dishName + '/'
  OUT_FILE = TSP_WORK_DIR + str(index) + '_' + tsp_exp +  '.out'
  IN_FILE = TSP_WORK_DIR + str(index) + '_' + tsp_exp +'.in'

  try:
    os.makedirs(TSP_WORK_DIR)
  except Exception as e:
    pass

  #CCutil_readint method picks the first integer that appears in the input file to get the number of nodes - so it is important the first number appears only in DIMENSION line
  with open(IN_FILE, 'w') as INP_F:
    INP_F.write('NAME: DUMMY_NAME\n')
    INP_F.write('TYPE: ATSP' + '\n')
    INP_F.write('COMMENT: Asymmetric TSP recipe instance' + '\n')
    INP_F.write('DIMENSION: ' + str(len(distances[0])) + '\n')
    INP_F.write('EDGE_WEIGHT_TYPE: EXPLICIT\n')
    INP_F.write('EDGE_WEIGHT_FORMAT: FULL_MATRIX\n')
    INP_F.write('EDGE_WEIGHT_SECTION\n')

    for i in xrange(len(distances[0])):
      for j in xrange(len(distances[0])):
        INP_F.write('    ' + str(distances[i][j]))

      INP_F.write('\n') #end of row

    INP_F.write('EOF')
    pass


  import commands
  stat, out = commands.getstatusoutput('/home/gt/LinKern-Concorde/src/concorde/LINKERN/linkern  -N 7 -o ' + OUT_FILE + ' ' + IN_FILE)

  if stat != 0:
    print dishName + ' ' + str(index) + ' LinKern error'
    print out
    # return []

  ret = []
  with open(OUT_FILE) as OUT_F:
    lines = OUT_F.readlines()
    #skipping first line of the output file
    for i in xrange(1, len(lines)):
      ret.append(int(lines[i].split(' ')[0]))


  return ret
  pass


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
  cnt = len(all_distances[0])
  # print A
  for m in range(2, cnt):
    B = {}
    for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
      for j in S - {0}:
        B[(S, j)] = min([(A[(S - {j}, k)][0] + all_distances[k][j], A[(S - {j}, k)][1] + [j]) for k in S if
                         k != 0 and k != j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
    A = B
  res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])

  # print res[0]
  return res[1]
