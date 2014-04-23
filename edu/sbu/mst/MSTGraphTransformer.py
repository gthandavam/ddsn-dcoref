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

  def transform(self, pnodes, rnodes):
    mst_graph = WeightedGraph(pnodes, rnodes)
    return mst_graph
    pass

  pass