__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes


class PNode:

  def __init__(self):
    self.pnum = -1
    self.snum = -1
    self.predicate = ''
    self.args = {}
    for argType in argTypes:
      self.args[argType] = []
    pass

  def __init__(self, pnum, snum, predicate):
    self.pnum = pnum
    self.snum = snum
    self.predicate = predicate
    self.args = {}
    for argType in argTypes:
      self.args[argType] = []


  def add_arg(self, argType, rnode):
    self.args[argType] = rnode

