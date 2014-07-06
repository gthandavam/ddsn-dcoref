__author__ = 'gt'
from sklearn.feature_extraction.text import  CountVectorizer, TfidfVectorizer, TfidfTransformer

from nltk import word_tokenize
from nltk import PorterStemmer
import re
from edu.sbu.eval.so.data.prepare_data import sentSeparator, labelSeparator, predSeparator, arg1POSSeparator, arg1Separator, arg2Separator

from pprint import pprint

############globals###################
stemmer = PorterStemmer()
punc_rx = re.compile(r'[^#A-Za-z0-9]+', re.DOTALL)
############globals###################

def get_sem_grouping(sentence):
  ret = {}
  pred, sentence = sentence.split(predSeparator)
  arg1, sentence = sentence.split(arg1Separator)
  arg1POS, sentence = sentence.split(arg1POSSeparator)
  arg2, arg2POS = sentence.split(arg2Separator)

  ret['pred'] = pred
  ret['arg1'] = arg1
  ret['arg1POS'] = arg1POS
  ret['arg2'] = arg2
  ret['arg2POS'] = arg2POS

  return ret

def nltk_filter(sent):
  b1, b2 = sent.split(sentSeparator)

  b1 = b1.rstrip()
  b1 = get_sem_grouping(b1)

  b1 = b1['pred'] + ' ' + b1['arg1'] + ' ' + b1['arg2']

  b2 = b2.rstrip()
  b2 = get_sem_grouping(b2)
  b2 = b2['pred'] + ' ' + b2['arg1'] + ' ' + b2['arg2']

  b1            = b1.lower()
  tokens        = word_tokenize(b1)
  filtered_sent = ' '
  for token in tokens:
    #try without separating as 1 and 2
    # filtered_sent += stemmer.stem(token) + ' '
    filtered_sent += '1' + stemmer.stem(token) + ' '
  # for pos_t in pos_tags:
  #   if pos_t[1] in filterList:
  #     #filtered_sent += stemmer.stem(pos_t[0]) + ' '
  #     filtered_sent += '1' + stemmer.stem(pos_t[0]) + ' '

#note: 1 concat stemmer(word) == stemmer(1 concat word)

  b2            = b2.lower()
  tokens        = word_tokenize(b2)


  # for pos_t in pos_tags:
  #   if pos_t[1] in filterList:
  #     #filtered_sent += stemmer.stem(pos_t[0]) + ' '
  #     filtered_sent += '2' + stemmer.stem(pos_t[0]) + ' '

  for token in tokens:
    # filtered_sent += stemmer.stem(token) + ' '
    filtered_sent += '2' + stemmer.stem(token) + ' '
  return filtered_sent


def filter_text(sent):
  # return stanford_corenlp_filter(sent)
  sent = re.sub(punc_rx, ' ', sent)
  return nltk_filter(sent)
  # sents = sent.split(blockSeparator)
  # sent = sents[0] + ' ' + sents[1]
  # return sent


def get_probability_features(sample, stats_obj):

  sent1, sent2 = sample.split(sentSeparator)

  sem_group1 = get_sem_grouping(sent1)
  sem_group2 = get_sem_grouping(sent2)

  return stats_obj.get_prob_features(sem_group1, sem_group2)


def get_features(sents, vec=1, recipeName='MacAndCheese', cp0=True, cp1=True, cp2=True, cp3=True, cp4=True):
  from scipy.sparse import csr_matrix,csc_matrix, hstack
  from sklearn import preprocessing
  from edu.sbu.eval.so.features.statistical_features import StatFeatures

  if vec == 1:
    # vec = CountVectorizer(min_df=1, binary=True, tokenizer=word_tokenize,
    #                     preprocessor=filter_text, ngram_range=(1,2) )
    vec = TfidfTransformer( min_df=1, tokenizer=word_tokenize,
                          preprocessor=filter_text, ngram_range=(1,2) )

    X   = vec.fit_transform(sents)
  else:
    X   = vec.transform(sents)

  # X = preprocessing.scale(X, with_mean=False)

  skip_stats = False
  if(not cp0 and  not cp1 and not cp2 and not cp3 and not cp4):
    skip_stats = True

  if not skip_stats:
    stats_obj = StatFeatures(recipeName, cp0, cp1, cp2, cp3, cp4)
    p_features = []
    for sample in sents:
      # print sample
      p_features.append(get_probability_features(sample, stats_obj))

    # To get combination of unigram, bigram and probability features
    X = hstack([X, csc_matrix(p_features)])

  #   False -> not centering on mean; only option for sparse matrices
  #   True -> center on variance
  #   False -> no copy of data
  X = preprocessing.scale(X, 0, False, True, False)

  # #pprint(str(X))
  return vec, X
  # return vec, csc_matrix(p_features)

def test_features():
  sents = [
    'preheat oven to 350 degrees F#SENTENCE#bring a large pot of lightly salted water to a boil#LABEL#+',
'preheat oven to 350 degrees F#SENTENCE#cook elbow macaroni in the boiling water#LABEL#+',
'preheat oven to 350 degrees F#SENTENCE#spread half the macaroni into a 9x13-inch casserole dish#LABEL#+',
'top NULL with half the tomatoes and half the Cheddar cheese#SENTENCE#preheat oven to 350 degrees F#LABEL#-',
'pour milk over entire casserole#SENTENCE#preheat oven to 350 degrees F#LABEL#-',
'preheat oven to 350 degrees F#SENTENCE#sprinkle NULL with crushed crackers#LABEL#+',
'preheat oven to 350 degrees F#SENTENCE#bake NULL in the preheated oven#LABEL#+',
'are NULL about 30 minutes#SENTENCE#preheat oven to 350 degrees F#LABEL#-',
'bring a large pot of lightly salted water to a boil#SENTENCE#cook elbow macaroni in the boiling water#LABEL#+',
'bring a large pot of lightly salted water to a boil#SENTENCE#spread half the macaroni into a 9x13-inch casserole dish#LABEL#+',
'top NULL with half the tomatoes and half the Cheddar cheese#SENTENCE#bring a large pot of lightly salted water to a boil#LABEL#-',
'pour milk over entire casserole#SENTENCE#bring a large pot of lightly salted water to a boil#LABEL#-,',
  ]
  vec, X = get_features(sents)

  print vec.get_params()
  print vec.get_feature_names()
  pprint(X)

def main():
  test_features()

if __name__ == '__main__':
  main()
  print '#############'