__author__ = 'gt'

from edu.sbu.stats.corpus.reader import RecipeReader


# I think nltk has incorrectly named this package as collocations
#it should ideally have had a name related to LanguageModel
#For eg: strong tea is a collocation : it has got nothing to do with
# co-location
import nltk.collocations as coll
from nltk.probability import FreqDist
from nltk.probability import MLEProbDist

class RecipeHMM:

  def __init__(self, recipe_name):
    #TODO: Smoothing on the language models constructed
    self.reader = RecipeReader(recipe_name)
    self.reader.read()
    self.words_bigram_prob = None
    self.verbs_bigram_prob = None
    self.verb_unigram_prob = None
    self.word_unigram_prob = None
    ####Recipe frequencies calculated here
    pass

  #TODO: I expect nltk to handle end of sentence marker cases - check!!!
  def calc_words_bigram_prob(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.words)
    self.words_bigram_prob = finder.score_ngrams( bgm.likelihood_ratio )
    pass

  def calc_verbs_bigram_prob(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.verbs)
    self.verbs_bigram_prob = finder.score_ngrams( bgm.likelihood_ratio )
    pass

  def calc_verbs_unigram(self):
    freq_dist = FreqDist()
    for verb in self.reader.verbs:
      freq_dist.inc(verb)

    self.verb_unigram_prob = MLEProbDist(freq_dist)
    pass

  def calc_words_unigram(self):
    freq_dist = FreqDist()
    for word in self.reader.words:
      freq_dist.inc(word)

    self.word_unigram_prob = MLEProbDist(freq_dist)
    pass

  def calc_phrase_probability(self, phrase):
    phrase = phrase.lower()
    words = phrase.split()

    #TODO: smooth the probability here
    #TODO: log probability
    #TODO: remove punctuation in phrase ?

    #Question: TODO: Check this
    #P(b1, b2, b3) = P(b3|b2) * P(b2|b1) * P(b1)
    #                or P(b1|b2) * P(b2|b3) * P(b3) ?
    #I guess they are not one and the same - verify

    #TODO: How to access the bigram probability
    for i in xrange(len(words) - 1):



      pass

    pass

  def conditional_prob(self, arg_type):
    pass

  def build_prob_dist(self):
    self.calc_words_unigram()
    self.calc_verbs_unigram()
    self.calc_words_bigram_prob()
    self.calc_verbs_bigram_prob()
    pass

  def save_all(self):
    pass

  pass