__author__ = 'gt'

from edu.sbu.stats.corpus.reader import RecipeReader


# I think nltk has incorrectly named this package as collocations
#it should ideally have had a name related to LanguageModel
#For eg: strong tea is a collocation : it has got very little to do with
# language model n-grams
import nltk.collocations as coll
from nltk.probability import FreqDist
from nltk.probability import MLEProbDist
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
import logging

class RecipeStats:

  def __init__(self, recipe_name):
    #TODO: Smoothing on the language models constructed
    self.reader = RecipeReader(recipe_name)
    self.reader.read()
    self.words_bigram_prob = None
    self.verbs_bigram_prob = None
    self.verb_unigram_prob = None
    self.word_unigram_prob = None
    self.null_args_cond    = None
    self.v_prev_v_phrase_cond = None
    self.v_phrase_cond = None
    self.phrase_cond = None
    self.logger = logging.getLogger('root')
    ####Recipe frequencies calculated here
    pass

  #TODO: I expect nltk to handle end of sentence marker cases - check!!!
  #The current usage doesnt handle this case - TODO:Clean this up
  def calc_words_bigram_prob(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.words)
    self.words_bigram_prob = dict(finder.score_ngrams( bgm.likelihood_ratio ))
    pass

  def calc_verbs_bigram_prob(self):
    bgm    = coll.BigramAssocMeasures()
    finder = coll.BigramCollocationFinder.from_words(self.reader.verbs)
    self.verbs_bigram_prob = dict(finder.score_ngrams( bgm.likelihood_ratio ))
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

    #I guess everything is handled by the nltk
    #TODO: smooth the probability here
    #TODO: log probability

    #Need to check this
    #TODO: remove punctuation in phrase ?

    #Question: TODO: Check this
    #P(b1, b2, b3) = P(b3|b2) * P(b2|b1) * P(b1)
    #                or P(b1|b2) * P(b2|b3) * P(b3) ?
    #I guess they are not one and the same - verify

    for i in xrange(len(words) - 1):

      pass

    pass


  def build_prob_dist(self):
    self.calc_words_unigram()
    self.calc_verbs_unigram()
    self.calc_words_bigram_prob()
    self.calc_verbs_bigram_prob()
    self.calc_null_args_prob()
    self.calc_conditional_prob()
    pass

  def calc_conditional_prob(self):
    """
    nltk conditional prob notation:
    cpd['condition'].prob(a) is P(a | condition)
    """

    prev_v = 'PREV'
    v_prev_phrase_cfd = ConditionalFreqDist()
    v_phrase_cfd = ConditionalFreqDist()
    phrase_cfd = ConditionalFreqDist()
    for sem_group in self.reader.sem_groups:
      if(sem_group['pred'] is None):
        self.logger.error("pred is none!!!")
        continue

      if(sem_group['arg1'] is None):
        arg1 = 'NULL'
      else:
        arg1 = sem_group['arg1']

      if(sem_group['arg2'] is None):
        arg2 = 'NULL'
      else:
        arg2 = sem_group['arg2']

      v_prev_phrase_cfd[(arg1, sem_group['pred'], prev_v)].inc('arg1')
      v_prev_phrase_cfd[(arg2, sem_group['pred'], prev_v)].inc('arg2')
      v_phrase_cfd[(arg1, sem_group['pred'])].inc('arg1')
      v_phrase_cfd[(arg2, sem_group['pred'])].inc('arg2')
      phrase_cfd[arg1].inc('arg1')
      phrase_cfd[arg2].inc('arg2')

      prev_v = sem_group['pred']

      pass

    self.v_prev_v_phrase_cond = ConditionalProbDist(v_prev_phrase_cfd, MLEProbDist, 2)

    self.v_phrase_cond = ConditionalProbDist(v_phrase_cfd, MLEProbDist, 2)

    self.phrase_cond = ConditionalProbDist(phrase_cfd, MLEProbDist, 2)


    pass

  def calc_null_args_prob(self):
    null_args_cfd = ConditionalFreqDist()
    for sem_group in self.reader.sem_groups:
      if(sem_group['pred'] is None):
        self.logger.error("pred is none!!!")

      if sem_group['arg1'] is None and sem_group['arg2'] is None:
        null_args_cfd['arg1arg2null'].inc(sem_group['pred'])

      #cases when both arg1 and arg2 are null are also included
      #in the below conditional freq counts
      if sem_group['arg1'] is None:
        null_args_cfd['arg1null'].inc(sem_group['pred'])

      if sem_group['arg2'] is None:
        null_args_cfd['arg2null'].inc(sem_group['pred'])

      self.null_args_cond = ConditionalProbDist(null_args_cfd, MLEProbDist, 3)

      pass
    pass

  def save_all(self):

    # print json.dumps(self.null_args_cond)
    pass

  pass