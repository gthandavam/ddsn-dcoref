__author__ = 'polina'

from edu.sbu.stats.corpus.reader2 import RecipeReader2
from collections import Counter
import math
from nltk.stem.porter import *
from edu.sbu.shell.rules.ArgString import ArgString

class RecipeStats2:

  # function_words = ["a","of","in","for","the","this","that","these","those","on"]
  arg = ArgString()
  ignorePOS = arg.ignorePOS
  stemmer = PorterStemmer()
  verbs_score = {}
  verb_args1_score = {}
  verb_args2_score = {}
  sent_window = 4


  def __init__(self, recipe_name):
    self.reader = RecipeReader2(recipe_name)
    self.computeStat()
    pass

  def computeStat(self):
    self.reader.read()
    self.computeVerbArgSentStat()

  # 1. Compute average relative distance for 2 verbs in sentence numbers
  # Average over all recipes
  # For each recipe distance(verb1,verb2) = abs(sent_num(verb1),sent_num(verb2))/sent_cnt
  # 2. Compute average relative distance for verb and output argument in sentence numbers
  def computeVerbArgSentStat(self):
    cnt = {}
    for r in range(len(self.reader.recipe_verbs)):
      recipe = self.reader.recipe_verbs[r]
      arg1_recipe = self.reader.recipe_args1[r]
      arg2_recipe = self.reader.recipe_args2[r]
      verbs = {}
      verb_args1 = {}
      verb_args2 = {}
      sent_num = 0
      for sent in range(len(recipe)):
        for i in range(len(recipe[sent])):
          verb = self.stemmer.stem(recipe[sent][i])
          if verb not in verbs:
            verbs[verb] = {}
            verb_args1[verb] = {}
            verb_args2[verb] = {}
          for k in range(self.sent_window):
            if sent+k>=len(recipe):
              break
            for j in range(len(recipe[sent+k])):
              if k==0 and j<=i:
                continue
              #### Consider other verbs
              verb2 = self.stemmer.stem(recipe[sent+k][j])
              score = None
              if k==0:
                score = float(j-i)/len(recipe[sent])
              else:
                score = float(k)/len(recipe)
              if verb2 not in verbs[verb] or verbs[verb][verb2]<score:
                verbs[verb][verb2] = score
              #### Consider arguments
              if k==0:
                continue
              args1 = arg1_recipe[sent+k]
              for a1 in args1:
                arg1 = self.stemmer.stem(a1)
                if arg1 not in verb_args1[verb] or verb_args1[verb][arg1]<score:
                  verb_args1[verb][arg1] = score
              args2 = arg1_recipe[sent+k]
              for a2 in args2:
                arg2 = self.stemmer.stem(a2)
                if arg2 not in verb_args2[verb] or verb_args2[verb][arg2]<score:
                  verb_args2[verb][arg2] = score
      for verb in verbs:
        if verb not in self.verbs_score:
          self.verbs_score[verb] = {}
          self.verb_args1_score[verb] = {}
          self.verb_args2_score[verb] = {}
        if verb not in cnt:
          cnt[verb] = 1
        else:
          cnt[verb] += 1
        for verb2 in verbs[verb]:
          if verb2 not in self.verbs_score[verb]:
            self.verbs_score[verb][verb2] = verbs[verb][verb2]
          else:
            self.verbs_score[verb][verb2] += verbs[verb][verb2]
        for arg1 in verb_args1[verb]:
          if arg1 not in self.verb_args1_score[verb]:
            self.verb_args1_score[verb][arg1] = verb_args1[verb][arg1]
          else:
            self.verb_args1_score[verb][arg1] += verb_args1[verb][arg1]
        for arg2 in verb_args2[verb]:
          if arg2 not in self.verb_args2_score[verb]:
            self.verb_args2_score[verb][arg2] = verb_args1[verb][arg2]
          else:
            self.verb_args2_score[verb][arg2] += verb_args1[verb][arg2]

    for verb in self.verbs_score:
      for verb2 in self.verbs_score[verb]:
        self.verbs_score[verb][verb2] = float(self.verbs_score[verb][verb2])/cnt[verb]
      for arg1 in self.verb_args1_score[verb]:
        self.verb_args1_score[verb][arg1] = float(self.verb_args1_score[verb][arg1])/cnt[verb]
      for arg2 in self.verb_args2_score[verb]:
        self.verb_args2_score[verb][arg2] = float(self.verb_args2_score[verb][arg2])/cnt[verb]

  def getPredOuputArgProb(self, predicate, input_argument, output_argument):
    if input_argument==None:
      return 0
    # score = math.log(1-self.getTextSim(input_argument.argPOS, output_argument.argPOS)+0.00000001)
    score = math.log(1-self.getTextSimArr(input_argument.argIngs, output_argument.argIngs)+0.00000001)
    if output_argument.arg_type=="arg1":
      score += self.getPredOuputArg1Prob(predicate, input_argument, output_argument)
    elif output_argument.arg_type=="arg2":
      score += self.getPredOuputArg2Prob(predicate, input_argument, output_argument)
    return score

  def getPredOuputArg1Prob(self, predicate, input_argument, output_argument):
    ### Compute probability of edge predicate->arg1
    verb = self.stemmer.stem(predicate.predicate)
    if verb in self.verb_args1_score:
      s=0
      d = {}
      # arr = output_argument.argPOS.split()
      arr = output_argument.argIngs
      for e in arr:
        # arr2 = e.split("/")
        # if "NN" in arr2[1]:
        #   d[self.stemmer.stem(arr2[0])] = 1
        d[self.stemmer.stem(e)] = 1
      if len(d)!=0:
        for arg1 in self.verb_args1_score[verb]:
          if arg1 in d:
            s +=  1-self.verb_args1_score[verb][arg1]
        return math.log(1-float(s)/len(d)+0.00000001)
    return 0

  def getPredOuputArg2Prob(self, predicate, input_argument, output_argument):
    ### Compute probability of edge predicate->arg2
    verb = self.stemmer.stem(predicate.predicate)
    if verb in self.verb_args2_score:
      s=0
      d = {}
      # arr = output_argument.argPOS.split()
      arr = output_argument.argIngs
      for e in arr:
        # arr2 = e.split("/")
        # if arr2[1]=="NN":
        #   d[self.stemmer.stem(arr2[0])] = 1
        d[self.stemmer.stem(e)] = 1
      if len(d)!=0:
        for arg1 in self.verb_args2_score[verb]:
          if arg1 in d:
            s +=  1-self.verb_args2_score[verb][arg1]
        return math.log(1-float(s)/len(d)+0.00000001)
    return 0

  def getPredPredProb(self, predicate, input_argument, predicate2, input_argument2):
    if input_argument==None or input_argument2==None:
      return 0
    # score = math.log(1-self.getTextSim(input_argument.argPOS, input_argument2.argPOS)+0.00000001) + \
  # math.log(1-self.getTextSim(input_argument.argPOS, predicate2.predicate)+0.00000001)
    score = math.log(1-self.getTextSimArr(input_argument.argIngs, input_argument2.argIngs)+0.00000001)
    verb = self.stemmer.stem(predicate.predicate)
    verb2 = self.stemmer.stem(predicate2.predicate)
    if verb in self.verbs_score and verb2 in self.verbs_score[verb]:
      score += math.log(self.verbs_score[verb][verb2]+0.00000001)
    else:
      score += 1
    #   score /=3
    # else:
    #   score /=2
    return score

  def stem(self, word):
    if word=="":
      return "~~IGNORE~~"
    arr = word.split("/")
    if len(arr)==2 and arr[1] in self.ignorePOS:
      return "~~IGNORE~~"
    return self.stemmer.stem(arr[0])

  def getTextSim(self, text1, text2):
    if text1 is None:
      text1 = ''
    if text2 is None:
      text2 = ''
    return self.getTextSimArr(text1.lower().split(" "),text2.lower().split(" "))

  def getTextSimArr(self, text1, text2):
    d1 = Counter(map(lambda k: self.stem(k), text1))
    d2 = Counter(map(lambda k: self.stem(k), text2))
    sum1 = 0
    sum2 = 0
    sum12 = 0
    for e in d1:
      if e=="~~IGNORE~~":
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


