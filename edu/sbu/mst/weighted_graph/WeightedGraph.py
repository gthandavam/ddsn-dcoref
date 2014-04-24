__author__ = 'gt'
import logging
class WeightedGraph:
  def __init__(self, pNodes, rNodes, weight_heuristic):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.vertex_list = []
    self.edge_list = self.get_edge_list(rNodes)
    self.weight_heuristic = weight_heuristic
    self.logger = logging.getLogger('root')
    pass

  def get_edge_list(self):
    """
    process pNodes and rNodes to get edges
    """
    ret = []
    return ret

  def get_vertex_list(self):
    """
    process pNodes and rNodes to get island vertices
    """
    ret = []
    return ret

  def add_edges(self, edge_list):
    self.edge_list.extend(edge_list)

  def identify_islands(self):
    pass

  def add_edges_between_islands(self, island1, island2):
    pass

  pass