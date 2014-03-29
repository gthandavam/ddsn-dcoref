__author__ = 'gt'


class Previous:

  def __init__(self):
    pass

  def run(self, pnodes, rnodes):
    for i in xrange(1, len(rnodes)):
      for j in xrange(0, len(rnodes[i])):
        prev_j = j-1 if j != 0 else len(rnodes[i-1]) - 1
        prev_i = i if j!= 0 else i-1
        rnodes[i][j].shell_coref.append((prev_i, prev_j))

    return pnodes, rnodes