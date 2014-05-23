__author__ = 'gt'

from edu.sbu.stats.corpus.reader import RecipeReader
import nltk.collocations as coll
class RecipeHMM:

  def __init__(self, recipe_name):
    self.reader = RecipeReader(recipe_name)
    self.reader.read()
    self.words_bigram = None
    self.verbs_bigram = None
    ####Recipe frequencies calculated here
    pass

  def calc_words_bigram(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.words)
    self.words_bigram = finder.score_ngrams( bgm.likelihood_ratio )
    pass

  def calc_verbs_bigram(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.verbs)
    self.verbs_bigram = finder.score_ngrams( bgm.likelihood_ratio )
    pass

  def calc_verbs_unigram(self):
    pass

  def calc_phrase_probability(self, arg_type):
    pass

  def conditional_prob(self, arg_type):
    pass


  def save_all(self):
    pass

  pass

