__author__ = 'gt'

import logging
class HeadWordArgString:

  def __init__(self):
    self.logger = logging.getLogger('root')
    pass

  def run(self, pnodes, rnodes):
    return pnodes, rnodes