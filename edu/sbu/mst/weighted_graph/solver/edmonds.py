import sys
from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode

def _reverse(graph):
  r = {}
  for src in graph:
    for (dst,c) in graph[src].items():
      if dst in r:
        r[dst][src] = c
      else:
        r[dst] = { src : c }
  return r


def _getCycle(n,start_n,g,cycle,visited,global_visited,cycles,visited_in_cycle):
  global_visited.add(n)
  # cycle = []
  new_cycle = []
  for e in cycle:
    new_cycle += [e]
  new_cycle += [n]
  new_visited = set()
  for e in visited:
    new_visited.add(e)
  new_visited.add(n)
  # visited.add(n)
  if n not in g:
    return
  for e in g[n]:
    if e==start_n and visited_in_cycle!=len(cycle):
      cycles += [new_cycle]
    d = 0
    if e in global_visited:
      d+=1
    if e not in visited:
      _getCycle(e,start_n,g,new_cycle,new_visited,global_visited,cycles,visited_in_cycle+d)
  return

def _mergeCycles(cycle,connected_nodes,G,RG,g,rg):
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
      if e not in connected_nodes:
      # else:
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
  rmst(root,G,RG)

def rmst(root,G,RG):
  if root not in RG:
    return None
  RG[root] = {}
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
    if s==None:
      continue
    if d in g:
      g[d][s] = RG[s][d]
    else:
      g[d] = { s : RG[s][d] }

  cycles = []
  visited = set()
  for n in g:
    # if n not in visited:
      _getCycle(n,n,g,[],set(),visited,cycles,0)
      # cycle = _getCycle(n,g,[],visited)
      # cycles.append(cycle)

  rg = _reverse(g)
  for cycle in cycles:
    if root in cycle:
      continue
    _mergeCycles(cycle, get_connected_nodes(cycle,g), G, RG, g, rg)

  return g

def get_connected_nodes(cycle,g,visited=set()):
  for n in cycle:
    visited.add(n)
    if n in g:
      for e in g[n]:
        if e not in visited:
          get_connected_nodes([e],g,visited)
  return visited

def adjust_graph(g):
  a = {}
  nodes = {}
  for nd in g:
    nodes[nd] = 1
    for ch in g[nd]:
      nodes[ch] = 1
  # for n in nodes:
  #   if n not in g:
  #     g[n] = {}
  for nd in g:
    a[nd] = {}
    for ch in nodes.keys():
      if ch in g[nd]:
        a[nd][ch] = g[nd][ch]
      else:
        a[nd][ch] = sys.maxint
  return a

def getNodeText(label, id_node_map):
    node = id_node_map.get(label)
    text = str(label)
    if isinstance(node, PNode):
      text += "-"+str(node.predicate)
    elif isinstance(node, RNode):
      text += "-"+str(node.text)
    return text

def print_graph(g, id_node_map):
  for s in g:
    for t in g[s]:
      print "{}->({})->{}".format(getNodeText(s,id_node_map),getNodeText(g[s][t],id_node_map),getNodeText(t,id_node_map))

# def upside_down_arborescence(root, g, id_node_map):
def upside_down_arborescence(root, g, id_node_map):
  # if True:
  #   return g
  ag = adjust_graph(g)
  rag = _reverse(ag)
  h = rmst(root, rag, ag)
  # h = mst(root, g)

  if not h is None:
    res = _reverse(h)
    print_graph(res, id_node_map)
    return res
  else:
    print '*** None Arborescence ***'

  return None

def arborescence(root, g):
  h = mst(root, adjust_graph(g))

  return h


if __name__ == '__main__':
  g= {}
  # g['TD'] = {'T2t' : sys.maxint - 1, 'T3t' : sys.maxint - 1, 'T4t' : sys.maxint - 1, 'T2b' : sys.maxint - 1, 'T3b' : sys.maxint - 1, 'T4b' : sys.maxint - 1}
  g['T2t'] = {'T2b' : -100}
  g['T3t'] = {'T3b' : -100}
  g['T4t'] = {'T4b' : -100}

  g['T2b'] = {'T3t' : 40, 'T4t' : 60}
  g['T3b'] = {'T4t': 50}
  g['T4b'] = {'T3t' : sys.maxint - 1}
  root = 'T2t'

  arborescence(root, g)