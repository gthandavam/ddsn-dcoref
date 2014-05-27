__author__ = 'gt'

from edu.sbu.stats.RecipeStats import RecipeStats

if __name__ == '__main__':
  stats = RecipeStats('MacAndCheese')
  stats.build_prob_dist()

  print 'here'
  # print stats.v_prev_v_arg2_p_arg[()]
  #
  # print stats.v_prev_v_arg1_p_arg[()]

  pass
