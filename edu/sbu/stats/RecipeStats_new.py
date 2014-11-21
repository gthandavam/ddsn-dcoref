__author__ = 'gt'

from edu.sbu.stats.corpus.reader2 import RecipeReader2
from collections import Counter
import math
from nltk.stem.porter import *
from edu.sbu.shell.semgraph.RNode import RNode
from edu.sbu.shell.semgraph.PNode import PNode

class RecipeStats2:

  def __init__(self):
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

    #implicit arg stat
    self.args1_args2_verb_verb_score = {}
    self.args1_args2_verb_verb_args1_score = {}
    self.args1_verb_verb_score = {}
    self.args1_verb_verb_args1_score = {}

    self.sent_window = 1 #incorrectly being used - so for now setting it to 1

    self.my_max = 0 # in log P space, log(1) == 0 is max
    self.my_min = -100 #setting log(0) to be -100

    pass

  def log(self, val):
    if val==0:
      return self.my_min
    else:
      return math.log(val)

  def computeStat(self, recipe_name):
    self.reader = RecipeReader2(recipe_name)
    self.reader.read()
    self.computeVerbArgSentStat()

  def computeVerbArgSentStat(self):
    cnt = {}
    cnt_arg1 = {}
    cnt_arg2 = {}
    cnt_arg1_arg2_verb = {}
    cnt_arg1_verb = {}

    pass

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

    pass

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
      return self.my_max # no evidence so returning max wt 1-P min wt formulation

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
      return self.my_max

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
      return self.my_max
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
      return self.my_max

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
      return self.my_max

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
        d[self.stemmer.stem(e)] = 1
      if len(d)!=0:
        for arg1 in self.verb_args2_score[verb]:
          if arg1 in d:
            s +=  self.verb_args2_score[verb][arg1]
        return self.log(1 - (float(s)/len(d)))

    return self.my_max

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
      return self.my_max
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
      return self.my_max
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
      return self.my_max
    return self.log(1 - (float(s)/cnt))

  def getVerbVerbProb(self, predicate, predicate2):
    verb = self.stemmer.stem(predicate.predicate)
    verb2 = self.stemmer.stem(predicate2.predicate)
    if verb not in self.verbs_score:
      return self.my_max
    if verb2 not in self.verbs_score[verb]:
      return self.my_max

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

        if score != 0:
          return score-0.0001

      if input_argument2==None:
        score = self.getArg1PredPred(input_argument1,predicate,predicate2)
      else:
        score = self.getArg1Arg2PredPred(input_argument1,input_argument2,predicate,predicate2)
      if score!=0:
        return score

      score = self.getArgPredProb(input_argument1, predicate2)

      if score!=0:
        return score

    return self.getVerbVerbProb(predicate, predicate2)

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
    '''
    Returns score between 0 to 1
    '''
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
    print sum12/math.sqrt(sum1*sum2)
    return sum12/math.sqrt(sum1*sum2)


def get_whole_graph(pnodes_resolved, rnodes_resolved, arbor_edges):
  '''
  Get graph for stat calculation based on the mode of operation CC or arbor

  cc mode operates only on pnodes_resolved and rnodes_resolved
  arbor mode operates on pnodes_resolved, rnodes_resolved and arbor_edges
  '''
  #TODO: add check for cc or arbor mode
  w_g = {}
  for i in xrange(len(pnodes_resolved)):
    for j in xrange(len(pnodes_resolved[i])):
      pred_id = pnodes_resolved[i][j].id
      w_g[pred_id] = {}

      for k in xrange(1,3):
        r_id = rnodes_resolved[i][j][k].id
        #consider only non-null nodes
        if not rnodes_resolved[i][j][k].is_null:
          if not r_id in w_g:
            w_g[r_id] = {}

          w_g[r_id][pred_id] = 1 #adjacency matrix

          #update evolution edge
          if(len(rnodes_resolved[i][j][k].shell_coref) > 0):
            x,y = rnodes_resolved[i][j][k].shell_coref[0][0]
            p1_id = pnodes_resolved[x][y].id
            if not p1_id in w_g:
              w_g[p1_id] = {}

            w_g[p1_id][r_id] = 1 #adjacency matrix

        elif (len(rnodes_resolved[i][j][k].shell_coref) > 0):
          #implicit edge
          x,y = rnodes_resolved[i][j][k].shell_coref[0][0]
          p1_id = pnodes_resolved[x][y].id
          if not p1_id in w_g:
            w_g[p1_id] = {}

          w_g[p1_id][pred_id] = 1 #adjacency matrix

      pass

  for n1 in arbor_edges:
    for n2 in arbor_edges[n1]:
      if not n1 in w_g:
        w_g[n1] = {}

      w_g[n1][n2] = 1

  w_g = get_transitive_closure(w_g)

  return w_g
  pass

#public static method
def get_transitive_closure(g):
  '''
  g is assumed to have dictionary representation of graph
  so to find vertices get all distinct nodes via set operation on the graph
  warshall's transitive closure algorithm
  '''
  vertices = set(g.keys())

  ret_g = {}

  for key in g.keys():
    vertices = vertices.union(set(g[key].keys()))

  vertices = list(vertices)

  for vertex in vertices:
    for vertex2 in vertices:
      if not vertex in ret_g:
        ret_g[vertex] = {}

      if vertex in g and vertex2 in g[vertex]:
        ret_g[vertex][vertex2] = 1
      else:
        ret_g[vertex][vertex2] = 0

  for k in xrange(len(vertices)):
    for i in xrange(len(vertices)):
      for j in xrange(len(vertices)):
        if ret_g[vertices[i]][vertices[j]] == 0 and ret_g[vertices[i]][vertices[k]] !=0 and ret_g[vertices[k]][vertices[j]] != 0:
          ret_g[vertices[i]][vertices[j]] = ret_g[vertices[i]][vertices[k]] + ret_g[vertices[k]][vertices[j]]

  return ret_g
