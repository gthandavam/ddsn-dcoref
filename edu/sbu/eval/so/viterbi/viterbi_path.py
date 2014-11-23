__author__ = 'gt'

import numpy as np
import math
import copy

def objective_function(curr_state, next_state, prev_path, prob_matrix):
  '''
  returns Sum(wt_matrix[prev_path[i]][next_state])  : i varies over length of path
  '''
  ret = 0

  for i in xrange(len(prev_path[curr_state])):
    ret += prob_matrix[next_state][prev_path[curr_state][i]]

  return ret
  pass

def get_viterbi_path(prob_matrix):
  '''
  Return the (min) viterbi path given the log prob matrix
  '''

  #in this formulation, no of observations == no of states
  n = len(prob_matrix) #no of states == no of obs
  # print wt_matrix

  V_dp_table = [[-100000 for x in xrange(n)] for x in xrange(n)]
  path = {}

  for i in xrange(n):
    if i== 0:
      V_dp_table[0][i] = 0 #log(1) == 0 #initializing for first observation, uniform
    else:
      V_dp_table[0][i] = -100
    path[i] = [i]

  # Run Viterbi from 2nd observation
  for t in xrange(1, n):
    newpath = {}

    for y in xrange(n):
      # candidates = [(V_dp_table[t-1][y0] + prob_matrix[y0][y], y0) for y0 in xrange(n) if y not in path[y0]]
      candidates = [(V_dp_table[t-1][y0] + objective_function(y0, y, path, prob_matrix), y0) for y0 in xrange(n) if y not in path[y0]]
      if(len(candidates) != 0):
        (prob, state) = max(candidates)
      else:
        print 'check this'
        newpath[y] = copy.deepcopy(path[y])
        newpath[y].append(y)
        V_dp_table[t][y] = -1000000
        continue

      V_dp_table[t][y] = prob
      newpath[y] = copy.deepcopy(path[state])
      newpath[y].append(y)

    # No need to remember the old paths
    path = newpath

  last_obs = n - 1

  (prob, state) = max((V_dp_table[last_obs][y], y) for y in xrange(n))

  # print V_dp_table
  print path, state
  return path[state]

  pass


if __name__ == '__main__':
  wt_m = [[  -100000,  -5.65288875e+00,  -8.15378581e+00,  -8.44961230e+00,
   -8.53410221e+00,  -7.82074549e+00,  -8.56745110e+00,  -1.12419325e+01,
   -9.60010851e+00,  -1.39255675e+01,  -8.07181007e+00,  -1.22128097e+01,],
 [ -3.51353546e-03,   -100000,  -2.07956243e+00,  -1.18617232e+00,
   -2.04567892e+00,  -1.60721619e+00,  -3.34006839e+00,  -6.37913834e+00,
   -3.75236290e+00,  -7.49668495e+00, -2.00820725e+00,  -6.52143384e+00,],
 [ -2.87685706e-04,  -1.33514124e-01,   -100000,  -1.44944805e-01,
   -3.80056033e-01,  -2.42031548e-01,  -1.06582567e+00,  -3.70338529e+00,
   -1.36573667e+00,  -4.81837512e+00,  -3.66610818e-01,  -3.84498439e+00,],
 [ -2.14006259e-04,  -3.64401802e-01,  -2.00299945e+00,   -100000,
   -6.26977548e-01,  -1.45508765e-01,  -6.76509088e-01,  -4.22436450e+00,
   -2.80197153e+00,  -5.77100755e+00,  -4.37744622e-01,  -3.54565742e+00,],
 [ -1.96665965e-04,  -1.38449042e-01,  -1.15145338e+00,  -7.64007443e-01,
    -100000,  -2.73032540e-01,  -1.16571107e+00,  -3.83931769e+00,
   -1.46921648e+00,  -4.95490685e+00,  -4.10557638e-01,  -3.98107878e+00,],
 [ -4.01402940e-04,  -2.23699754e-01,  -1.53726336e+00,  -1.99939129e+00,
   -1.43157638e+00,   -100000,  -1.75353899e+00,  -4.60880671e+00,
   -2.10839415e+00,  -5.72593284e+00,  -7.40865151e-01,  -4.75098644e+00,],
 [ -1.90214915e-04,  -3.60775736e-02,  -4.22270543e-01,  -7.10066790e-01,
   -3.73531858e-01,  -1.90144129e-01,   -100000,  -4.20094457e+00,
   -2.77994264e+00,  -5.74754084e+00,  -4.29487508e-01,  -3.52237107e+00,],
 [ -1.31127443e-05,  -1.69802503e-03,  -2.49486164e-02,  -1.47427746e-02,
   -2.17429456e-02,  -1.00136707e-02,  -1.50947741e-02,   -100000,
   -9.73902797e-02,  -2.16869404e+00,  -2.19753575e-02,  -8.73626541e-01,],
 [ -6.77236809e-05,  -2.37418621e-02,  -2.94629636e-01,  -6.26100265e-02,
   -2.61502056e-01,  -1.29462895e-01,  -6.40501774e-02,  -2.37732884e+00,
    -100000,  -2.55088289e+00,  -4.13926410e-02,  -1.69683488e+00,],
 [ -8.95783518e-07,  -5.55074940e-04,  -8.11272468e-03,  -3.12148255e-03,
   -7.07369657e-03,  -3.26563689e-03,  -3.19571826e-03, -1.21407275e-01,
   -8.12238942e-02,   -100000,  -5.01987892e-03,  -2.74875574e-01,],
 [ -3.12266384e-04,  -1.44134954e-01,  -1.18116596e+00,  -1.03702043e+00,
   -1.08850438e+00,  -6.47602885e-01,  -1.05223234e+00,  -3.82880113e+00,
   -3.20527710e+00,  -5.29685836e+00,   -100000,  -4.33464783e+00,],
 [ -4.96644043e-06,  -1.47264141e-03,  -2.16187455e-02,  -2.92739823e-02,
   -1.88418914e-02,  -8.68073381e-03,  -2.99741045e-02,  -5.40314436e-01,
   -2.02437723e-01,  -1.42572832e+00,  -1.31931369e-02,   -100000]]

  print get_viterbi_path(wt_m)

  wt_m = [[-100, math.log(0.7), math.log(0.2)], [-100, -100, math.log(0.6)], [math.log(0.1), math.log(0.1), math.log(0.2)]]

  print get_viterbi_path(wt_m)

  wt_m_1 = [[-100,-100,0,-100], [0,-100,-100,-100], [-100,-100,-100,0], [-100,0,-100,-100]]
  print get_viterbi_path(wt_m_1)