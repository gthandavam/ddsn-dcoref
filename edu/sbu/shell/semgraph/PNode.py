__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes


class PNode:

  def __init__(self):
    self.pnum = -1
    self.snum = -1
    self.predicate = ''
    self.args = [[], [], []]
    self.light = False
    pass

  def __init__(self,  predicate, pnum, snum, light):
    self.pnum = pnum
    self.snum = snum
    self.predicate = predicate
    self.args = [[], [], []] #arg0 arg1 and arg2 stored here
    self.light = light

  def add_arg(self, argType, rnode):
    pass

