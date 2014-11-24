__author__ = 'gt'

import nltk
import logging

class RNode:

  def __init__(self, text='', pnum=-1, snum=-1, arg_type='' ,argPOS='', is_null=False, span_start = -1, span_end=-1):
    #This line was added for swirl formulation
    if not text is None:
      text = text.replace('V#', '')
    self.raw_text = text
    self.text = text #self.cleanse_arg(text)
    self.arg_type = arg_type
    self.sent_num = snum
    self.pred_num = pnum
    self.shell_coref = []
    self.to_delete = False
    self.is_null = is_null
    self.argIngs = set()
    self.argPOS = argPOS
    self.logger = logging.getLogger('root')
    self.id = ""
    self.arg_text_nouns = None
    self.span_start = span_start
    self.span_end = span_end

    pass

  def cleanse_arg(self, arg):
    """
    remove undesired punctuation and stopwords
    """
    if arg is None:
      return None

    arg = arg.lower()

    # arg = unicode(arg)
    # punct = '".\'()[]'
    # punct_translate_map = dict( (char, None) for char in punct )
    # arg = arg.translate(punct_translate_map)

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


  def getNouns(self):
    if self.arg_text_nouns != None:
      return self.arg_text_nouns

    arr = self.argPOS.split()
    res = set()
    for a in arr:
      if "minute" in a:
        continue
      if a.lower() == 'null':
        continue
      arr2 = a.split("/")

      if not(len(arr2) > 1):
        continue
      if "NN" in arr2[1]:
        res.add(arr2[0].lower())
        # if self.arg_type=="arg2":
        #   break # take only the first noun -- why ?
    self.arg_text_nouns = list(res)
    return list(res)
