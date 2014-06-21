__author__ = 'gt'

import commands
import sys
from shutil import copyfile
from edu.sbu.shell.Transformer import statFile, statFile2
def main(num_iter, recipe):
  cmd = 'python Transformer.py -learn_init ' + recipe
  out = commands.getoutput(cmd)
  print out

  for i in xrange(num_iter):
    cmd = 'python Transformer.py -learn_iter ' + recipe
    out = commands.getoutput(cmd)
    print out
    #copying output of this iteration to be input for next iteration
    copyfile(statFile2, statFile)

  cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe
  out = commands.getoutput(cmd)
  print out


  pass


if __name__ == '__main__':
  try:
    main(int(sys.argv[1]), sys.argv[2])
  except Exception as inst:
    print inst.args
    print inst.message
    print 'usage:python iterative_learning.py number_of_iterations  recipe_name'