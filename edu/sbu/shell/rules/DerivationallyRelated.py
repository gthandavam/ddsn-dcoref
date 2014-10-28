__author__ = 'gt'

from nltk.corpus import wordnet as wn
import logging

class DerivationallyRelated:
  def __init__(self):
    self.logger = logging.getLogger('root')

    pass

  def nounify(self, verb_word):
    """ Transform a verb to the closest noun: mix -> mixture """
    verb_synsets = wn.synsets(verb_word, pos="v")

    # Word not found
    if not verb_synsets:
      return []

    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets \
                   for l in s.lemmas if s.name.split('.')[1] == 'v']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]

    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset.name.split('.')[1] == 'n']

    # Extract the words from the lemmas
    words = [l.name for l in related_noun_lemmas]
    len_words = len(words)

    if len_words == 0:
      return verb_word

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    #TODO: Should we return top N instead of the top most ?
    # return noun with max probability
    return result[0][0]

  def find_derivationally_related(self, pnodes, snum, pnum, rnode):
    ret_i = -1
    ret_j = -1

    for i in xrange(snum, -1, -1):
      for j in xrange(len(pnodes[i]) - 1, -1, -1):
        if i == snum and j >= pnum:
          continue

        if not pnodes[i][j] is None:
          if self.nounify(pnodes[i][j].predicate) in rnode.text.split():
            # print 'Derivationally related applied'
            # print 'pred: ' + pnodes[i][j].predicate
            # print 'Nominalize: ' + self.nounify(pnodes[i][j].predicate)
            # print rnode.text
            return i,j
          from edu.sbu.shell.semgraph.DCorefGraphBuilder import DCorefGraphBuilder
          tmp = DCorefGraphBuilder()
          for word in rnode.text.split():
            verb, verbified = tmp.verbify(word)
            if verbified and (verb == pnodes[i][j].predicate):
              # print 'here'
              # print rnode.text
              # print pnodes[i][j].predicate
              return i,j

          pass
        else:
          self.logger.warn('None predicate found!!!')

    return ret_i, ret_j



  def run(self, pnodes, rnodes):

    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        if i==0 and j==0:
          continue
        for k in xrange(1,3): #for arg1 and arg2
          if not rnodes[i][j][k].is_null:
            ret_i, ret_j = self.find_derivationally_related(pnodes, i, j, rnodes[i][j][k])
            if(not (ret_i == - 1 and ret_j == -1) ):
              rnodes[i][j][k].shell_coref.append(((ret_i,ret_j), 'DerivationallyRelated'))

              pnodes[i][j].arg_text_for_coref += ' ' + pnodes[ret_i][ret_j].arg_text_for_coref
              pnodes[i][j].arg_text_POS_for_coref += ' ' + pnodes[ret_i][ret_j].arg_text_POS_for_coref

              ##Updating the lexical chain in RNode as well, so that it will be helpful in stat collection
              rnodes[i][j][k].argPOS += ' ' + pnodes[ret_i][ret_j].arg_text_POS_for_coref
              # print 'Derivationally Related applied'
              # print rnodes[i][j][k].raw_text + ' pred: ' + pnodes[i][j].predicate

    return pnodes, rnodes