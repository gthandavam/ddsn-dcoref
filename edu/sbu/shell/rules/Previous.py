__author__ = 'gt'


class Previous:

  def __init__(self):
    pass


  def find_previous(self, pnodes, find_i, find_j):
    prev_i = -1
    prev_j = -1
    #brute forcing for now - optmize later
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        if i == find_i and j == find_j:
          break

        if not pnodes[i][j] is None:
          prev_i = i
          prev_j = j

    return prev_i, prev_j

  def run(self, pnodes, rnodes):
    for i in xrange(1, len(rnodes)):
      for j in xrange(len(rnodes[i])):

        prev_i, prev_j = self.find_previous(pnodes, i, j)
          # i if j!= 0 else i-1
        for k in xrange(3):
          if not rnodes[i][j][k] is None:
            rnodes[i][j][k].shell_coref.append((prev_i, prev_j))

    return pnodes, rnodes