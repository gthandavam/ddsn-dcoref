__author__ = 'gt'

import commands
from nltk.tag.stanford import POSTagger
from nltk import word_tokenize
from nltk.corpus import wordnet as wn

from sklearn.externals import joblib

from string import punctuation as punct
from string import maketrans


class VRVerbs:
  #class that gives
  # 1. the list of verbs per recipe
  # 2. frequency count of the verbs
  # 3. language model on the verb sequence ( after ignoring less frequent verbs )

  def __init__(self):
    #http://www.comp.leeds.ac.uk/amalgam/tagsets/upenn.html
    self.penn_verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
    self.verb_frequency = {}
    self.encoding = 'UTF-8'
    self.bigrams = {}
    #not handling don't won't and so on
    self.apostrophed_verb = {u's': u'is', u're' : u'are',
                             u've' : u'have', u'd' : u'would',
                             u'm' : u'am'
                            }
    self.load_data()


  def update_bigram_model(self, pos_tags):
    prev_verb = 'DUMMY'
    for pos_tag in pos_tags:
      word, part_of_speech = pos_tag

      if part_of_speech in self.penn_verb_tags:
        word_cleansed = self.cleanse_verb(word)
        if word_cleansed is None:
          print 'unable to clean the ' + word
        else:
          word = word_cleansed
        if prev_verb != 'DUMMY':

          if (prev_verb, word) not in self.bigrams.keys():
            self.bigrams[(prev_verb, word)] = 0

          self.bigrams[(prev_verb, word)] += 1
          prev_verb = word

        else:
          prev_verb = word

  def dump_bigrams(self):
    name = 'bigram_verb_frequency.pkl'
    joblib.dump(self.bigrams, name)
    return name


  def dump_verb_frequency(self):
    name = 'verb_frequency.pkl'
    joblib.dump(self.verb_frequency, name)
    return name

  def load_verb_frequency(self):
    return joblib.load('verb_frequency.pkl')

  def get_verb_frequency(self):
    return self.verb_frequency

  def print_verbs(self):
    print self.verb_frequency.keys()

  def print_frequency_count(self):
    for verb in self.verb_frequency.keys():
      line = verb
      for verb_tag in self.penn_verb_tags:
        line+= ','+str(self.verb_frequency[verb][verb_tag])

      print line

  def get_text(self, file_name):
    ret = ''
    with open(file_name) as fp:
      for line in fp:
        ret += line

    return ret

  def get_pos_tags(self, text):
    posTagger = POSTagger('/home/gt/Downloads/'
                          'stanford-postagger-2014-01-04/models/'
                          'english-bidirectional-distsim.tagger',
                          '/home/gt/Downloads/stanford-postagger-2014-01-04'
                          '/stanford-postagger.jar',encoding=self.encoding)

    text = text.lower()

    tokens = word_tokenize(text)
    pos_tags = posTagger.tag(tokens)

    return pos_tags


  def update_verb_frequency(self, pos_tags):
    for pos_tag in pos_tags:
      word, part_of_speech = pos_tag

      if part_of_speech in self.penn_verb_tags:
        word = self.cleanse_verb(word)
        if word not in self.verb_frequency.keys():
          #initialize the map if new verb is found
          self.verb_frequency[word] = {}
          for verb_tag in self.penn_verb_tags:
            self.verb_frequency[word][verb_tag] = 0

        #updating the map based on word, part of speech
        self.verb_frequency[word][part_of_speech] += 1


  def cleanse_verb(self, verb):
    verb = verb.strip()

    #this works for ascii strings not for unicode strings (codecs.open gives unicode)
    #verb = verb.translate(maketrans('',''), punct)

    #this is translate for unicode strings
    #ref: http://stackoverflow.com/questions/11692199/string-translate-with-unicode-data-in-python
    punct_translate_map = dict( (ord(char), None) for char in punct )
    verb = verb.translate(punct_translate_map)

    if verb in self.apostrophed_verb.keys():
      verb = self.apostrophed_verb[verb]

    verb = wn.morphy(verb, wn.VERB)
    return verb



  def load_data(self):
    for file_name in commands.getoutput('ls /home/gt/NewSchematicSummary/recipe-split/*.txt').split('\n'):

      recipe = self.get_text(file_name)
      pos_tags = self.get_pos_tags(recipe)
      self.update_verb_frequency(pos_tags)
      # self.update_bigram_model(pos_tags)