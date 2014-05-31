__author__ = 'gt'


from edu.sbu.shell.Constants import argTypes
import logging

class PNode:


  def __init__(self,  predicate='', pnum=-1, snum=-1, light=False, coref_text='', coref_text_pos=''):
    self.pnum = pnum
    self.snum = snum
    self.predicate = self.cleanse_arg(predicate)
    self.light = light
    self.pIngs = []
    self.cc_edge = []
    self.logger = logging.getLogger('root')
    self.arg_text_for_coref = coref_text
    self.arg_text_POS_for_coref = coref_text_pos
    self.id = ""
    self.arg_text_coref_nouns = None

  def add_arg(self, argType, rnode):
    pass

  def cleanse_arg(self, arg):
    """
    remove undesired punctuation
    """
    if arg is None:
      return None

    arg = arg.lower()

    # arg = unicode(arg)
    # punct = '".()[]'
    # punct_translate_map = dict( (ord(char), None) for char in punct )
    # arg = arg.translate(punct_translate_map)

    return arg

  def getNouns(self):
    if self.arg_text_coref_nouns != None:
      return self.arg_text_coref_nouns
    arr = self.arg_text_POS_for_coref.split()
    res = []
    for a in arr:
      if "minute" in a:
        continue
      arr2 = a.split("/")
      if "NN" in arr2[1]:
        res.append(arr2[0].lower())
    self.arg_text_coref_nouns = res
    return res

