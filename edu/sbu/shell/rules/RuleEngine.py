__author__ = 'gt'

from edu.sbu.shell.rules.Previous import Previous
from edu.sbu.shell.rules.ArgString import ArgString
from edu.sbu.shell.rules.DerivationallyRelated import DerivationallyRelated
from edu.sbu.shell.rules.GlossBased import GlossBased

class RuleEngine:
  def __init__(self):
    #tuple of rules - Immutable
    self.rules = (
      'Previous',
      # 'ArgString',
      # 'DerivationallyRelated',
      # 'GlossBased',
    )

  def apply_rules(self, dcoref_graph):
    for rule in self.rules:
      rule_obj = globals()[rule]()
      pnodes, rnodes = rule_obj.run(dcoref_graph.PNodes, dcoref_graph.RNodes)


    return pnodes, rnodes

