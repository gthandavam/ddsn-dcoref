__author__ = 'gt'

import nltk
import logging

class RNode:

  def __init__(self, text='', pnum=-1, snum=-1, arg_type='', is_null=False, arg_prob = -1.0):
    self.raw_text = text
    self.text = self.cleanse_arg(text)
    self.arg_type = arg_type
    self.sent_num = snum
    self.pred_num = pnum
    self.shell_coref = []
    self.to_delete = False
    self.is_null = is_null
    self.argIngs = []
    self.arg_prob = arg_prob
    self.logger = logging.getLogger('root')

    pass

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