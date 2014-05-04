__author__ = 'gt'

from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.mst.weighted_graph.WeightedGraph import WeightedGraph
from edu.sbu.shell.semgraph.PNode import PNode
import logging
class MSTGraphTransformer:
  """
  Transforms the ShellDCoref graph for the MST formulation.
  Uses MST Heuristic Handler to assign weights to the edges
  """

  def __init__(self):
    self.logger = logging.getLogger('root')
    self.adj_list = {}
    self.v_props = {}
    self.id_node_map = {}
    self.dot_builder = None

    self.ccs = []


  def reverse_transform(self, mst_graph, mst_edges):

    # for mst_edge in mst_edges:
    #   from_node = self.id_node_map[mst_edge[0]]
    #
    #   if not isinstance(from_node, PNode):
    #     self.logger.error('CC Edge starting from an RNode ?')
    #     continue
    #
    #   from_node.cc_edge.append(mst_edge[1])

    return mst_graph.pNodes, mst_graph.rNodes
    pass

  def print_ccs(self):
    for cc in self.ccs:
      self.logger.error(cc)

  def print_v_props(self):
    for key in self.v_props.keys():
        if self.v_props[key][1] == 0 and self.v_props[key][2] == 1:
          self.logger.error(' {} : bottom ; cc = {}'.format(key, self.v_props[key][0]))
        elif self.v_props[key][1] == 1 and self.v_props[key][2] == 0:
          self.logger.error(' {} : top ; cc = {}'.format(key, self.v_props[key][0]))
        elif self.v_props[key][1] == 1 and self.v_props[key][1] == 1:
          self.logger.error(' {} : middle ; cc = {}'.format(key, self.v_props[key][0]))
        else:
          self.logger.error('null instant replaced with a pred (shell coref) node number {} ; cc {}'.format(key, self.v_props[key][0]))

  def transform(self, pnodes, rnodes):
    self.dot_builder = DotGraphBuilder()
    self.adj_list, self.id_node_map  = self.dot_builder.get_edge_list_mst(pnodes, rnodes)

    for key in self.adj_list.keys():
      self.v_props[key] = [-1,0,0]

    self.mark_top_bottom_nodes()
    self.adj_list = self.directed_to_undirected()
    self.ccs = self.get_connected_components()
    weighted_graph = WeightedGraph(pnodes, rnodes, self.ccs, self.v_props, self.id_node_map)

    weighted_graph.print_edges()

    return weighted_graph
    pass

  def dfs(self, node, tkr, ccs):
    # global adj_list #not needed for reading
    self.v_props[node][0] = tkr
    for neighbor in self.adj_list[node]:
      if self.v_props[neighbor][0] == -1: #if node not visited
        ccs[tkr] = set.union(ccs[tkr], set([neighbor]))
        self.v_props[neighbor][0] = tkr
        ccs = self.dfs(neighbor, tkr, ccs)

    return ccs

  def get_connected_components(self):
    tkr = 0
    ccs = []
    # global v_props # no need for reading
    for node in self.v_props.keys():
      if self.v_props[node][0] == -1:
        ccs.append(set([node]))
        ccs = self.dfs(node, tkr, ccs)
        tkr += 1

    return ccs
    pass

  def mark_top_bottom_nodes(self):
    """
    marks the flags to find 'active' nodes per connected component
    """
    for key in self.adj_list.keys():
      for neighbor in self.adj_list[key]:
        self.v_props[key][1] = 1
        self.v_props[neighbor][2] = 1
    pass

  def directed_to_undirected(self):
    ret = dict((key,[]) for key in self.adj_list.keys())
    for key in self.adj_list.keys():
      for neighbor in self.adj_list[key]:
        ret[key].append(neighbor)
        ret[neighbor].append(key)

    return ret
    pass