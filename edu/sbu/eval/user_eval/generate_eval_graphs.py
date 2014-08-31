__author__ = 'gt'

from edu.sbu.eval.user_eval.diff_edges import  common_graph_lines, diff_edges
import commands
import os
from random import randint


# recipeName = 'ChickenSalad'
recipeName = 'MacAndCheese'
# recipeName = 'EggNoodles'
# testArchiveOut = '/home/localdirs/NLPLab/Tools/google_appengine/projects/recipe-graphs/UserEvaluation-files/'+ recipeName + '/'
testArchiveOut = '/home/gt/Documents/IterGraphs/'+ recipeName + '/'
testArchive = '/home/gt/Documents/'+recipeName+'/'+recipeName+"-dot-files"
# testArchiveSVG = '/home/gt/Documents/'+recipeName+'/'+recipeName+"-svg-files"

def make_svg(gv_file, svg_file):
  #dot is in path
  status, output = commands.getstatusoutput('dot -Tsvg \"' + gv_file + '\" -o\"' + svg_file + '\"')

  #print output in case of any error
  if(status != 0):
    print output

  return status


if __name__ == '__main__':
  exp1 = '-learn_iteriter1'
  exp2 = '-learn_iteriter2'
  algoA = os.listdir(testArchive+exp1)
  # algoB = os.listdir(testArchive+'-run_wt')

  #algoA and algoB should have same length!!!
  for i in xrange(len(algoA)):
    A_file = testArchive+exp1 + '/' + algoA[i]
    B_file = testArchive+exp2 + '/' + algoA[i]
    try:
      f = open(B_file)
      f.close()
    except:
      continue

    with open(A_file) as f:
      a_lines = f.readlines()

    with open(B_file) as f:
      b_lines = f.readlines()

    a_diff_b, b_diff_a = diff_edges(a_lines, b_lines)
    a_diff_b.sort()
    b_diff_a.sort()
    # if "butternut-squash-mac-and-cheese" in algoA[i]:
    #   pass

    chosen_edge = -1
    if len(a_diff_b) > 0:
      chosen_edge = randint(0, len(a_diff_b) - 1)

    common = common_graph_lines(a_lines, b_lines)
    a_out = testArchiveOut+'MC_1_2_diff/' + algoA[i]
    b_out = testArchiveOut+'MC_2_1_diff/' + algoA[i]
    pass


    save_as_svg = False
    with open(a_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('}') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for j in xrange(len(a_diff_b)):
        if( j == chosen_edge):
          save_as_svg = True
          print algoA[i] + ' difference '
          f.write(a_diff_b[j].rstrip() + '[color=red]\n')
        else:
          f.write(a_diff_b[j])

      f.write('}')

    # a_svg = testArchiveSVG+'-run_init/' + algoA[i]
    # b_svg = testArchiveSVG+'-run_wt/' + algoA[i]
    a_svg = testArchiveOut+'MC_1_2_svg/' + algoA[i].replace(".gv",".svg")
    b_svg = testArchiveOut+'MC_2_1_svg/' + algoA[i].replace(".gv",".svg")
    if(save_as_svg):
      make_svg(a_out, a_svg)

    save_as_svg = False

    with open(b_out, 'w') as f:
      f.write('Digraph G {\n')
      for line in common:
        if line.find('}') != -1 or line.find('Digraph') != -1:
          continue
        f.write(line)

      for j in xrange(len(b_diff_a)):
        if( j == chosen_edge):
          save_as_svg = True
          f.write(b_diff_a[j].rstrip() + '[color=red]\n')
          print algoA[i] + ' difference '
        else:
          f.write(b_diff_a[j])

      f.write('}')

    if(save_as_svg):
      make_svg(b_out, b_svg)
  pass