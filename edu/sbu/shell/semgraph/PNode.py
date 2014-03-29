__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes


class PNode:

  def __init__(self):
    self.pnum = -1
    self.snum = -1
    self.predicate = ''
    self.args = [[], [], []]
    self.to_delete = False
    pass

  def __init__(self, pnum, snum, predicate):
    self.pnum = pnum
    self.snum = snum
    self.predicate = predicate
    self.args = [[], [], []] #arg0 arg1 and arg2 stored here
    self.to_delete = False

  def add_arg(self, argType, rnode):
    pass

