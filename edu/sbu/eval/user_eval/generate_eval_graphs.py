__author__ = 'gt'

from edu.sbu.eval.user_eval.diff_edges import  common_graph_lines, diff_edges

import os
recipeName = 'MacAndCheese'
testArchive = '/home/gt/Documents/UserEvaluation/'+ recipeName + '/'

if __name__ == '__main__':
  algoA = os.listdir(testArchive+'AlgoA')
  algoB = os.listdir(testArchive+'AlgoB')

  #algoA and algoB should have same length!!!
  for i in xrange(len(algoA)):
    A_file = testArchive + '/AlgoA/' + algoA[i]
    B_file = testArchive + '/AlgoB/' + algoB[i]
    with open(A_file) as f:
      a_lines = f.readlines()

    with open(B_file) as f:
      b_lines = f.readlines()

    a_diff_b, b_diff_a = diff_edges(a_lines, b_lines)
    common = common_graph_lines(a_lines, b_lines)
    a_out = A_file.replace('AlgoA', 'AlgoA_diff')
    b_out = B_file.replace('AlgoB', 'AlgoB_diff')
    pass

    with open(a_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('};') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for line in a_diff_b:
        f.write(line.rstrip() + '[color=red]\n')

      f.write('};')

    with open(b_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('};') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for line in b_diff_a:
        f.write(line.rstrip() + '[color=red]\n')

      f.write('};')

  pass