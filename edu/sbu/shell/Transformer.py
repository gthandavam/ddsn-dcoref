__author__ = 'gt'

from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.shell.RuleEngine import RuleEngine
from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode



def get_text(recipe_file):
  """
  returns the text in array of sentences
  removes empty sentences
  """
  pass

def get_semantic_parsing(recipe):
  """
  Runs a SRL tool to get pred argument structure and
  returns pnodes and rnodes
  """
  pass

def make_svg(gv_file):
  pass

def main():
  for recipe_file in recipe_files:
    recipe = get_text(recipe_file)
    pnodes, rnodes = get_semantic_parsing(recipe)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(pnodes, rnodes)

    graph_builder = DotGraphBuilder()
    gv_file = graph_builder.write_gv(pnodes_resolved, rnodes_resolved)

    make_svg(gv_file)

  pass


if __name__ == '__main__':
  main()

