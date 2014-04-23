__author__ = 'gt'

import logging
class Previous:

  def __init__(self):
    """
    Rule for handling null instantiations
    """
    self.logger = logging.getLogger('root')

    pass


  def find_previous(self, pnodes, find_i, find_j):

    for i in xrange(find_i, -1, -1):
      for j in xrange(len(pnodes[i]) - 1, -1, -1):
        if i == find_i and j >= find_j:
          continue

        if not pnodes[i][j] is None:
          # return i, j
          if len(set.intersection(pnodes[i][j].pIngs, pnodes[find_i][find_j].pIngs)) > 0:
            pnodes[find_i][find_j].pIngs = set.union(pnodes[i][j].pIngs, pnodes[find_i][find_j].pIngs)
            return i, j
        else:
          self.logger.warn('None Predicate found!!! ' + str(i) + ',' + str(j))

    return -1, -1

  def run(self, pnodes, rnodes):
    for i in xrange(1, len(rnodes)):
      for j in xrange(len(rnodes[i])):
        prev_i, prev_j = self.find_previous(pnodes, i, j)
          # i if j!= 0 else i-1
        if prev_i == -1 and prev_j == -1:
          continue

        for k in xrange(1,3):
          if rnodes[i][j][k].is_null:
            rnodes[i][j][k].shell_coref.append((prev_i, prev_j))
            break #only one of arg1 or arg2 needs to use prev as IArg


    return pnodes, rnodes