__author__ = 'gt'

import nltk
import logging

class RNode:

  def __init__(self):
    self.arg_type = ''
    self.raw_text = ''
    self.text = ''
    self.sent_num = -1 #sentence number
    self.pred_num = -1 #predicate number in the document : because it is needed to generate graph
    self.shell_coref = []#tracks stepwise reference predicate num
    self.to_delete = False
    self.is_null = False
    self.logger = logging.getLogger(__name__)
    logging.basicConfig()
    pass

  def __init__(self, text, pnum, snum, arg_type, is_null=False):
    self.raw_text = text
    self.text = self.cleanse_arg(text)
    self.arg_type = arg_type
    self.sent_num = snum
    self.pred_num = pnum
    self.shell_coref = []
    self.to_delete = False
    self.is_null = is_null
    self.logger = logging.getLogger(__name__)
    logging.basicConfig()
    pass

  def add_shell_coref(self, stepnum, pnum):
    #not tracking the step num - assuming one assignment in one step
    self.shell_coref.append(pnum)

  def cleanse_arg(self, arg):
    """
    remove undesired punctuation and stopwords
    """
    if arg is None:
      return None

    arg = arg.lower()

    arg = unicode(arg)
    punct = '".\'()[]'
    punct_translate_map = dict( (ord(char), None) for char in punct )
    arg = arg.translate(punct_translate_map)

    ret = []
    for word in arg.split():
      if self.is_stopword(word):
        continue
      else:
        ret.append(word)

    if len(ret) == 0:
      return arg

    return ' '.join(ret)

  def is_stopword(self, arg):
    if arg.lower() in ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'what', 'which', 'who', 'whom', 'a', 'an', 'the', 'and', 'but', 'if','because', 'when', 'where', 'why', 'how', 'all', 'any', 'both']:
        return True
    else:
        return False


