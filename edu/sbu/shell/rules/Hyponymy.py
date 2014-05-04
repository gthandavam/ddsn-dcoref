__author__ = 'gt'
import logging

class Hyponymy:
  """
  This rule is for handling Hyponymous realtions that occur in recipe text.
  For eg: In MacAndCheese Recipes, words pasta and macaroni are used
  interchangeably to mean the same thing; since macaroni is a type of pasta.
  So by capturing such hierarchical relations, we can handle Hyponymy.
  """
  def __init__(self):
    self.logger = logging.getLogger('root')

  def run(self, pnodes, rnodes):
    return pnodes, rnodes