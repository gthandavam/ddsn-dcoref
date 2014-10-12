__author__ = 'gt'

from edu.sbu.shell.rules.IArgHeuristics import Previous
from edu.sbu.shell.rules.ArgString import ArgString
from edu.sbu.shell.rules.DerivationallyRelated import DerivationallyRelated
from edu.sbu.shell.rules.GlossBased import GlossBased
from edu.sbu.shell.rules.HeadWordArgString import HeadWordArgString
import logging
class RuleEngine:
  def __init__(self):
    #tuple of rules - Immutable
    self.rules = (

    'GlossBased', #not implemented
      'DerivationallyRelated',
      'HeadWordArgString',#not implemented
      'ArgString',
    'Previous', #-> IArgHeuristics here


    )
    self.logger = logging.getLogger('root')

  def apply_rules(self, dcoref_graph):
    """
    No Rule but Previous should act on RNode when it is a  null instantiation
    When RNode obj.is_null is True -> Only 'Previous' Rule acts on it
    """
    for rule in self.rules:
      rule_obj = globals()[rule]()
      pnodes, rnodes = rule_obj.run(dcoref_graph.PNodes, dcoref_graph.RNodes)

    return pnodes, rnodes