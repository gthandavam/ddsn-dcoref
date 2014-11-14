__author__ = 'gt'

import numpy as np

def get_viterbi_path(wt_matrix):
  '''
  Return the (min) viterbi path given the log weighted matrix
  '''

  #in this formulation, no of observations == no of states
  n = len(wt_matrix) #no of states == no of obs

  V_dp_table= [np.zeros(n)] * n # n * n matrix
  path = []

  for i in xrange(n):
    V_dp_table[0][i] = wt_matrix[0][i] #initializing for first observation
    path[i] = [i]

  # Run Viterbi from 2nd observation
  for t in xrange(1, n):
    newpath = [[]] * n

    for y in range(n):
      (prob, state) = min((V_dp_table[t-1][y0] + wt_matrix[y0][y], y0) for y0 in xrange(n))
      V_dp_table[t][y] = prob
      newpath[y] = path[state].append(y)

    # No need to remember the old paths
    path = newpath

  last_obs = n - 1

  (prob, state) = min((V_dp_table[last_obs][y], y) for y in xrange(n))

  return path[state]

  pass