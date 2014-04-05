__author__ = 'gt'


class Previous:

  def __init__(self):
    """
    Rule for handling null instantiations
    """
    pass


  def find_previous(self, pnodes, find_i, find_j):

    for i in xrange(find_i, -1, -1):
      for j in xrange(len(pnodes[i]) - 1, -1, -1):
        if i == find_i and j >= find_j:
          break

        if not pnodes[i][j] is None:
          return i, j
        else:
          print 'None Predicate found!!! ' + str(i) + ',' + str(j)

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

    return pnodes, rnodes