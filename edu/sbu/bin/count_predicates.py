__author__ = 'gt'

import sys
from edu.sbu.stats.corpus.reader2 import RecipeReader2


def main(dishName):
  print "processing " + dishName
  reader = RecipeReader2(dishName)
  cnt = 0
  for recipe_index in xrange(len(reader.recipe_verbs)):
    for sent_index in xrange(len(reader.recipe_verbs[recipe_index])):
      cnt += len(reader.recipe_verbs[recipe_index][sent_index])

  print "total: " + str(cnt)
  print "average: " + str(cnt/len(reader.recipe_verbs))
  pass

if __name__ == '__main__':
  main(sys.argv[1])