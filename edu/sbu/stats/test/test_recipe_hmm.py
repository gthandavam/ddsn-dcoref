__author__ = 'gt'

from edu.sbu.stats.RecipeHMM import RecipeHMM

if __name__ == '__main__':
  hmm = RecipeHMM('MacAndCheese')
  hmm.build_prob_dist()
  pass
