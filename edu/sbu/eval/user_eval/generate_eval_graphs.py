__author__ = 'gt'

from edu.sbu.eval.user_eval.diff_edges import  common_graph_lines, diff_edges
import commands
import os
from random import randint

testArchive = '/home/gt/Documents/UserEvaluation/'


def make_svg(gv_file, svg_file):
  #dot is in path
  status, output = commands.getstatusoutput('dot -Tsvg \"' + gv_file + '\" -o\"' + svg_file + '\"')

  #print output in case of any error
  if(status != 0):
    print output

  return status


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
    a_diff_b.sort()
    b_diff_a.sort()

    chosen_edge = 0
    if len(a_diff_b) > 0:
      chosen_edge = randint(0, len(a_diff_b) - 1)

    common = common_graph_lines(a_lines, b_lines)
    a_out = A_file.replace('AlgoA', 'AlgoA_diff')
    b_out = B_file.replace('AlgoB', 'AlgoB_diff')
    pass


    save_as_svg = False
    with open(a_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('};') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for i in xrange(len(a_diff_b)):
        if( i == chosen_edge):
          save_as_svg = True
          f.write(a_diff_b[i].rstrip() + '[color=red]\n')
        else:
          f.write(a_diff_b[i])

      f.write('};')

    a_svg = a_out.replace('AlgoA_diff', 'AlgoA_svg')
    a_svg = a_svg.replace('.gv', '.svg')
    if(save_as_svg):
      make_svg(a_out, a_svg)

    save_as_svg = False

    with open(b_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('};') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for i in xrange(len(b_diff_a)):
        if( i == chosen_edge):
          save_as_svg = True
          f.write(b_diff_a[i].rstrip() + '[color=red]\n')
        else:
          f.write(b_diff_a[i])

      f.write('};')

    b_svg = b_out.replace('AlgoB_diff', 'AlgoB_svg')
    b_svg = b_svg.replace('.gv', '.svg')
    if(save_as_svg):
      make_svg(b_out, b_svg)
  pass