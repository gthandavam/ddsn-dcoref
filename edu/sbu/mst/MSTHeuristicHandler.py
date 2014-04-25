__author__ = 'gt'
import logging
class MSTHeuristicHandler:
  """
  Interface for different heuristics for assigning
  edge weights
  """

  def __init__(self):
    self.logger = logging.getLogger('root')

  def get_weights(self, pNodes, rNodes, edge_list, heuristic):

    return edge_list
    pass

  pass