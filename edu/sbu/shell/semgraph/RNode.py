__author__ = 'gt'

import nltk

class RNode:

  def __init__(self):
    self.arg_type = ''
    self.text = ''
    self.sent_num = -1 #sentence number
    self.pred_num = -1 #predicate number in the document : because it is needed to generate graph
    self.shell_coref = []#tracks stepwise reference predicate num
    self.to_delete = False
    pass

  def __init__(self, text, pnum, snum, arg_type):
    self.text = self.cleanse_arg(text)
    self.arg_type = arg_type
    self.sent_num = snum
    self.pred_num = pnum
    self.shell_coref = []
    self.to_delete = False
    pass

  def add_shell_coref(self, stepnum, pnum):
    #not tracking the step num - assuming one assignment in one step
    self.shell_coref.append(pnum)

  def cleanse_arg(self, arg):
    ret = []
    for word in arg.split():
      if self.is_stopword(word):
        pass
      else:
        ret.append(word)
    return ' '.join(ret)

  def is_stopword(self, string):
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False


