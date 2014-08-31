__author__ = 'gt'


import commands
import sys
from shutil import copyfile

def learn_arbor(num_iter, recipe):
  expName = 'arbor'
  cmd = 'python Transformer.py -learn_init ' + recipe + ' ' + expName + ' -no_trans '
  out = commands.getoutput(cmd)
  print out

  for i in xrange(num_iter):
    cmd = 'python Transformer.py -learn_iter ' + recipe + ' ' + expName + ' -no_trans ' + str(i)
    out = commands.getoutput(cmd)
    print out
    #copying output of this iteration to be input for next iteration
    statFile = "/home/gt/Documents/"+ recipe + "/" + expName + "/RecipeStats2_init.pickle"
    statFile2 = "/home/gt/Documents/" + recipe + "/" + expName +  "/RecipeStats2_iter.pickle"
    copyfile(statFile2, statFile)


  cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe + ' ' + expName + ' -no_trans ' + str(100)
  out = commands.getoutput(cmd)
  print out

def learn_arbor_trans(num_iter, recipe):
  expName = 'arbor_trans'
  cmd = 'python Transformer.py -learn_init ' + recipe + ' ' + expName + ' -trans '
  out = commands.getoutput(cmd)
  print out

  for i in xrange(num_iter):
    cmd = 'python Transformer.py -learn_iter ' + recipe + ' ' + expName + ' -trans ' + str(i)
    out = commands.getoutput(cmd)
    print out
    #copying output of this iteration to be input for next iteration
    statFile = "/home/gt/Documents/"+ recipe +  "/" + expName +  "/RecipeStats2_init.pickle"
    statFile2 = "/home/gt/Documents/" + recipe +  "/" + expName + "/RecipeStats2_iter.pickle"
    copyfile(statFile2, statFile)

  cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe + ' ' + expName +  ' -trans'
  # cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe
  out = commands.getoutput(cmd)
  print out


def learn_cc(num_iter, recipe):
  expName = 'cc'
  cmd = 'python Transformer.py -learn_init ' + recipe + ' ' + expName
  out = commands.getoutput(cmd)
  print out

  # cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe + '  -trans'
  cmd = 'python Transformer.py -stat_for_eval_cc ' + recipe + ' ' + expName
  out = commands.getoutput(cmd)
  print out


  pass


def learn_text_order(num_iter, recipe):
  expName = 'text_order'
  cmd = 'python Transformer.py -learn_init ' + recipe + ' ' + expName
  out = commands.getoutput(cmd)
  print out

  # cmd = 'python Transformer.py -stat_for_eval_iter ' + recipe + '  -trans'
  cmd = 'python Transformer.py -stat_for_eval_wt ' + recipe + ' ' + expName
  out = commands.getoutput(cmd)
  print out


  pass

if __name__ == '__main__':
  try:
    learn_arbor(int(sys.argv[1]), sys.argv[2])
    # learn_arbor_trans(int(sys.argv[1]), sys.argv[2])
    # learn_cc(int(sys.argv[1]), sys.argv[2])
    # learn_text_order(int(sys.argv[1]), sys.argv[2])
  except Exception as inst:
    print inst.args
    print inst.message
    print 'usage:python iterative_learning.py number_of_iterations  recipe_name'