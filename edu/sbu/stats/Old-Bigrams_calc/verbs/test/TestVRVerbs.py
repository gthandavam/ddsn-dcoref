__author__ = 'gt'

from VR.verbs import VRVerbs
from sklearn.externals import joblib
import codecs
from nltk.corpus import wordnet as wn

def main():
  obj = VRVerbs.VRVerbs()
  # obj.print_frequency_count()
  obj.dump_bigrams()
  obj.print_verbs()
  # obj.dump_verb_frequency()
  pass

def bigram_to_csv():
  bigrams = joblib.load('bigram_verb_frequency.pkl')
  f = codecs.open('bigram_frequency.csv','w','UTF-8')
  for key in bigrams.keys():
    line = key[0]
    line += ',' + key[1]
    line += ','
    line += str(bigrams[key])
    line += '\n'
    f.write(line)
    f.flush()

  f.close()

def nounify(verb_word):
  """ Transform a verb to the closest noun: die -> death """
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

  # Build the result in the form of a list containing tuples (word, probability)
  result = [(w, float(words.count(w))/len_words) for w in set(words)]
  result.sort(key=lambda w: -w[1])

  # return all the possibilities sorted by probability
  return result

def verbify(noun_word):
  """ Transform a noun to the closest verb: mixture -> mix """
  noun_synsets = wn.synsets(noun_word, pos="n")

  # Word not found
  if not noun_synsets:
    return []

  # Get all noun lemmas of the word
  noun_lemmas = [l for s in noun_synsets \
                 for l in s.lemmas if s.name.split('.')[1] == 'n']

  # Get related forms
  derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                  for l in    noun_lemmas]

  # filter only the verbs
  related_verb_lemmas = [l for drf in derivationally_related_forms \
                         for l in drf[1] if l.synset.name.split('.')[1] == 'v']

  # Extract the words from the lemmas
  words = [l.name for l in related_verb_lemmas]
  len_words = len(words)

  # Build the result in the form of a list containing tuples (word, probability)
  result = [(w, float(words.count(w))/len_words) for w in set(words)]
  result.sort(key=lambda w: -w[1])

  # return all the possibilities sorted by probability
  return result


if __name__ == '__main__':
  # main()
  # bigram_to_csv()
  print nounify('eating')
  print verbify('death')
  print verbify('mixture')
  print verbify('boiling')