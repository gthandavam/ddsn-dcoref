__author__ = 'gt'
import logging
class WeightedGraph:
  def __init__(self, pNodes, rNodes, weight_heuristic):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.edge_list = self.get_edge_list(rNodes)
    self.weight_heuristic = weight_heuristic
    self.logger = logging.getLogger('root')
    pass

  def get_edge_list(self, rNodes):
    ret = []
    #process rNodes to get edges
    return ret

  def add_edges(self, edge_list):
    self.edge_list.extend(edge_list)

  pass