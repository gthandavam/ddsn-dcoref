__author__ = 'gt'
from sklearn.feature_extraction.text import  CountVectorizer

from nltk import word_tokenize
from nltk import PorterStemmer
import re
from edu.sbu.eval.so.data.prepare_data import sentSeparator, labelSeparator

from pprint import pprint

############globals###################
stemmer = PorterStemmer()
punc_rx = re.compile(r'[^#A-Za-z0-9]+', re.DOTALL)
############globals###################

def nltk_filter(sent):
  b1, b2 = sent.split(sentSeparator)

  b1 = b1.rstrip()

  b2 = b2.rstrip()


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

def get_features(sents, vec=1):
  if vec == 1:
    vec = CountVectorizer(min_df=1, binary=True, tokenizer=word_tokenize,
                        preprocessor=filter_text, ngram_range=(1,2) )
    # vec = TfidfVectorizer(min_df=1, tokenizer=word_tokenize,
    #                       preprocessor=filter_text, ngram_range=(1,2) )
    X   = vec.fit_transform(sents)
  else:
    X   = vec.transform(sents)

  #pprint(str(X))
  return vec, X

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