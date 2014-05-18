__author__ = 'gt'

import nltk
import logging
class ArgString:
  def __init__(self):
    self.stopwords = nltk.corpus.stopwords.words('english')
    self.logger = logging.getLogger('root')

    pass


  def is_word(self, word):
    """
    1. Should not contain any punctuation - punctuation retained by RNode for display purposes
    so cleaning it here during comparison
    "carrot , beetroot and tomato".split() gives "," as a word
    so we need to remove punctuation from comparison
    2. checks if the word contains only alphabets
    """
    word = word.lower()
    # word = unicode(word)
    # punct = '".\'()[]'
    # punct_translate_map = dict( (ord(char), None) for char in punct )
    # word = word.translate(punct_translate_map)

    for char in word:
      if char not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', \
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
        return False

    return True

  def find_overlap(self, txt1, txt2):
    """
    find overlap in content words
    """
    for word1 in txt1.split():
      for word2 in txt2.split():
        if word1 in self.stopwords or word2 in self.stopwords:
          continue
        if not self.is_word(word1) or not self.is_word(word2):
          continue
        if word1 == word2:
          return True

    return False

  def find_arg_string_match(self, pnodes, rnodes, rnode, snum, pnum):
    ret_i = -1
    ret_j = -1

    for i in xrange(snum, -1, -1):
      for j in xrange(len(pnodes[i]) - 1, -1, -1):
        if i == snum and j >= pnum:
          continue

        if not pnodes[i][j] is None:
          for k in xrange(1,3):
            if not rnodes[i][j][k].is_null:

              if self.find_overlap(rnodes[i][j][k].text, rnode.text):
                self.logger.warn(rnodes[i][j][k].text + ' referring arg:' + rnode.text)
                return i,j
          pass
        else:
          self.logger.warn('None predicate found!!!')

    return ret_i, ret_j



  def run(self, pnodes, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        if i == 0 and j == 0:
          continue
        for k in xrange(1,3):#applying arg string match for arg1 and arg2
          #applies only for non-null instantiations of args
          if not rnodes[i][j][k].is_null:
            ret_i, ret_j = self.find_arg_string_match(pnodes, rnodes, rnodes[i][j][k], i, j)
            if ret_i != -1 and ret_j != -1:
              rnodes[i][j][k].shell_coref.append(((ret_i, ret_j), 'ArgString'))

              # print 'ArgString applied'
              # print rnodes[i][j][k].text + ' pred:' + pnodes[ret_i][ret_j].predicate

    return pnodes, rnodes