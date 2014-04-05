__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes


class PNode:

  def __init__(self):
    self.pnum = -1
    self.snum = -1
    self.predicate = ''
    self.light = False
    pass

  def __init__(self,  predicate, pnum, snum, light):
    self.pnum = pnum
    self.snum = snum
    self.predicate = self.cleanse_arg(predicate)
    self.light = light

  def add_arg(self, argType, rnode):
    pass

  def cleanse_arg(self, arg):
    """
    remove undesired punctuation
    """
    if arg is None:
      return None

    arg = arg.lower()

    arg = unicode(arg)
    punct = '".()[]'
    punct_translate_map = dict( (ord(char), None) for char in punct )
    arg = arg.translate(punct_translate_map)

    return arg
