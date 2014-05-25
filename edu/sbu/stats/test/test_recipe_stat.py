__author__ = 'gt'

from edu.sbu.stats.RecipeStats import RecipeStats

if __name__ == '__main__':
  hmm = RecipeStats('MacAndCheese')
  hmm.build_prob_dist()
  hmm.save_all()
  pass
