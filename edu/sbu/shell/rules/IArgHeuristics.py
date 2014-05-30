__author__ = 'gt'

import logging
class Previous:

  def __init__(self):
    """
    IArg rule doesnt (and may be shouldnt rely) on ingredients involved.
    It implicitly refers to the preceding sentence
    """
    self.logger = logging.getLogger('root')
    pass


  def find_previous(self, pnodes, find_i, find_j):

    for i in xrange(find_i, -1, -1):
      for j in xrange(len(pnodes[i]) - 1, -1, -1):
        if i == find_i and j >= find_j:
          continue

        if not pnodes[i][j] is None:
          return i, j
          # if len(set.intersection(pnodes[i][j].pIngs, pnodes[find_i][find_j].pIngs)) > 0:
          #   return i, j
        else:
          self.logger.warn('None Predicate found!!! ' + str(i) + ',' + str(j))

    return -1, -1

  def run(self, pnodes, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        prev_i, prev_j = self.find_previous(pnodes, i, j)
          # i if j!= 0 else i-1
        if prev_i == -1 and prev_j == -1:
          continue

        if not self.allow_Iarg(pnodes, rnodes, i,j, prev_i, prev_j):
          continue

        for k in xrange(1,3):
          if rnodes[i][j][k].is_null:
            rnodes[i][j][k].shell_coref.append(((prev_i, prev_j), 'IArgHeuristics'))
            self.logger.error('IArg Edge')
            #Updating ing flow upon resolving null arg
            pnodes[i][j].pIngs = set.union(pnodes[i][j].pIngs, pnodes[prev_i][prev_j].pIngs)
            #updating rnode argIngs as well, just in case
            rnodes[i][j][k].argIngs = set.union(rnodes[i][j][k].argIngs, pnodes[prev_i][prev_j].pIngs)
            #to avoid parallel IArg edges between predicates
            #only one of arg1 or arg2 needs to use prev as IArg
            #so when arg1 and arg2 are null, only arg1 has IArg edge
            break

    return pnodes, rnodes

  def allow_Iarg(self, pnodes, rnodes, i, j, prev_i, prev_j):
    '''
    Method to avoid (indirect) IArg parallel edges between predicate nodes

    Test Case:
    kicked-up-mac-and-cheese (All Recipes Mac And Cheese data
    '''
    #TODO: Once IArg rule is run first, this method becomes obviated
    for k in xrange(1,3):
      if len(rnodes[i][j][k].shell_coref) > 0:
        shell_i, shell_j = rnodes[i][j][k].shell_coref[0][0]
        if shell_i == prev_i and shell_j == prev_j:
          return False

    return True