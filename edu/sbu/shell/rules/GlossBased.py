__author__ = 'gt'
import logging
class GlossBased:
  def __init__(self):
    self.logger = logging.getLogger('root')

  def run(self, pnodes, rnodes):
    return pnodes, rnodes