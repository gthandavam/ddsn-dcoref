__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes
import logging

class PNode:


  def __init__(self,  predicate='', pnum=-1, snum=-1, light=False):
    self.pnum = pnum
    self.snum = snum
    self.predicate = self.cleanse_arg(predicate)
    self.light = light
    self.pIngs = []
    self.cc_edge = []
    self.logger = logging.getLogger('root')

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
