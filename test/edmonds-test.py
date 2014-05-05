import sys

# --------------------------------------------------------------------------------- #

# def _input(filename):
#   prices = {}
#   names = {}
#
#   for line in file(filename).readlines():
#     (name, src, dst, price) = line.rstrip().split()
#     name = int(name.replace('M',''))
#     src = int(src.replace('C',''))
#     dst = int(dst.replace('C',''))
#     price = int(price)
#     t = (src,dst)
#     if t in prices and prices[t] <= price:
#         continue
#     prices[t] = price
#     names[t] = name
#
#   return prices,names
#
# def _load(arcs,weights):
#   g = {}
#   for (src,dst) in arcs:
#     if src in g:
#       g[src][dst] = weights[(src,dst)]
#     else:
#       g[src] = { dst : weights[(src,dst)] }
#   return g

def _reverse(graph):
  r = {}
  for src in graph:
    for (dst,c) in graph[src].items():
      if dst in r:
        r[dst][src] = c
      else:
        r[dst] = { src : c }
  return r

def _getCycle(n,g,visited=set(),cycle=[]):
  visited.add(n)
  cycle += [n]
  if n not in g:
    return cycle
  for e in g[n]:
    if e not in visited:
      cycle = _getCycle(e,g,visited,cycle)
  return cycle

def _mergeCycles(cycle,G,RG,g,rg):
  allInEdges = []
  minInternal = None
  minInternalWeight = sys.maxint

  # find minimal internal edge weight
  for n in cycle:
    for e in RG[n]:
      if e in cycle:
        if minInternal is None or RG[n][e] < minInternalWeight:
          minInternal = (n,e)
          minInternalWeight = RG[n][e]
          continue
      else:
        allInEdges.append((n,e))

  # find the incoming edge with minimum modified cost
  minExternal = None
  minModifiedWeight = 0
  for s,t in allInEdges:
    u,v = rg[s].popitem()
    rg[s][u] = v
    w = RG[s][t] - (v - minInternalWeight)
    if minExternal is None or minModifiedWeight > w:
      minExternal = (s,t)
      minModifiedWeight = w

  u,w = rg[minExternal[0]].popitem()
  rem = (minExternal[0],u)
  rg[minExternal[0]].clear()
  if minExternal[1] in rg:
    rg[minExternal[1]][minExternal[0]] = w
  else:
    rg[minExternal[1]] = { minExternal[0] : w }
  if rem[1] in g:
    if rem[0] in g[rem[1]]:
      del g[rem[1]][rem[0]]
  if minExternal[1] in g:
    g[minExternal[1]][minExternal[0]] = w
  else:
    g[minExternal[1]] = { minExternal[0] : w }

# --------------------------------------------------------------------------------- #

def mst(root,G):
  """ The Chu-Lui/Edmond's algorithm

  arguments:

  root - the root of the MST
  G - the graph in which the MST lies

  returns: a graph representation of the MST

  Graph representation is the same as the one found at:
  http://code.activestate.com/recipes/119466/

  Explanation is copied verbatim here:

  The input graph G is assumed to have the following
  representation: A vertex can be any object that can
  be used as an index into a dictionary.  G is a
  dictionary, indexed by vertices.  For any vertex v,
  G[v] is itself a dictionary, indexed by the neighbors
  of v.  For any edge v->w, G[v][w] is the length of
  the edge.  This is related to the representation in
  <http://www.python.org/doc/essays/graphs.html>
  where Guido van Rossum suggests representing graphs
  as dictionaries mapping vertices to lists of neighbors,
  however dictionaries of edges have many advantages
  over lists: they can store extra information (here,
  the lengths), they support fast existence tests,
  and they allow easy modification of the graph by edge
  insertion and removal.  Such modifications are not
  needed here but are important in other graph algorithms.
  Since dictionaries obey iterator protocol, a graph
  represented as described here could be handed without
  modification to an algorithm using Guido's representation.

  Of course, G and G[v] need not be Python dict objects;
  they can be any other object that obeys dict protocol,
  for instance a wrapper in which vertices are URLs
  and a call to G[v] loads the web page and finds its links.
  """
  RG = _reverse(G)
  if root not in RG:
    return None
  RG[root].clear()
  g = {}
  for n in RG:
    if len(RG[n]) == 0:
      continue
    minimum = sys.maxint
    s,d = None,None
    for e in RG[n]:
      if RG[n][e] < minimum:
        minimum = RG[n][e]
        s,d = n,e
    if d in g:
      g[d][s] = RG[s][d]
    else:
      g[d] = { s : RG[s][d] }

  cycles = []
  visited = set()
  for n in g:
    if n not in visited:
      cycle = _getCycle(n,g,visited)
      cycles.append(cycle)

  rg = _reverse(g)
  for cycle in cycles:
    if root in cycle:
      continue
    _mergeCycles(cycle, G, RG, g, rg)

  return g

# --------------------------------------------------------------------------------- #

def arborescence(root, g):
  h = mst(root, g)

  for s in h:
    for t in h[s]:
      print "{}->{}".format(s,t)

  return h


if __name__ == '__main__':
  g= {}
  g['TD'] = {'T2t' : sys.maxint - 1, 'T3t' : sys.maxint - 1, 'T4t' : sys.maxint - 1, 'T2b' : sys.maxint - 1, 'T3b' : sys.maxint - 1, 'T4b' : sys.maxint - 1}
  g['T2t'] = {'T2b' : -100}
  g['T3t'] = {'T3b' : -100}
  g['T4t'] = {'T4b' : -100}

  g['T2b'] = {'T3t' : 40, 'T4t' : 30}
  g['T3b'] = {'T4t': 50}
  g['T4b'] = {'T3t' : 20}
  root = 'T2t'

  # g = _reverse(g)
  # g = {}
  # g['b'] = { 'c' : 10, 'a' : sys.maxint - 1}
  # g['c'] = { 'b' : 100, 'a' : sys.maxint - 1 }
  # g['a'] = {'b' : 10, 'c' : 1000}
  # root = 'a'
  arborescence(root, g)