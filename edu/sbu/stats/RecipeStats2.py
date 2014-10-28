__author__ = 'polina'

from edu.sbu.stats.corpus.reader2 import RecipeReader2
from collections import Counter
import math
from nltk.stem.porter import *
from edu.sbu.shell.semgraph.RNode import RNode
from edu.sbu.shell.semgraph.PNode import PNode

class RecipeStats2:

  def __init__(self):
    # function_words = ["a","of","in","for","the","this","that","these","those","on"]

    self.ignorePOS = ['DT', 'JJ', 'RB', 'CC', 'TO', 'IN', 'CD', 'PDT']
    self.stemmer = PorterStemmer()
    self.verbs_score = {}
    self.verb_args1_score = {}
    self.verb_args2_score = {}
    self.args1_args_score = {}
    self.args1_args2_args_score = {}
    self.args_verb_score = {}
    self.args1_args2_verb_args_score = {}
    self.args1_verb_args_score = {}
    self.args1_args2_verb_verb_score = {}
    self.args1_args2_verb_verb_args1_score = {}
    self.args1_verb_verb_score = {}
    self.args1_verb_verb_args1_score = {}
    self.sent_window = 3

    pass

  def log(self, val):
    if val==0:
      return -100
    else:
      return math.log(val)

  def computeStat(self, recipe_name):
    self.reader = RecipeReader2(recipe_name)
    self.reader.read()
    self.computeVerbArgSentStat()
    print 'here'

  # 1. Compute average relative distance for 2 verbs in sentence numbers
  # Average over all recipes
  # For each recipe distance(verb1,verb2) = abs(sent_num(verb1),sent_num(verb2))/sent_cnt
  # 2. Compute average relative distance for verb and output argument in sentence numbers
  def computeVerbArgSentStat(self):
    cnt = {}
    cnt_arg1 = {}
    cnt_arg2 = {}
    cnt_arg1_arg2_verb = {}
    cnt_arg1_verb = {}
    for r in range(len(self.reader.recipe_verbs)):
      recipe = self.reader.recipe_verbs[r]
      arg1_recipe = self.reader.recipe_args1[r]
      arg2_recipe = self.reader.recipe_args2[r]
      verbs = {}
      verb_args1 = {}
      verb_args2 = {}
      args1_args1 = {}
      args1_args2_verb_verb_score = {}
      args1_verb_verb_score = {}
      args1_args2_verb_args_score = {}
      args1_verb_args_score = {}
      args1_args2_verb_verb_args1_score = {}
      args1_verb_verb_args1_score = {}
      sent_num = 0
      for sent in range(len(recipe)):
        for i in range(len(recipe[sent])):
          verb = self.stemmer.stem(recipe[sent][i])
          args1 = arg1_recipe[sent][i]
          args2 = arg2_recipe[sent][i]
          if verb not in verbs:
            verbs[verb] = {}
            verb_args1[verb] = {}
            verb_args2[verb] = {}
          for a1 in args1:
            arg1 = self.stemmer.stem(a1)
            if arg1 not in args1_args2_verb_verb_score:
              args1_args2_verb_verb_score[arg1] = {}
            if arg1 not in args1_args2_verb_args_score:
              args1_args2_verb_args_score[arg1] = {}
            if arg1 not in args1_args2_verb_verb_args1_score:
              args1_args2_verb_verb_args1_score[arg1] = {}
            if arg1 not in args1_verb_verb_score:
              args1_verb_verb_score[arg1] = {}
            if arg1 not in args1_verb_args_score:
              args1_verb_args_score[arg1] = {}
            if arg1 not in args1_verb_verb_args1_score:
              args1_verb_verb_args1_score[arg1] = {}
            if verb not in args1_verb_verb_score[arg1]:
              args1_verb_verb_score[arg1][verb] = {}
            if verb not in args1_verb_args_score[arg1]:
              args1_verb_args_score[arg1][verb] = {}
            if verb not in args1_verb_verb_args1_score[arg1]:
              args1_verb_verb_args1_score[arg1][verb] = {}
            for a2 in args2:
              arg2 = self.stemmer.stem(a2)
              if arg2 not in args1_args2_verb_verb_score[arg1]:
                args1_args2_verb_verb_score[arg1][arg2] = {}
              if arg2 not in args1_args2_verb_args_score[arg1]:
                args1_args2_verb_args_score[arg1][arg2] = {}
              if arg2 not in args1_args2_verb_verb_args1_score[arg1]:
                args1_args2_verb_verb_args1_score[arg1][arg2] = {}
              if verb not in args1_args2_verb_verb_score[arg1][arg2]:
                args1_args2_verb_verb_score[arg1][arg2][verb] = {}
              if verb not in args1_args2_verb_args_score[arg1][arg2]:
                args1_args2_verb_args_score[arg1][arg2][verb] = {}
              if verb not in args1_args2_verb_verb_args1_score[arg1][arg2]:
                args1_args2_verb_verb_args1_score[arg1][arg2][verb] = {}
          for k in range(self.sent_window):
            if sent+k>=len(recipe):
              break
            for j in range(len(recipe[sent+k])):
              if k==0 and j<=i:
                continue
              #### Consider other verbs
              verb2 = self.stemmer.stem(recipe[sent+k][j])
              verbs[verb][verb2] = 1
              verb2_args1 = arg1_recipe[sent+k][j]
              verb2_args2 = arg2_recipe[sent+k][j]
              ####
              #### args1_args2_verb_verb_score and args1_verb_verb_score ####
              for a1 in args1:
                arg1 = self.stemmer.stem(a1)
                args1_verb_verb_score[arg1][verb][verb2] = 1
                if verb2 not in args1_verb_verb_args1_score[arg1][verb]:
                  args1_verb_verb_args1_score[arg1][verb][verb2] = {}
                for a in verb2_args1:
                  arg = self.stemmer.stem(a)
                  args1_verb_verb_args1_score[arg1][verb][verb2][arg] = 1
                  #### args1_verb_args_score ####
                  args1_verb_args_score[arg1][verb][arg] = 1
                #### args1_verb_args_score ####
                for a in verb2_args2:
                  arg = self.stemmer.stem(a)
                  args1_verb_args_score[arg1][verb][arg] = 1
                for a2 in args2:
                  arg2 = self.stemmer.stem(a2)
                  if verb2 not in args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
                    args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2] = {}
                  args1_args2_verb_verb_score[arg1][arg2][verb][verb2] = 1
                  for a in verb2_args1:
                    arg = self.stemmer.stem(a)
                    args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] = 1
                    #### args1_args2_verb_args_score ####
                    args1_args2_verb_args_score[arg1][arg2][verb][arg] = 1
                  #### args1_args2_verb_args_score ####
                  for a in verb2_args2:
                    arg = self.stemmer.stem(a)
                    args1_args2_verb_args_score[arg1][arg2][verb][arg] = 1
              ####
              # score = None
              # if k==0:
              #   score = float(j-i)/len(recipe[sent])
              # else:
              #   score = float(k)/len(recipe)
              # if verb2 not in verbs[verb] or verbs[verb][verb2]<score:
              #   verbs[verb][verb2] = score
            #### Consider arguments
            if k==0:
              continue
            k_args1 = arg1_recipe[sent+k]
            for as1 in k_args1:
              for a1 in as1:
                arg1 = self.stemmer.stem(a1)
                verb_args1[verb][arg1] = 1
                # if arg1 not in verb_args1[verb] or verb_args1[verb][arg1]<score:
                #   verb_args1[verb][arg1] = score
            k_args2 = arg1_recipe[sent+k]
            for as2 in k_args2:
              for a2 in as2:
                arg2 = self.stemmer.stem(a2)
                verb_args2[verb][arg2] = 1
                # if arg2 not in verb_args2[verb] or verb_args2[verb][arg2]<score:
                #   verb_args2[verb][arg2] = score
        # Arg1 - Arg1 statistics
        args1_0 = arg1_recipe[sent]
        for k in range(self.sent_window-1):
            if sent+k+1>=len(recipe):
              break
            args1 = arg1_recipe[sent+k+1]
            for as1_0 in args1_0:
              for a1_0 in as1_0:
                arg1_0 = self.stemmer.stem(a1_0)
                if arg1_0 not in args1_args1:
                  args1_args1[arg1_0] = {}
                for as1 in args1:
                  for a1 in as1:
                    arg1 = self.stemmer.stem(a1)
                    args1_args1[arg1_0][arg1] = 1
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

      for arg in args1_args1:
        if arg not in self.args1_args_score:
          self.args1_args_score[arg] = {}
        if arg not in cnt_arg1:
          cnt_arg1[arg] = 1
        else:
          cnt_arg1[arg] += 1
        for arg1 in args1_args1[arg]:
          if arg1 not in self.args1_args_score[arg]:
            self.args1_args_score[arg][arg1] = args1_args1[arg][arg1]
          else:
            self.args1_args_score[arg][arg1] += args1_args1[arg][arg1]

      for arg1 in args1_args2_verb_verb_score:
        if arg1 not in cnt_arg1_arg2_verb:
          cnt_arg1_arg2_verb[arg1] = {}
        if arg1 not in self.args1_args2_verb_verb_score:
          self.args1_args2_verb_verb_score[arg1] = {}
        for arg2 in args1_args2_verb_verb_score[arg1]:
          if arg2 not in cnt_arg1_arg2_verb[arg1]:
            cnt_arg1_arg2_verb[arg1][arg2] = {}
          if arg2 not in self.args1_args2_verb_verb_score[arg1]:
            self.args1_args2_verb_verb_score[arg1][arg2] = {}
          for verb in args1_args2_verb_verb_score[arg1][arg2]:
            if verb not in cnt_arg1_arg2_verb[arg1][arg2]:
              cnt_arg1_arg2_verb[arg1][arg2][verb] = 1
            else:
              cnt_arg1_arg2_verb[arg1][arg2][verb] += 1
            if verb not in self.args1_args2_verb_verb_score[arg1][arg2]:
              self.args1_args2_verb_verb_score[arg1][arg2][verb] = {}
            for verb2 in args1_args2_verb_verb_score[arg1][arg2][verb]:
              if verb2 not in self.args1_args2_verb_verb_score[arg1][arg2][verb]:
                self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2] = args1_args2_verb_verb_score[arg1][arg2][verb][verb2]
              else:
                self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2] += args1_args2_verb_verb_score[arg1][arg2][verb][verb2]

      for arg1 in args1_args2_verb_args_score:
        if arg1 not in self.args1_args2_verb_args_score:
          self.args1_args2_verb_args_score[arg1] = {}
        for arg2 in args1_args2_verb_args_score[arg1]:
          if arg2 not in self.args1_args2_verb_args_score[arg1]:
            self.args1_args2_verb_args_score[arg1][arg2] = {}
          for verb in args1_args2_verb_args_score[arg1][arg2]:
            if verb not in self.args1_args2_verb_args_score[arg1][arg2]:
              self.args1_args2_verb_args_score[arg1][arg2][verb] = {}
            for arg in args1_args2_verb_args_score[arg1][arg2][verb]:
              if arg not in self.args1_args2_verb_args_score[arg1][arg2][verb]:
                self.args1_args2_verb_args_score[arg1][arg2][verb][arg] = args1_args2_verb_args_score[arg1][arg2][verb][arg]
              else:
                self.args1_args2_verb_args_score[arg1][arg2][verb][arg] += args1_args2_verb_args_score[arg1][arg2][verb][arg]

      for arg1 in args1_args2_verb_verb_args1_score:
        if arg1 not in self.args1_args2_verb_verb_args1_score:
          self.args1_args2_verb_verb_args1_score[arg1] = {}
        for arg2 in args1_args2_verb_verb_args1_score[arg1]:
          if arg2 not in self.args1_args2_verb_verb_args1_score[arg1]:
            self.args1_args2_verb_verb_args1_score[arg1][arg2] = {}
          for verb in args1_args2_verb_verb_args1_score[arg1][arg2]:
            if verb not in self.args1_args2_verb_verb_args1_score[arg1][arg2]:
              self.args1_args2_verb_verb_args1_score[arg1][arg2][verb] = {}
            for verb2 in args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
              if verb2 not in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
                self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2] = {}
              for arg in args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
                if arg not in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
                  self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] = args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg]
                else:
                  self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] += args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg]

      for arg1 in args1_verb_verb_score:
        if arg1 not in cnt_arg1_verb:
          cnt_arg1_verb[arg1] = {}
        if arg1 not in self.args1_verb_verb_score:
          self.args1_verb_verb_score[arg1] = {}
        for verb in args1_verb_verb_score[arg1]:
            if verb not in cnt_arg1_verb[arg1]:
              cnt_arg1_verb[arg1][verb] = 1
            else:
              cnt_arg1_verb[arg1][verb] += 1
            if verb not in self.args1_verb_verb_score[arg1]:
              self.args1_verb_verb_score[arg1][verb] = {}
            for verb2 in args1_verb_verb_score[arg1][verb]:
              if verb2 not in self.args1_verb_verb_score[arg1][verb]:
                self.args1_verb_verb_score[arg1][verb][verb2] = args1_verb_verb_score[arg1][verb][verb2]
              else:
                self.args1_verb_verb_score[arg1][verb][verb2] += args1_verb_verb_score[arg1][verb][verb2]

      for arg1 in args1_verb_args_score:
        if arg1 not in self.args1_verb_args_score:
          self.args1_verb_args_score[arg1] = {}
        for verb in args1_verb_args_score[arg1]:
            if verb not in self.args1_verb_args_score[arg1]:
              self.args1_verb_args_score[arg1][verb] = {}
            for arg in args1_verb_args_score[arg1][verb]:
              if arg not in self.args1_verb_args_score[arg1][verb]:
                self.args1_verb_args_score[arg1][verb][arg] = args1_verb_args_score[arg1][verb][arg]
              else:
                self.args1_verb_args_score[arg1][verb][arg] += args1_verb_args_score[arg1][verb][arg]

      for arg1 in args1_verb_verb_args1_score:
        if arg1 not in self.args1_verb_verb_args1_score:
          self.args1_verb_verb_args1_score[arg1] = {}
        for verb in args1_verb_verb_args1_score[arg1]:
            if verb not in self.args1_verb_verb_args1_score[arg1]:
              self.args1_verb_verb_args1_score[arg1][verb] = {}
            for verb2 in args1_verb_verb_args1_score[arg1][verb]:
              if verb2 not in self.args1_verb_verb_args1_score[arg1][verb]:
                self.args1_verb_verb_args1_score[arg1][verb][verb2] = {}
              for arg in args1_verb_verb_args1_score[arg1][verb][verb2]:
                if arg not in self.args1_verb_verb_args1_score[arg1][verb][verb2]:
                  self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] = args1_verb_verb_args1_score[arg1][verb][verb2][arg]
                else:
                  self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] += args1_verb_verb_args1_score[arg1][verb][verb2][arg]


    #normalization of all counts here
    for verb in self.verbs_score:
      for verb2 in self.verbs_score[verb]:
        self.verbs_score[verb][verb2] = float(self.verbs_score[verb][verb2])/cnt[verb]
      for arg1 in self.verb_args1_score[verb]:
        self.verb_args1_score[verb][arg1] = float(self.verb_args1_score[verb][arg1])/cnt[verb]
      for arg2 in self.verb_args2_score[verb]:
        self.verb_args2_score[verb][arg2] = float(self.verb_args2_score[verb][arg2])/cnt[verb]

    for arg in self.args1_args_score:
      for arg1 in self.args1_args_score[arg]:
        self.args1_args_score[arg][arg1] = float(self.args1_args_score[arg][arg1])/cnt_arg1[arg]

    for arg in self.args_verb_score:
      for verb in self.args_verb_score[arg]:
        self.args_verb_score[arg][verb] = float(self.args_verb_score[arg][verb])/cnt_arg2[arg]

    for arg1 in self.args1_args2_verb_verb_score:
      for arg2 in self.args1_args2_verb_verb_score[arg1]:
        for verb in self.args1_args2_verb_verb_score[arg1][arg2]:
          for verb2 in self.args1_args2_verb_verb_score[arg1][arg2][verb]:
            self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2] = float(self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2])/cnt_arg1_arg2_verb[arg1][arg2][verb]

    for arg1 in self.args1_args2_verb_args_score:
      for arg2 in self.args1_args2_verb_args_score[arg1]:
        for verb in self.args1_args2_verb_args_score[arg1][arg2]:
          for verb2 in self.args1_args2_verb_args_score[arg1][arg2][verb]:
            self.args1_args2_verb_args_score[arg1][arg2][verb][verb2] = float(self.args1_args2_verb_args_score[arg1][arg2][verb][verb2])/cnt_arg1_arg2_verb[arg1][arg2][verb]

    for arg1 in self.args1_verb_verb_score:
        for verb in self.args1_verb_verb_score[arg1]:
          for verb2 in self.args1_verb_verb_score[arg1][verb]:
            self.args1_verb_verb_score[arg1][verb][verb2] = float(self.args1_verb_verb_score[arg1][verb][verb2])/cnt_arg1_verb[arg1][verb]

    for arg1 in self.args1_verb_args_score:
        for verb in self.args1_verb_args_score[arg1]:
          for verb2 in self.args1_verb_args_score[arg1][verb]:
            self.args1_verb_args_score[arg1][verb][verb2] = float(self.args1_verb_args_score[arg1][verb][verb2])/cnt_arg1_verb[arg1][verb]

    for arg1 in self.args1_args2_verb_verb_args1_score:
      for arg2 in self.args1_args2_verb_verb_args1_score[arg1]:
        for verb in self.args1_args2_verb_verb_args1_score[arg1][arg2]:
          for verb2 in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
            for arg in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
              self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] = float(self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg])/cnt_arg1_arg2_verb[arg1][arg2][verb]

    for arg1 in self.args1_verb_verb_args1_score:
        for verb in self.args1_verb_verb_args1_score[arg1]:
          for verb2 in self.args1_verb_verb_args1_score[arg1][verb]:
            for arg in self.args1_verb_verb_args1_score[arg1][verb][verb2]:
              self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] = float(self.args1_verb_verb_args1_score[arg1][verb][verb2][arg])/cnt_arg1_verb[arg1][verb]


  def calcStatFromGraph(self, stat_data, useArbo, transitive=False):
    self.verbs_score = {}
    self.args_verb_score = {}
    self.verb_args1_score = {}
    self.verb_args2_score = {}
    self.args1_args_score = {}
    self.args1_args2_args_score = {}
    self.args1_args2_verb_args_score = {}
    self.args1_verb_args_score = {}
    self.args1_args2_verb_verb_score = {}
    self.args1_verb_verb_score = {}
    self.args1_args2_verb_verb_args1_score = {}
    self.args1_verb_verb_args1_score = {}
    self.cnt = {}
    self.cnt_arg = {}
    self.cnt_arg1 = {}
    self.cnt_arg2 = {}
    self.cnt_arg1_verb = {}
    self.cnt_arg1_arg2_verb = {}
    self.cnt_arg1_arg2 = {}
    for [file_name,weighted_graph, arbor_adapter, arbor_edges] in stat_data:
      # print file_name
      self.updateStatFromGraph(weighted_graph, arbor_adapter, arbor_edges, useArbo, transitive)
      pass
    for verb in self.verbs_score:
      for verb2 in self.verbs_score[verb]:
        self.verbs_score[verb][verb2] = self.calcFreq(self.verbs_score[verb][verb2],self.cnt[verb])
      for arg1 in self.verb_args1_score[verb]:
        self.verb_args1_score[verb][arg1] = self.calcFreq(self.verb_args1_score[verb][arg1],self.cnt[verb])
      for arg2 in self.verb_args2_score[verb]:
        self.verb_args2_score[verb][arg2] = self.calcFreq(self.verb_args2_score[verb][arg2],self.cnt[verb])

    for arg in self.args1_args_score:
      for arg1 in self.args1_args_score[arg]:
        self.args1_args_score[arg][arg1] = self.calcFreq(self.args1_args_score[arg][arg1],self.cnt_arg1[arg])

    for arg1 in self.args1_args2_args_score:
      for arg2 in self.args1_args2_args_score[arg1]:
        for arg in self.args1_args2_args_score[arg1][arg2]:
          self.args1_args2_args_score[arg1][arg2][arg] = self.calcFreq(self.args1_args2_args_score[arg1][arg2][arg],self.cnt_arg1_arg2[arg1][arg2])

    for arg in self.args_verb_score:
      for verb in self.args_verb_score[arg]:
        # self.args_verb_score[arg][verb] = self.calcFreq(self.args_verb_score[arg][verb],self.cnt_arg2[arg])
        self.args_verb_score[arg][verb] = self.calcFreq(self.args_verb_score[arg][verb],self.cnt_arg[arg])

    for arg1 in self.args1_args2_verb_args_score:
      for arg2 in self.args1_args2_verb_args_score[arg1]:
        for verb in self.args1_args2_verb_args_score[arg1][arg2]:
          for arg in self.args1_args2_verb_args_score[arg1][arg2][verb]:
            self.args1_args2_verb_args_score[arg1][arg2][verb][arg] = self.calcFreq(self.args1_args2_verb_args_score[arg1][arg2][verb][arg],self.cnt_arg1_arg2_verb[arg1][arg2][verb])

    for arg1 in self.args1_verb_args_score:
      for verb in self.args1_verb_args_score[arg1]:
        for arg in self.args1_verb_args_score[arg1][verb]:
          self.args1_verb_args_score[arg1][verb][arg] = self.calcFreq(self.args1_verb_args_score[arg1][verb][arg],self.cnt_arg1_verb[arg1][verb])

    for arg1 in self.args1_args2_verb_verb_score:
      for arg2 in self.args1_args2_verb_verb_score[arg1]:
        for verb in self.args1_args2_verb_verb_score[arg1][arg2]:
          for arg in self.args1_args2_verb_verb_score[arg1][arg2][verb]:
            self.args1_args2_verb_verb_score[arg1][arg2][verb][arg] = self.calcFreq(self.args1_args2_verb_verb_score[arg1][arg2][verb][arg],self.cnt_arg1_arg2_verb[arg1][arg2][verb])

    for arg1 in self.args1_verb_verb_score:
      for verb in self.args1_verb_verb_score[arg1]:
        for arg in self.args1_verb_verb_score[arg1][verb]:
          self.args1_verb_verb_score[arg1][verb][arg] = self.calcFreq(self.args1_verb_verb_score[arg1][verb][arg],self.cnt_arg1_verb[arg1][verb])

    for arg1 in self.args1_args2_verb_verb_args1_score:
      for arg2 in self.args1_args2_verb_verb_args1_score[arg1]:
        for verb in self.args1_args2_verb_verb_args1_score[arg1][arg2]:
          for verb2 in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
            for arg in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
              self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] = self.calcFreq(self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg],self.cnt_arg1_arg2_verb[arg1][arg2][verb])

    for arg1 in self.args1_verb_verb_args1_score:
      for verb in self.args1_verb_verb_args1_score[arg1]:
        for verb2 in self.args1_verb_verb_args1_score[arg1][verb]:
          for arg in self.args1_verb_verb_args1_score[arg1][verb][verb2]:
            self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] = self.calcFreq(self.args1_verb_verb_args1_score[arg1][verb][verb2][arg],self.cnt_arg1_verb[arg1][verb])

  def calcFreq(self, freq, cnt):
    if freq==1 and cnt==1:
      return 0
    return float(freq)/cnt

  def findInputArgument(self, node, reverse_g, id_node_map):
    if node.id not in reverse_g:
      return None

    for node_id in reverse_g[node.id]:
      node2 = id_node_map[node_id]
      if isinstance(node2,RNode) and node2.arg_type=="arg1":

        return node2

    for node_id in reverse_g[node.id]:
      node2 = id_node_map[node_id]
      if isinstance(node2,PNode):
        node3 = self.findInputArgument(node2,reverse_g, id_node_map)
        if node3!=None:
          return node3

    return None

  def findInputArgument2(self, node, reverse_g, id_node_map):
    if node.id not in reverse_g:
      return None

    for node_id in reverse_g[node.id]:
      node2 = id_node_map[node_id]
      if isinstance(node2,RNode) and node2.arg_type=="arg2":
        return node2

    return None

  def getTransClosure(self,g,id_node_map):
    res = {}
    for s in g:
      s_node = id_node_map[s]
      res[s] = {}
      for d in g[s]:
        res[s][d] = res[s][d] + 1 if d in res[s] else 1
      if not isinstance(s_node,PNode):
        continue
      self.getTransClosureBranch(s,s,res,g,id_node_map)
    return res

  def getTransClosureBranch(self,s,c,res,g,id_node_map,visited={}):
    for d in g[c]:
      if d in visited:
        continue
      d_node = id_node_map[d]
      if not isinstance(d_node,PNode):
        continue
      visited[d] = 1

      res[s][d] = res[s][d] + 1 if d in res[s] else 1

      self.getTransClosureBranch(s,d,res,g,id_node_map,visited)

  def updateStatFromGraph(self, weighted_graph, arbor_adapter, arbor_edges, useArbo, transitive):
    verbs_score = {}
    verb_args1_score = {}
    verb_args2_score = {}
    args1_args_score = {}
    args1_args2_args_score = {}
    args_verb_score = {}
    args1_args2_verb_args_score = {}
    args1_verb_args_score = {}
    args1_args2_verb_verb_score = {}
    args1_verb_verb_score = {}
    args1_args2_verb_verb_args1_score = {}
    args1_verb_verb_args1_score = {}
    g = {}
    # Artificially connect verb to verb 2 if there is a path verb->arg2->verb2
    g_copy = weighted_graph.adj_list
    if useArbo:
      g_copy = arbor_edges
    for s in g_copy:
      g[s] = {}
      for d in g_copy[s]:
        # g[s][d] = arbor_edges[s][d]
        g[s][d] = 1
    if transitive:
      g = self.getTransClosure(g, arbor_adapter.id_node_map)
    else:
      for s in g_copy:
        s_node = arbor_adapter.id_node_map[s]
        if not isinstance(s_node,PNode):
          continue
        for d in g_copy[s]:
          if d not in g_copy:
            continue
          d_node = arbor_adapter.id_node_map[d]
          # if not isinstance(d_node,RNode) or d_node.arg_type!="arg2":
          if not isinstance(d_node,RNode):
            continue
          for v in g_copy[d]:
            v_node = arbor_adapter.id_node_map[v]
            if not isinstance(v_node,PNode):
              continue
            g[s][v] = "use"

    reverse_g = {}
    for s in g:
      for d in g[s]:
        if d not in reverse_g:
          reverse_g[d] = {}
        reverse_g[d][s] = g[s][d]

    for s in g:
      # if not useArbo and s not in weighted_graph.adj_list:
      #   continue
      node1 = arbor_adapter.id_node_map[s]
      verb1 = None
      verb1_arg = None
      verb1_arg2 = None
      if isinstance(node1,PNode):
        verb1 = self.stemmer.stem(node1.predicate)
        verb1_arg = self.findInputArgument(node1,reverse_g,weighted_graph.id_node_map)
        verb1_arg2 = self.findInputArgument2(node1,reverse_g,weighted_graph.id_node_map)
        if verb1 not in verbs_score:
          verbs_score[verb1] = {}
          verb_args1_score[verb1] = {}
          verb_args2_score[verb1] = {}
      elif isinstance(node1,RNode):
        pass
      for d in g[s]:
        # if not useArbo and d not in weighted_graph.adj_list[s] and g[s][d]!="use":
        #   continue
        node2 = arbor_adapter.id_node_map[d]
        if isinstance(node1,PNode) and isinstance(node2,PNode):
          verb2 = self.stemmer.stem(node2.predicate)
          verb2_arg = self.findInputArgument(node2,reverse_g,weighted_graph.id_node_map)
          verb2_arg2 = self.findInputArgument2(node2,reverse_g,weighted_graph.id_node_map)
          verbs_score[verb1][verb2] = 1
          verb1_args = []
          if verb1_arg!=None:
            verb1_args = verb1_arg.getNouns()
          verb2_args = []
          if verb2_arg!=None:
            verb2_args = verb2_arg.getNouns()
          verb2_args2 = []
          if verb2_arg2!=None:
            verb2_args2 = verb2_arg2.getNouns()
          verb1_args2 = []
          if verb1_arg2 != None:
            verb1_args2 = verb1_arg2.getNouns()
          for a1 in verb1_args:
            arg1 = self.stemmer.stem(a1)
          #   if arg1 not in args1_args_score:
          #     args1_args_score[arg1] = {}
            # for a2 in verb2_args:
            #   arg2 = self.stemmer.stem(a2)
            #   args1_args_score[arg1][arg2] = 1

            # args1_args2_verb_verb_score and args1_verb_verb_score
            # args1_args2_verb_verb_args1_score and args1_verb_verb_args1_score
            if arg1 not in args1_args2_verb_args_score:
              args1_args2_verb_args_score[arg1] = {}
            if arg1 not in args1_args2_verb_verb_score:
              args1_args2_verb_verb_score[arg1] = {}
            if arg1 not in args1_args2_verb_verb_args1_score:
              args1_args2_verb_verb_args1_score[arg1] = {}
            if arg1 not in args1_verb_verb_score:
              args1_verb_verb_score[arg1] = {}
            if arg1 not in args1_verb_verb_args1_score:
              args1_verb_verb_args1_score[arg1] = {}
            # args1_verb_args_score
            if verb1 not in args1_verb_verb_score[arg1]:
              args1_verb_verb_score[arg1][verb1] = {}
            if verb1 not in args1_verb_verb_args1_score[arg1]:
              args1_verb_verb_args1_score[arg1][verb1] = {}
            if verb2 not in args1_verb_verb_args1_score[arg1][verb1]:
              args1_verb_verb_args1_score[arg1][verb1][verb2] = {}
            args1_verb_verb_score[arg1][verb1][verb2] = 1

            # args1_verb_verb_args1_score
            for a in verb2_args:
              arg = self.stemmer.stem(a)
              args1_verb_verb_args1_score[arg1][verb1][verb2][arg]=1
            for a in verb2_args2:
              arg = self.stemmer.stem(a)
              args1_verb_verb_args1_score[arg1][verb1][verb2][arg]=1

            # args1_args2_verb_args_score
            for a2 in verb1_args2:
                arg2 = self.stemmer.stem(a2)
                if arg2 not in args1_args2_verb_verb_score[arg1]:
                  args1_args2_verb_verb_score[arg1][arg2] = {}
                if arg2 not in args1_args2_verb_verb_args1_score[arg1]:
                  args1_args2_verb_verb_args1_score[arg1][arg2] = {}
                if verb1 not in args1_args2_verb_verb_score[arg1][arg2]:
                  args1_args2_verb_verb_score[arg1][arg2][verb1] = {}
                if verb1 not in args1_args2_verb_verb_args1_score[arg1][arg2]:
                  args1_args2_verb_verb_args1_score[arg1][arg2][verb1] = {}
                args1_args2_verb_verb_score[arg1][arg2][verb1][verb2] = 1
                if verb2 not in args1_args2_verb_verb_args1_score[arg1][arg2][verb1]:
                  args1_args2_verb_verb_args1_score[arg1][arg2][verb1][verb2] = {}
                # args1_args2_verb_verb_args1_score
                for a in verb2_args:
                  arg = self.stemmer.stem(a)
                  args1_args2_verb_verb_args1_score[arg1][arg2][verb1][verb2][arg]=1
                for a in verb2_args2:
                  arg = self.stemmer.stem(a)
                  args1_args2_verb_verb_args1_score[arg1][arg2][verb1][verb2][arg]=1

        elif isinstance(node1,PNode) and isinstance(node2,RNode):
          if node2.is_null == True:
            print 'NULL NODE!!! 675' + str(node2.getNouns())

          args = node2.getNouns()
          verb1_args = []
          if verb1_arg!=None:
            verb1_args = verb1_arg.getNouns()
          verb1_args2 = []
          if verb1_arg2 != None:
            verb1_args2 = verb1_arg2.getNouns()
          for a in args:
            arg = self.stemmer.stem(a)
            if node2.arg_type=="arg1":
              verb_args1_score[verb1][arg] = 1
            elif node2.arg_type=="arg2":
              verb_args2_score[verb1][arg] = 1

            # args1_args2_verb_args_score and args1_verb_args_score
            for a1 in verb1_args:
              arg1 = self.stemmer.stem(a1)
              if arg1 not in args1_args2_verb_args_score:
                args1_args2_verb_args_score[arg1] = {}
              if arg1 not in args1_args2_args_score:
                args1_args2_args_score[arg1] = {}
              if arg1 not in args1_verb_args_score:
                args1_verb_args_score[arg1] = {}
              if arg1 not in args1_args_score:
                args1_args_score[arg1] = {}
              # args1_verb_args_score
              if verb1 not in args1_verb_args_score[arg1]:
                args1_verb_args_score[arg1][verb1] = {}
              args1_verb_args_score[arg1][verb1][arg] = 1
              args1_args_score[arg1][arg] = 1
              # args1_args2_verb_args_score
              for a2 in verb1_args2:
                arg2 = self.stemmer.stem(a2)
                if arg2 not in args1_args2_verb_args_score[arg1]:
                  args1_args2_verb_args_score[arg1][arg2] = {}
                if arg2 not in args1_args2_args_score[arg1]:
                  args1_args2_args_score[arg1][arg2] = {}
                if verb1 not in args1_args2_verb_args_score[arg1][arg2]:
                  args1_args2_verb_args_score[arg1][arg2][verb1] = {}
                args1_args2_verb_args_score[arg1][arg2][verb1][arg] = 1
                args1_args2_args_score[arg1][arg2][arg] = 1
        elif isinstance(node1,RNode) and isinstance(node2,PNode):
            # if node1.is_null == True:
            #   print 'NULL NODE!!! 719' + str(node1.getNouns())

          # if node1.arg_type=="arg2":
            verb2 = self.stemmer.stem(node2.predicate)
            nouns = node1.getNouns()
            for a in nouns:
              arg = self.stemmer.stem(a)
              if arg not in args_verb_score:
                args_verb_score[arg] = {}
              args_verb_score[arg][verb2] = 1


    for verb1 in verbs_score:
      if verb1 in self.verbs_score:
        self.cnt[verb1] += 1
      else:
        self.verbs_score[verb1] = {}
        self.verb_args1_score[verb1] = {}
        self.verb_args2_score[verb1] = {}
        self.cnt[verb1] = 1
      for verb2 in verbs_score[verb1]:
        if verb2 in self.verbs_score[verb1]:
          self.verbs_score[verb1][verb2] += verbs_score[verb1][verb2]
        else:
          self.verbs_score[verb1][verb2] = verbs_score[verb1][verb2]
      for arg1 in verb_args1_score[verb1]:
        if arg1 in self.verb_args1_score[verb1]:
          self.verb_args1_score[verb1][arg1] += verb_args1_score[verb1][arg1]
        else:
          self.verb_args1_score[verb1][arg1] = verb_args1_score[verb1][arg1]
      for arg2 in verb_args2_score[verb1]:
        if arg2 in self.verb_args2_score[verb1]:
          self.verb_args2_score[verb1][arg2] += verb_args2_score[verb1][arg2]
        else:
          self.verb_args2_score[verb1][arg2] = verb_args2_score[verb1][arg2]

    for arg in args1_args_score:
        if arg not in self.cnt_arg1:
          self.cnt_arg1[arg] = 1
          self.args1_args_score[arg] = {}
        else:
          self.cnt_arg1[arg] += 1
        for arg1 in args1_args_score[arg]:
          if arg1 not in self.args1_args_score[arg]:
            self.args1_args_score[arg][arg1] = args1_args_score[arg][arg1]
          else:
            self.args1_args_score[arg][arg1] += args1_args_score[arg][arg1]

    for arg1 in args1_args2_args_score:
        if arg1 not in self.cnt_arg1_arg2:
          self.cnt_arg1_arg2[arg1] = {}
        if arg1 not in self.args1_args2_args_score:
          self.args1_args2_args_score[arg1] = {}
        for arg2 in args1_args2_args_score[arg1]:
          if arg2 not in self.args1_args2_args_score[arg1]:
            self.args1_args2_args_score[arg1][arg2] = {}
          if arg2 not in self.cnt_arg1_arg2[arg1]:
            self.cnt_arg1_arg2[arg1][arg2] = 1
          else:
            self.cnt_arg1_arg2[arg1][arg2] += 1
          for arg in args1_args2_args_score[arg1][arg2]:
            if arg not in self.args1_args2_args_score[arg1][arg2]:
              self.args1_args2_args_score[arg1][arg2][arg] = args1_args2_args_score[arg1][arg2][arg]
            else:
              self.args1_args2_args_score[arg1][arg2][arg] += args1_args2_args_score[arg1][arg2][arg]

    for arg in args_verb_score:
        if arg=="salt":
          pass
        # if arg not in self.cnt_arg2:
        #   self.cnt_arg2[arg] = 1
        #   self.args_verb_score[arg] = {}
        # else:
        #   self.cnt_arg2[arg] += 1
        if arg not in self.cnt_arg:
          self.cnt_arg[arg] = 1
        else:
          self.cnt_arg[arg] += 1
        if arg not in self.args_verb_score:
          self.args_verb_score[arg] = {}
        for verb in args_verb_score[arg]:
          if verb not in self.args_verb_score[arg]:
            self.args_verb_score[arg][verb] = args_verb_score[arg][verb]
          else:
            self.args_verb_score[arg][verb] += args_verb_score[arg][verb]

    for arg1 in args1_args2_verb_args_score:
      if arg1 not in self.args1_args2_verb_args_score:
        self.args1_args2_verb_args_score[arg1] = {}
      if arg1 not in self.cnt_arg1_arg2_verb:
        self.cnt_arg1_arg2_verb[arg1] = {}
      for arg2 in args1_args2_verb_args_score[arg1]:
        if arg2 not in self.args1_args2_verb_args_score[arg1]:
          self.args1_args2_verb_args_score[arg1][arg2] = {}
        if arg2 not in self.cnt_arg1_arg2_verb[arg1]:
          self.cnt_arg1_arg2_verb[arg1][arg2] = {}
        for verb in args1_args2_verb_args_score[arg1][arg2]:
          if verb not in self.args1_args2_verb_args_score[arg1][arg2]:
            self.args1_args2_verb_args_score[arg1][arg2][verb] = {}
          if verb not in self.cnt_arg1_arg2_verb[arg1][arg2]:
            self.cnt_arg1_arg2_verb[arg1][arg2][verb] = 1
          else:
            self.cnt_arg1_arg2_verb[arg1][arg2][verb] += 1
          for arg in args1_args2_verb_args_score[arg1][arg2][verb]:
            if arg not in self.args1_args2_verb_args_score[arg1][arg2][verb]:
              self.args1_args2_verb_args_score[arg1][arg2][verb][arg] = args1_args2_verb_args_score[arg1][arg2][verb][arg]
            else:
              self.args1_args2_verb_args_score[arg1][arg2][verb][arg] += args1_args2_verb_args_score[arg1][arg2][verb][arg]

    for arg1 in args1_verb_args_score:
      if arg1 not in self.args1_verb_args_score:
        self.args1_verb_args_score[arg1] = {}
      if arg1 not in self.cnt_arg1_verb:
        self.cnt_arg1_verb[arg1] = {}
      for verb in args1_verb_args_score[arg1]:
          if verb not in self.args1_verb_args_score[arg1]:
            self.args1_verb_args_score[arg1][verb] = {}
          if verb not in self.cnt_arg1_verb[arg1]:
            self.cnt_arg1_verb[arg1][verb] = 1
          else:
            self.cnt_arg1_verb[arg1][verb] += 1
          for arg in args1_verb_args_score[arg1][verb]:
            if arg not in self.args1_verb_args_score[arg1][verb]:
              self.args1_verb_args_score[arg1][verb][arg] = args1_verb_args_score[arg1][verb][arg]
            else:
              self.args1_verb_args_score[arg1][verb][arg] += args1_verb_args_score[arg1][verb][arg]

    for arg1 in args1_args2_verb_verb_score:
      if arg1 not in self.args1_args2_verb_verb_score:
        self.args1_args2_verb_verb_score[arg1] = {}
      if arg1 not in self.args1_args2_verb_verb_args1_score:
        self.args1_args2_verb_verb_args1_score[arg1] = {}
      if arg1 not in self.cnt_arg1_arg2_verb:
        self.cnt_arg1_arg2_verb[arg1] = {}
      for arg2 in args1_args2_verb_verb_score[arg1]:
        if arg2 not in self.args1_args2_verb_verb_score[arg1]:
          self.args1_args2_verb_verb_score[arg1][arg2] = {}
        if arg2 not in self.args1_args2_verb_verb_args1_score[arg1]:
          self.args1_args2_verb_verb_args1_score[arg1][arg2] = {}
        if arg2 not in self.cnt_arg1_arg2_verb[arg1]:
          self.cnt_arg1_arg2_verb[arg1][arg2] = {}
        for verb in args1_args2_verb_verb_score[arg1][arg2]:
          if verb not in self.args1_args2_verb_verb_score[arg1][arg2]:
            self.args1_args2_verb_verb_score[arg1][arg2][verb] = {}
          if verb not in self.args1_args2_verb_verb_args1_score[arg1][arg2]:
            self.args1_args2_verb_verb_args1_score[arg1][arg2][verb] = {}
          if verb not in self.cnt_arg1_arg2_verb[arg1][arg2]:
            self.cnt_arg1_arg2_verb[arg1][arg2][verb] = 1
          else:
            self.cnt_arg1_arg2_verb[arg1][arg2][verb] += 1
          for verb2 in args1_args2_verb_verb_score[arg1][arg2][verb]:
            if verb2 not in self.args1_args2_verb_verb_score[arg1][arg2][verb]:
              self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2] = args1_args2_verb_verb_score[arg1][arg2][verb][verb2]
            else:
              self.args1_args2_verb_verb_score[arg1][arg2][verb][verb2] += args1_args2_verb_verb_score[arg1][arg2][verb][verb2]
            if verb2 not in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
              self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2] = {}
            for arg in args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
              # if arg1=="oven" and verb=="preheat" and verb2=="bring" and (arg=="boil" or arg=="water"):
              #   pass
              if arg not in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2]:
                self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] = args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg]
              else:
                self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg] += args1_args2_verb_verb_args1_score[arg1][arg2][verb][verb2][arg]

    for arg1 in args1_verb_verb_score:
      if arg1 not in self.args1_verb_verb_score:
        self.args1_verb_verb_score[arg1] = {}
      if arg1 not in self.args1_verb_verb_args1_score:
        self.args1_verb_verb_args1_score[arg1] = {}
      if arg1 not in self.cnt_arg1_verb:
        self.cnt_arg1_verb[arg1] = {}
      for verb in args1_verb_verb_score[arg1]:
          if verb not in self.args1_verb_verb_score[arg1]:
            self.args1_verb_verb_score[arg1][verb] = {}
          if verb not in self.args1_verb_verb_args1_score[arg1]:
            self.args1_verb_verb_args1_score[arg1][verb] = {}
          if verb not in self.cnt_arg1_verb[arg1]:
            self.cnt_arg1_verb[arg1][verb] = 1
          else:
            self.cnt_arg1_verb[arg1][verb] += 1
          for verb2 in args1_verb_verb_score[arg1][verb]:
            if verb2 not in self.args1_verb_verb_score[arg1][verb]:
              self.args1_verb_verb_score[arg1][verb][verb2] = args1_verb_verb_score[arg1][verb][verb2]
            else:
              self.args1_verb_verb_score[arg1][verb][verb2] += args1_verb_verb_score[arg1][verb][verb2]
            if verb2 not in self.args1_verb_verb_args1_score[arg1][verb]:
              self.args1_verb_verb_args1_score[arg1][verb][verb2] = {}
            for arg in args1_verb_verb_args1_score[arg1][verb][verb2]:
              if arg not in self.args1_verb_verb_args1_score[arg1][verb][verb2]:
                self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] = args1_verb_verb_args1_score[arg1][verb][verb2][arg]
              else:
                self.args1_verb_verb_args1_score[arg1][verb][verb2][arg] += args1_verb_verb_args1_score[arg1][verb][verb2][arg]

  def getArg1PredArg(self, input_a1, predicate, output_a):
    a1s = input_a1.getNouns()
    oas = output_a.getNouns()
    verb = self.stemmer.stem(predicate.predicate)
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_verb_args_score:
        continue
      if verb not in self.args1_verb_args_score[arg1]:
        continue
      for o in oas:
        o_arg = self.stemmer.stem(o)
        if o_arg in self.args1_verb_args_score[arg1][verb]:
          s+= self.args1_verb_args_score[arg1][verb][o_arg]
        cnt+=1
    if cnt==0:
      return 0
    return self.log(1 - (float(s)/cnt))

  def getArg1PredPred(self, input_a1, predicate, output_predicate):
    a1s = input_a1.getNouns()
    overb = self.stemmer.stem(output_predicate.predicate)
    verb = self.stemmer.stem(predicate.predicate)
    return self.getArg1PredPredLogProb(a1s,verb,overb)


  def getArg1PredPredLogProb(self, a1s, verb, overb):
    '''
    Wrapper to return Log probability
    '''
    s, cnt = self.getArg1PredPredProb(a1s, verb, overb)

    if cnt == 0:
      return 0

    return self.log(1 - (float(s)/cnt))
    pass

  def getArg1PredPredProb(self, a1s, verb, overb):
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_verb_verb_score:
        continue
      if verb not in self.args1_verb_verb_score[arg1]:
        continue
      if overb in self.args1_verb_verb_score[arg1][verb]:
        s+= self.args1_verb_verb_score[arg1][verb][overb]
      cnt+=1

    return (s, cnt)

  def getArg1PredPredArg1(self, input_a1, predicate, output_predicate, output_arg):
    a1s = input_a1.getNouns()
    overb = self.stemmer.stem(output_predicate.predicate)
    verb = self.stemmer.stem(predicate.predicate)
    # oas = output_arg.getNouns()
    oas = output_predicate.getNouns()
    return self.getArg1PredPredArg1LogProb(a1s, verb, overb, oas)


  def getArg1PredPredArg1LogProb(self, a1s, verb, overb, oas):
    '''
    Wrapper to return Log probability
    '''
    s, cnt = self.getArg1PredPredArg1Prob(a1s, verb, overb, oas)
    if cnt == 0:
      return 0

    return self.log(1 - (float(s)/cnt))
    pass

  def getArg1PredPredArg1Prob(self, a1s, verb, overb, oas):
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_verb_verb_args1_score:
        continue
      if verb not in self.args1_verb_verb_args1_score[arg1]:
        continue
      # if overb not in self.args1_verb_verb_args1_score[arg1][verb]:
      #   continue
      for a in oas:
        arg = self.stemmer.stem(a)
        if overb in self.args1_verb_verb_args1_score[arg1][verb] and arg in self.args1_verb_verb_args1_score[arg1][verb][overb]:
          s+= self.args1_verb_verb_args1_score[arg1][verb][overb][arg]
        cnt+=1

    return (s, cnt)

  def getArg1Arg2PredArg(self, input_a1, input_a2, predicate, output_a):
    a1s = input_a1.getNouns()
    a2s = input_a2.getNouns()
    oas = output_a.getNouns()
    verb = self.stemmer.stem(predicate.predicate)
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_args2_verb_args_score:
        continue
      for a2 in a2s:
        arg2 = self.stemmer.stem(a2)
        if arg2 not in self.args1_args2_verb_args_score[arg1]:
          continue
        if verb not in self.args1_args2_verb_args_score[arg1][arg2]:
          continue
        for o in oas:
          o_arg = self.stemmer.stem(o)
          if o_arg in self.args1_args2_verb_args_score[arg1][arg2][verb]:
            s+= self.args1_args2_verb_args_score[arg1][arg2][verb][o_arg]
          cnt+=1
    if cnt==0:
      return 0
    return self.log(1 - (float(s)/cnt))

  def getArg1Arg2PredPred(self, input_a1, input_a2, predicate, output_predicate):
    a1s = input_a1.getNouns()
    a2s = input_a2.getNouns()
    overb = self.stemmer.stem(output_predicate.predicate)
    verb = self.stemmer.stem(predicate.predicate)
    return self.getArg1Arg2PredPredLogProb(a1s, a2s, verb, overb)

  def getArg1Arg2PredPredLogProb(self, a1s, a2s, verb, overb):
    '''
    Wrapper to return Log probability
    '''
    s, cnt = self.getArg1Arg2PredPredProb(a1s, a2s, verb, overb)

    if cnt == 0:
      return 0

    return self.log(1 - (float(s)/cnt))
    pass

  def getArg1Arg2PredPredProb(self, a1s, a2s, verb, overb):
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_args2_verb_verb_score:
        continue
      for a2 in a2s:
        arg2 = self.stemmer.stem(a2)
        if arg2 not in self.args1_args2_verb_verb_score[arg1]:
          continue
        if verb not in self.args1_args2_verb_verb_score[arg1][arg2]:
          continue
        if overb in self.args1_args2_verb_verb_score[arg1][arg2][verb]:
          s+= self.args1_args2_verb_verb_score[arg1][arg2][verb][overb]
        cnt+=1

    return (s, cnt)

  def getArg1Arg2PredPredArg1(self, input_a1, input_a2, predicate, output_predicate, output_argument):
    a1s = input_a1.getNouns()
    a2s = input_a2.getNouns()
    # oas = output_argument.getNouns()
    oas = output_predicate.getNouns()
    overb = self.stemmer.stem(output_predicate.predicate)
    verb = self.stemmer.stem(predicate.predicate)
    return self.getArg1Arg2PredPredArg1LogProb(a1s, a2s, verb, overb, oas)


  def getArg1Arg2PredPredArg1LogProb(self, a1s, a2s, verb, overb, oas):
    '''
    Wrapper to return Log probability
    '''
    s, cnt = self.getArg1Arg2PredPredArg1Prob(a1s, a2s, verb, overb, oas)

    if cnt == 0:
      return 0

    return self.log(1 - (float(s)/cnt))
    pass

  def getArg1Arg2PredPredArg1Prob(self, a1s, a2s, verb, overb, oas):
    s=0
    cnt=0
    for a1 in a1s:
      arg1 = self.stemmer.stem(a1)
      if arg1 not in self.args1_args2_verb_verb_args1_score:
        continue
      for a2 in a2s:
        arg2 = self.stemmer.stem(a2)
        if arg2 not in self.args1_args2_verb_verb_args1_score[arg1]:
          continue
        if verb not in self.args1_args2_verb_verb_args1_score[arg1][arg2]:
          continue
        # if overb not in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb]:
        #   continue
        for a in oas:
          arg = self.stemmer.stem(a)
          if overb in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb] and arg in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][overb]:
            s+= self.args1_args2_verb_verb_args1_score[arg1][arg2][verb][overb][arg]
          cnt+=1

    return (s, cnt)

  def getPredOuputArgProb(self, predicate, input_argument1, input_argument2, output_argument):
    #Used for Evolution edge weight assignment
    if input_argument1!=None:

      nouns = output_argument.getNouns()
      # if "minutes" in nouns:
      #   return 0
      # score = self.log(1-self.getTextSimArr(predicate.getNouns(), nouns))
      score = self.log(1 - self.getTextSimArr(input_argument1.getNouns(), nouns))
      if score!= 0:
        return score
      # if output_argument.arg_type=="arg1":
      #   score2 = self.getArg1Arg1Prob(input_argument1,output_argument)
      if input_argument2==None:
        score = self.getArg1PredArg(input_argument1,predicate,output_argument)
      else:
        score = self.getArg1Arg2PredArg(input_argument1,input_argument2,predicate,output_argument)

      if score != 0:
        return score

    # Arg1 to Arg1 score
      if input_argument2==None:
        return self.getArg1ArgProb(input_argument1,output_argument)
      else:
        return self.getArg1Arg2ArgProb(input_argument1,input_argument2,output_argument)

  def getPredOuputArg1Prob(self, predicate, input_argument, output_argument):
    ### Compute probability of edge predicate->arg1
    verb = self.stemmer.stem(predicate.predicate)
    if verb in self.verb_args1_score:
      s=0
      d = {}
      # arr = output_argument.argPOS.split()
      arr = output_argument.getNouns()
      for e in arr:
        # arr2 = e.split("/")
        # if "NN" in arr2[1]:
        #   d[self.stemmer.stem(arr2[0])] = 1
        d[self.stemmer.stem(e)] = 1
      if len(d)!=0:
        for arg1 in self.verb_args1_score[verb]:
          if arg1 in d:
            s +=  self.verb_args1_score[verb][arg1]
        return self.log(1 - (float(s)/len(d)))
        # return math.log(1-s+0.00000001)
    return 0

  def getPredOuputArg2Prob(self, predicate, input_argument, output_argument):
    ### Compute probability of edge predicate->arg2
    verb = self.stemmer.stem(predicate.predicate)
    if verb in self.verb_args2_score:
      s=0
      d = {}
      # arr = output_argument.argPOS.split()
      arr = output_argument.getNouns()
      for e in arr:
        # arr2 = e.split("/")
        # if arr2[1]=="NN":
        #   d[self.stemmer.stem(arr2[0])] = 1
        d[self.stemmer.stem(e)] = 1
      if len(d)!=0:
        for arg1 in self.verb_args2_score[verb]:
          if arg1 in d:
            s +=  self.verb_args2_score[verb][arg1]
        return self.log(1 - (float(s)/len(d)))
        # return math.log(1-s+0.00000001)
    return 0

  def getArg1ArgProb(self, input_argument0, input_argument1):
    ### Compute probability of edge predicate->arg2
    args0 = input_argument0.getNouns()
    args1 = input_argument1.getNouns()
    s=0
    cnt=0
    for a0 in args0:
      arg0 = self.stemmer.stem(a0)
      if arg0 in self.args1_args_score:
        for a1 in args1:
          arg1 = self.stemmer.stem(a1)
          if arg1 in self.args1_args_score[arg0]:
            s +=  self.args1_args_score[arg0][arg1]
          cnt += 1
    if cnt==0:
      return 0
    return self.log(1 - (float(s)/cnt))

  def getArg1Arg2ArgProb(self, input_argument1,input_argument2, output_argument):
    ### Compute probability of edge predicate->arg2
    args1 = input_argument1.getNouns()
    args2 = input_argument2.getNouns()
    if len(args2)==0:
      return self.getArg1ArgProb(input_argument1,output_argument)
    oargs = output_argument.getNouns()
    s=0
    cnt=0
    for a1 in args1:
      arg1 = self.stemmer.stem(a1)
      if arg1 in self.args1_args2_args_score:
        for a2 in args2:
          arg2 = self.stemmer.stem(a2)
          if arg2 in self.args1_args2_args_score[arg1]:
            for oa in oargs:
              oarg = self.stemmer.stem(oa)
              if oarg in self.args1_args2_args_score[arg1][arg2]:
                s +=  self.args1_args2_args_score[arg1][arg2][oarg]
              cnt += 1
    if cnt==0:
      return 0
    return self.log(1 - (float(s)/cnt))

  def getArgPredProb(self, arg, pred):
    ### Compute probability of edge predicate->arg2
    args = arg.getNouns()
    verb = self.stemmer.stem(pred.predicate)
    s=0
    cnt=0
    for a in args:
      arg = self.stemmer.stem(a)
      if arg in self.args_verb_score and verb in self.args_verb_score[arg]:
        s +=  self.args_verb_score[arg][verb]
      cnt += 1
    if cnt==0:
      return 0
    return self.log(1 - (float(s)/cnt))

  def getVerbVerbProb(self, predicate, predicate2):
    verb = self.stemmer.stem(predicate.predicate)
    verb2 = self.stemmer.stem(predicate2.predicate)
    if verb not in self.verbs_score:
      return 0
    if verb2 not in self.verbs_score[verb]:
      return 0

    #print '##### ' + self.verbs_score[verb][verb2]
    return self.log(1 - self.verbs_score[verb][verb2])

  def getPredPredProb(self, predicate, input_argument1, input_argument2, predicate2, input2_argument):
    #Implicit arg edge - edge between connected components
    if input_argument1!=None:#all possible assignments if arg1 of verb 1 is present
      score = 0
      if input2_argument!=None:
        if input_argument2==None:
          score = self.getArg1PredPredArg1(input_argument1,predicate,predicate2,input2_argument)
        else:
          score = self.getArg1Arg2PredPredArg1(input_argument1,input_argument2,predicate,predicate2,input2_argument)
        # # Test
        # if True:
        #   return score
        # ####
        if score != 0:
          # return score
          return score-0.0001 # for "bring" -> "add" <- "pasta" example, when "bring" -> "pasta" has the same weight as "bring" -> "add" <- "pasta"
      if input_argument2==None:
        score = self.getArg1PredPred(input_argument1,predicate,predicate2)
      else:
        score = self.getArg1Arg2PredPred(input_argument1,input_argument2,predicate,predicate2)
      # Test
      # if True:
      #   return score
      ####
      if score!=0:
        return score
      # verb = self.stemmer.stem(predicate.predicate)
      # verb2 = self.stemmer.stem(predicate2.predicate)
      # if verb in self.verbs_score and verb2 in self.verbs_score[verb]:
      #   return self.log(1-self.verbs_score[verb][verb2])
      # score += self.getArg2PredProb(input_argument, predicate2)
      # score += self.getArg1Arg1Prob(input_argument,input_argument2)
      score = self.getArgPredProb(input_argument1, predicate2)

      if score!=0:
        return score

    return self.getVerbVerbProb(predicate, predicate2)


    # score2 = self.getArgPredProb(input_argument1, predicate2)
    # return float(score+score2)/2

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
    d1 = Counter(map(lambda k: self.stemmer.stem(k), text1))
    d2 = Counter(map(lambda k: self.stemmer.stem(k), text2))
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


  def printEvolutionProb(self, fileName):
    with open(fileName + '_args1_args2_verb_args_score.csv', 'w') as f:
      for arg1 in self.args1_args2_verb_args_score.keys():
        for arg2 in self.args1_args2_verb_args_score[arg1].keys():
          for verb in self.args1_args2_verb_args_score[arg1][arg2].keys():
            for arg in self.args1_args2_verb_args_score[arg1][arg2][verb].keys():
              f.write(','.join([arg1,arg2,verb ,arg ,str(self.args1_args2_verb_args_score[arg1][arg2][verb][arg])]) + '\n')
      pass

    with open(fileName + '_args1_verb_args_score.csv', 'w') as f:
      for arg1 in self.args1_verb_args_score.keys():
        for verb in self.args1_verb_args_score[arg1].keys():
          for arg in self.args1_verb_args_score[arg1][verb].keys():
            f.write(','.join([arg1, verb, arg, str(self.args1_verb_args_score[arg1][verb][arg])]) + '\n')
      pass

    with open(fileName + '_args1_args2_args_score.csv', 'w') as f:
      for arg1 in self.args1_args2_args_score.keys():
        for arg2 in self.args1_args2_args_score[arg1].keys():
          for arg in self.args1_args2_args_score[arg1][arg2].keys():
            f.write(','.join([arg1, arg2, arg, str(self.args1_args2_args_score[arg1][arg2][arg])]) + '\n')
      pass

    with open(fileName + '_args1_args_score.csv', 'w') as f:
      for arg1 in self.args1_args_score.keys():
        for arg in self.args1_args_score[arg1].keys():
          f.write(','.join([arg1, arg, str(self.args1_args_score[arg1][arg])]) + '\n')
      pass
    pass

  def printImplicitProb(self, fileName):
    with open(fileName + '_args1_verb_verb_args1_score.csv', 'w') as f:
      for arg1 in self.args1_verb_verb_args1_score.keys():
        for verb1 in self.args1_verb_verb_args1_score[arg1].keys():
          for verb2 in self.args1_verb_verb_args1_score[arg1][verb1].keys():
            for oarg1 in self.args1_verb_verb_args1_score[arg1][verb1][verb2].keys():
              f.write( ','.join([arg1, verb1, verb2, oarg1, str(self.args1_verb_verb_args1_score[arg1][verb1][verb2][oarg1])]) + '\n')
      pass

    with open(fileName + '_args1_args2_verb_verb_args1_score.csv', 'w') as f:
      for arg1 in self.args1_args2_verb_verb_args1_score.keys():
        for arg2 in self.args1_args2_verb_verb_args1_score[arg1].keys():
          for verb1 in self.args1_args2_verb_verb_args1_score[arg1][arg2].keys():
            for verb2 in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb1].keys():
              for oarg1 in self.args1_args2_verb_verb_args1_score[arg1][arg2][verb1][verb2].keys():
                f.write( ','.join([arg1, arg2, verb1, verb2, oarg1, str(self.args1_args2_verb_verb_args1_score[arg1][arg2][verb1][verb2][oarg1])]) +'\n')
      pass

    with open(fileName + '_args1_verb_verb_score.csv', 'w') as f:
      for arg1 in self.args1_verb_verb_score.keys():
        for verb1 in self.args1_verb_verb_score[arg1].keys():
          for verb2 in self.args1_verb_verb_score[arg1][verb1].keys():
            f.write(','.join([arg1, verb1, verb2, str(self.args1_verb_verb_score[arg1][verb1][verb2])]) + '\n')
      pass

    with open(fileName + '_args1_args2_verb_verb_score.csv', 'w') as f:
      for arg1 in self.args1_args2_verb_verb_score.keys():
        for arg2 in self.args1_args2_verb_verb_score[arg1].keys():
          for verb1 in self.args1_args2_verb_verb_score[arg1][arg2].keys():
            for verb2 in self.args1_args2_verb_verb_score[arg1][arg2][verb1].keys():
              f.write( ','.join([arg1, arg2, verb1, verb2, str(self.args1_args2_verb_verb_score[arg1][arg2][verb1][verb2])]) +'\n')
      pass

    with open(fileName + '_args_verb_score.csv', 'w') as f:
      for arg1 in self.args_verb_score.keys():
        for verb in self.args_verb_score[arg1].keys():
          f.write(','.join([arg1, verb, str(self.args_verb_score[arg1][verb])]) + '\n')
      pass

    with open(fileName + '_verb_verb_score.csv', 'w') as f:
      for verb in self.verbs_score.keys():
        for verb2 in self.verbs_score[verb].keys():
          f.write(','.join([verb, verb2, str(self.verbs_score[verb][verb2])]) + '\n')
      pass
    pass


