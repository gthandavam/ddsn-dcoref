__author__ = 'polina'

from collections import Counter
import math
from nltk.stem.porter import *

class RecipeStats2:

  function_words = ["a","of","in","for","the","this","that","these","those","on"]
  stemmer = PorterStemmer()

  def __init__(self, recipe_name):
    # self.reader = RecipeReader2(recipe_name)
    pass

  def getPredOuputArgProb(self, predicate, input_argument, output_argument):
    if input_argument==None:
      return 0
    return self.getTextSim(input_argument.text, output_argument.text)

  def getPredPredProb(self, predicate, input_argument, predicate2):
    if input_argument==None:
      return 0
    return self.getTextSim(input_argument.text, predicate2.predicate)

  def getTextSim(self, text1, text2):
    d1 = Counter(map(lambda k: self.stemmer.stem(k), text1.lower().split(" ")))
    d2 = Counter(map(lambda k: self.stemmer.stem(k), text2.lower().split(" ")))
    sum1 = 0
    sum2 = 0
    sum12 = 0
    for e in d1:
      if e in self.function_words:
        continue
      sum1 += d1[e]*d1[e]
      if e not in d2:
        continue
      sum12 += d1[e]*d2[e]
    for e in d2:
      sum2 += d2[e]*d2[e]

    if sum12==0:
      return 0
    return sum12/math.sqrt(sum1*sum2)


