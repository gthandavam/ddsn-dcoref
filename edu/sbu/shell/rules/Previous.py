__author__ = 'gt'


class Previous:

  def __init__(self):
    pass

  def run(self, pnodes, rnodes):
    for i in xrange(1, len(rnodes)):
      for j in xrange(len(rnodes[i])):
        prev_j = j-1 if j != 0 else len(rnodes[i-1]) - 1
        prev_i = i if j!= 0 else i-1
        for k in xrange(3):
          if not rnodes[i][j][k] is None:
            rnodes[i][j][k].shell_coref.append((prev_i, prev_j))

    return pnodes, rnodes