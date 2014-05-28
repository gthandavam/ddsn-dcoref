__author__ = 'gt'

import commands
from random import randint

trainFile = 'trainFilesList'
testFile  = 'testFilesList'
devFile   = 'devFilesList'

def split_recipes():
  print 'files already split'
  return
  recipes = []
  with open(trainFile, 'w') as train, open(testFile, 'w') as test, open(devFile, 'w') as dev:
    for recipe_args_file in commands.getoutput('ls /home/gt/Documents/MacAndCheese/MacAndCheeseArgs/*.txt').split('\n'):
      recipes.append(recipe_args_file)

      ri = randint(1,100)

      if ri <= 60:
        train.write(recipe_args_file + '\n')
        pass
      elif ri > 60 and ri <= 80:
        dev.write(recipe_args_file + '\n')
        pass
      else:
        test.write(recipe_args_file + '\n')
        pass


  pass


if __name__ == '__main__':
  split_recipes()