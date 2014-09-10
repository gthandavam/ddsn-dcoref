__author__ = 'gt'
import pickle
from nltk.stem.porter import PorterStemmer

class StatFeatures:
  def __init__(self, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4):
    self.stat_file = '/home/gt/Documents/' + recipeName + '/' + stat_type + '/RecipeStats2_forEval.pickle'
    self.cp0 = cp0
    self.cp1 = cp1
    self.cp2 = cp2
    self.cp3 = cp3
    self.cp4 = cp4

    with open(self.stat_file) as f:
      self.recipe_stat = pickle.load(f)

    self.nounPOS = ['NN', 'NNS', 'NNPS', 'NNP']
    self.stemmer = PorterStemmer()

  def getNouns(self, txt, txtPOS):
    ret = []

    if txt is None or txt == 'NULL':
      return ret

    txt = txt.split()
    txtPOS = txtPOS.split()

    for i in xrange(len(txt)):
      if txtPOS[i].split('/')[-1] in self.nounPOS:
        ret.append(txt[i])

    return ret

  def process_sem_group(self, sem_group):
    ret = {}
    ret['pred'] = self.stemmer.stem(sem_group['pred'])
    ret['arg1'] = self.getNouns(sem_group['arg1'], sem_group['arg1POS'])
    ret['arg2'] = self.getNouns(sem_group['arg2'], sem_group['arg2POS'])
    return ret
    pass

  '''
  getArg1Arg2PredPredArg1Prob(a1s, a2s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)
  getArg1Arg2PredPredProb(a1s, a2s, verb, overb) returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
  getArg1PredPredArg1Prob(a1s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
  getArg1PredPredProb(a1s, verb, overb) returns P(pred2 | pred1.arg1, pred1)
  '''

  def getArg1Arg2PredPredArg1LogProb(self, sem_group1, sem_group2):
    '''returns P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)
    '''
    sem_group1 = self.process_sem_group(sem_group1)
    sem_group2 = self.process_sem_group(sem_group2)
    prob = self.recipe_stat.getArg1Arg2PredPredArg1LogProb(sem_group1['arg1'], sem_group1['arg2'], sem_group1['pred'], sem_group2['pred'], sem_group2['arg1'])

    return prob
    pass

  def getArg1Arg2PredPredLogProb(self, sem_group1, sem_group2):
    '''returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
    '''
    sem_group1 = self.process_sem_group(sem_group1)
    sem_group2 = self.process_sem_group(sem_group2)
    prob = self.recipe_stat.getArg1Arg2PredPredLogProb(sem_group1['arg1'], sem_group1['arg2'], sem_group1['pred'], sem_group2['pred'])

    return prob

  def getArg1PredPredArg1LogProb(self, sem_group1, sem_group2):
    '''returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
    '''
    sem_group1 = self.process_sem_group(sem_group1)
    sem_group2 = self.process_sem_group(sem_group2)
    prob = self.recipe_stat.getArg1PredPredArg1LogProb(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'], sem_group2['arg1'])

    pass

    return prob

  def getArg1PredPredLogProb(self, sem_group1, sem_group2):
    '''returns P(pred2 | pred1.arg1, pred1)
    '''
    sem_group1 = self.process_sem_group(sem_group1)
    sem_group2 = self.process_sem_group(sem_group2)
    prob = self.recipe_stat.getArg1PredPredLogProb(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'])


    return prob

  def get_statistics(self):
    with open(self.stat_file) as f:
      recipe_stat1 = pickle.load(f)
      print recipe_stat1

    pass

  def print_probability(self, sem_group1, sem_group2):
    self.getArg1Arg2PredPredArg1LogProb(sem_group1, sem_group2)
    self.getArg1Arg2PredPredLogProb(sem_group1, sem_group2)
    self.getArg1PredPredArg1LogProb(sem_group1, sem_group2)
    self.getArg1PredPredLogProb(sem_group1, sem_group2)

  def get_prob_features(self, sem_group1, sem_group2):
    ret = []
    #CP4
    if self.cp4:
      s1p = self.getArg1PredPredLogProb(sem_group1, sem_group2)
      s2p = self.getArg1PredPredLogProb(sem_group2, sem_group1)

      ret.extend(self.boolean_feature_encoding(s1p, s2p))

    #CP3
    if self.cp3:
      s1p = self.getArg1PredPredArg1LogProb(sem_group1, sem_group2)
      s2p = self.getArg1PredPredArg1LogProb(sem_group2, sem_group1)

      ret.extend(self.boolean_feature_encoding(s1p, s2p))

    #CP2
    if self.cp2:
      s1p = self.getArg1Arg2PredPredLogProb(sem_group1, sem_group2)
      s2p = self.getArg1Arg2PredPredLogProb(sem_group2, sem_group1)

      ret.extend(self.boolean_feature_encoding(s1p, s2p))

    #CP1
    if self.cp1:
      s1p = self.getArg1Arg2PredPredArg1LogProb(sem_group1, sem_group2)
      s2p = self.getArg1Arg2PredPredArg1LogProb(sem_group2, sem_group1)

      ret.extend(self.boolean_feature_encoding(s1p, s2p))

    #TODO: add for cp0 verb verb probability

    return ret

    pass

  def boolean_feature_encoding(self, s1p, s2p):
    '''
    feature encoding for precedence relation
      one feature to reflect the decision taken,
      one feature to indicate the confidence of the decision

      0 0 precedence false, confidence false
      0 1 precedence false, confidence true
      1 0 NOT POSSIBLE
      1 1 precedence true, confidence true
    '''
    ret = []
    print s1p, s2p
    if( s1p == -100 ):
      if( s2p == -100 ):
        ret.append(0) #decision
        ret.append(0) #decided vs undecided
      else:
        ret.append(0) #decision
        ret.append(1) #decided vs undecided
    else:
      if( s2p == -100):
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


if __name__ == '__main__':
  stats = StatFeatures('MacAndCheese')
  stats.get_statistics()
  pass