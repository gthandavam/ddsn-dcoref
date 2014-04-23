__author__ = 'gt'
import logging

class MSTGraphReverseTransformer:
  """
  Class responsible for transforming MST Graph to ShellDCoref graph
  """
  def __init__(self):
    self.logger = logging.getLogger('root')

  def transform(self, mst_graph):
    return mst_graph.pNodes, mst_graph.rNodes
    pass



  pass