__author__ = 'gt'

"""kruskal.py
Reference: http://www.ics.uci.edu/~eppstein/PADS/MinimumSpanningTree.py
Kruskal's algorithm for minimum spanning trees. D. Eppstein, April 2006.
"""

from UnionFind import UnionFind

def kruskal_mst(edges):
  """
  Return the minimum spanning tree of an undirected graph G.
  G should be represented in such a way that G[u][v] gives the
  length of edge u,v, and G[u][v] should always equal G[v][u].
  The tree is returned as a list of edges.
  """

  # Kruskal's algorithm: sort edges by weight, and add them one at a time.
  # We use Kruskal's algorithm, first because it is very simple to
  # implement once UnionFind exists, and second, because the only slow
  # part (the sort) is sped up by being built in to Python.
  subtrees = UnionFind()
  mst_edges = []
  edges.sort()
  for W,u,v in edges:
      if subtrees[u] != subtrees[v]:
          mst_edges.append((u,v))
          subtrees.union(u,v)
  return mst_edges