__author__ = 'gt'

from edu.sbu.mst.MSTGraphTransformer import MSTGraphTransformer
from edu.sbu.mst.MSTGraphReverseTransformer import MSTGraphReverseTransformer
import logging
class MSTGraphAdapter:
  """
  It is actually only an adapter between MSTGraph and DCoref Graph

  Assuming adapter is responsible for transformation and reverse transformation
  here

  Uses MSTGraphTransformer and MSTGraphReverseTransformer
  """
  def __init__(self):
    self.pnodes = []
    self.rnodes = []
    self.mst_graph = None
    self.logger = logging.getLogger('root')

  def transform(self, pnodes, rnodes):
    transformer = MSTGraphTransformer()
    self.pnodes = pnodes
    self.rnodes = rnodes
    self.mst_graph = transformer.transform(pnodes, rnodes)
    return self.mst_graph
    pass

  def reverse_transform(self):
    transformer = MSTGraphTransformer()
    self.pnodes, self.rnodes = transformer.reverse_transform()
    return self.pnodes,self.rnodes
    pass
  pass