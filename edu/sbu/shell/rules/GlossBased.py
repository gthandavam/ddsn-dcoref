__author__ = 'gt'
import logging

class GlossBased:
  """
  This rule was added to handle relations such as :
  batter : Mixture of flour, water, salt etc..,
  fond   : sauce scraped of the vessel used for grilling meat ?
    Can this be captured ?
  """
  def __init__(self):
    self.logger = logging.getLogger('root')

  def run(self, pnodes, rnodes):
    return pnodes, rnodes