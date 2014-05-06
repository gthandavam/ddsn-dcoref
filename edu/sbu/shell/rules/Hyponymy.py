__author__ = 'gt'
import logging

class Hyponymy:
  """
  This rule is for handling Hyponymous realtions that occur in recipe text.
  For eg: In MacAndCheese Recipes, words pasta and macaroni are used
  interchangeably to mean the same thing; since macaroni is a type of pasta.
  So by capturing such hierarchical relations, we can handle Hyponymy.
  """
  def __init__(self):
    self.logger = logging.getLogger('root')
    self.hyponymous = {}
    self.hyponymous['pasta'] = 'macaroni'

  def find_overlap(self, str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    str1_words = str1.split()
    str2_words = str2.split()

    for word1 in str1_words:
      for word2 in str2_words:
        if word1 in self.hyponymous.keys():
          if self.hyponymous[word1] == word2:
            return True

        if word2 in self.hyponymous.keys():
          if self.hyponymous[word2] == word1:
            return True

    return False


  def find_hypo_match(self, pnodes, rnodes, rnode):
    ret_i = -1
    ret_j = -1

    snum = rnode.sent_num
    pnum = rnode.pred_num

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
            ret_i, ret_j = self.find_hypo_match(pnodes, rnodes, rnodes[i][j][k], i, j)
            if ret_i != -1 and ret_j != -1:
              rnodes[i][j][k].shell_coref.append(((ret_i, ret_j), 'Hyponymy'))
              self.logger.error('Hyponymy Edge')

              # print 'ArgString applied'
              # print rnodes[i][j][k].text + ' pred:' + pnodes[ret_i][ret_j].predicate

    return pnodes, rnodes