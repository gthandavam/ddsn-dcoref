__author__ = 'gt'

from edu.sbu.eval.user_eval.diff_edges import  intersect_edges, diff_edges

import os
testArchive = '/home/gt/Documents/UserEvaluation/'

if __name__ == '__main__':
  algoA = os.listdir(testArchive+'AlgoA')
  algoB = os.listdir(testArchive+'AlgoB')

  #algoA and algoB should have same length!!!
  for i in xrange(len(algoA)):
    with open(algoA[i]) as f:
      a_lines = f.readlines()

    with open(algoB[i]) as f:
      b_lines = f.readlines()

    a_diff_b, b_diff_a = diff_edges(a_lines, b_lines)
    

    pass



  pass