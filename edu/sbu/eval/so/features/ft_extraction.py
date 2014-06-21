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

def boolean_feature_encoding(s1p, s2p):
  ret = []
  if( s1p == 0 ):
    if( s2p == 0 ):
      ret.append(0) #decision
      ret.append(0) #decided vs undecided
    else:
      ret.append(0) #decision
      ret.append(1) #decided vs undecided
  else:
    if( s2p == 0):
      ret.append(1)
      ret.append(1)
    else:
      if( s1p > s2p ):
        ret.append(1)
        ret.append(1)
      else:
        ret.append(0)
        ret.append(1)

    pass
  return ret

def get_probability_features(sample):
  from edu.sbu.eval.so.features.statistical_features import getArg1PredPredProb,getArg1PredPredArg1Prob, getArg1Arg2PredPredArg1Prob, getArg1Arg2PredPredProb
  ret = []

  sent1, sent2 = sample.split(sentSeparator)

  sem_group1 = get_sem_grouping(sent1)
  sem_group2 = get_sem_grouping(sent2)

  #CP4
  s1p = getArg1PredPredProb(sem_group1, sem_group2)
  s2p = getArg1PredPredProb(sem_group2, sem_group1)

  ret.extend(boolean_feature_encoding(s1p, s2p))


  #CP3
  s1p = getArg1PredPredArg1Prob(sem_group1, sem_group2)
  s2p = getArg1PredPredArg1Prob(sem_group2, sem_group1)

  ret.extend(boolean_feature_encoding(s1p, s2p))

  #CP2
  s1p = getArg1Arg2PredPredProb(sem_group1, sem_group2)
  s2p = getArg1Arg2PredPredProb(sem_group2, sem_group1)

  ret.extend(boolean_feature_encoding(s1p, s2p))

  #CP1
  s1p = getArg1Arg2PredPredArg1Prob(sem_group1, sem_group2)
  s2p = getArg1Arg2PredPredArg1Prob(sem_group2, sem_group1)

  ret.extend(boolean_feature_encoding(s1p, s2p))

  return ret

  pass

def get_features(sents, vec=1):
  from scipy.sparse import csr_matrix,csc_matrix, hstack

  if vec == 1:
    # vec = CountVectorizer(min_df=1, binary=True, tokenizer=word_tokenize,
    #                     preprocessor=filter_text, ngram_range=(1,2) )
    vec = TfidfVectorizer(min_df=1, tokenizer=word_tokenize,
                          preprocessor=filter_text, ngram_range=(1,2) )

    X   = vec.fit_transform(sents)
  else:
    X   = vec.transform(sents)

  p_features = []
  for sample in sents:
    # print sample
    p_features.append(get_probability_features(sample))

  # To get combination of unigram, bigram and probability features
  X = hstack([X, csc_matrix(p_features)])

  #pprint(str(X))
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