__author__ = 'gt'

from nltk.corpus import wordnet as wn


class DerivationallyRelated:
  def __init__(self):
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

    # return noun with max probability
    return result[0][0]


  def run(self, pnodes, rnodes):

    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        for k in xrange(1,3): #for arg1 and arg2
          if not rnodes[i][j][k].is_null:
            if self.nounify(pnodes[i][j].predicate) in rnodes[i][j][k].text.split():
              rnodes[i][j][k].shell_coref.append((i,j))
              print 'Derivationally Related applied'
              print rnodes[i][j][k].raw_text + ' pred: ' + pnodes[i][j].predicate

    return pnodes, rnodes