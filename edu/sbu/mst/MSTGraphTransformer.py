__author__ = 'gt'

from edu.sbu.mst.MSTHeuristicHandler import MSTHeuristicHandler
from edu.sbu.mst.weighted_graph.WeightedGraph import WeightedGraph
import logging
class MSTGraphTransformer:
  """
  Transforms the ShellDCoref graph for the MST formulation.
  Uses MST Heuristic Handler to assign weights to the edges
  """

  def __init__(self):
    self.logger = logging.getLogger('root')
    self.adj_list = []
    self.v_props = []

  def transform(self, pnodes, rnodes):
    mst_graph = WeightedGraph(pnodes, rnodes)
    return mst_graph
    pass

  def dfs(self, node, tkr, ccs):
    global v_props
    # global adj_list #not needed for reading
    v_props[node][0] = tkr
    for neighbor in self.adj_list[node]:
      if v_props[neighbor][0] == -1: #if node not visited
        ccs[tkr] = set.union(ccs[tkr], set([neighbor]))
        v_props[neighbor][0] = tkr
        ccs = dfs(neighbor, tkr, ccs)

    return ccs


  def get_connected_components(self, adj_list):
    tkr = 0
    ccs = []
    # global v_props # no need for reading


    for node in xrange(len(self.v_props)):
      if self.v_props[node][0] == -1:
        ccs.append(set([node]))
        ccs = self.dfs(node, tkr, ccs)
        tkr += 1

    return ccs
    pass

  def get_top_bottom_nodes(self, adj_list):
    for i in xrange(len(adj_list)):
      for neighbor in adj_list[i]:
        self.v_props[i][1] = 1
        self.v_props[neighbor][2] = 1
    pass

  def directed_to_undirected(self, adj_list):
    ret = [[] for i in xrange(len(adj_list)) ]
    for i in xrange(len(adj_list)):
      for neighbor in adj_list[i]:
        ret[i].append(neighbor)
        ret[neighbor].append(i)

    return ret


  pass