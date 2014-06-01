__author__ = 'gt'
import pickle
from nltk.stem.porter import PorterStemmer
stat_file = '/home/gt/Documents/RecipeStats2_forEval.pickle'

from edu.sbu.stats.RecipeStats2 import RecipeStats2

with open(stat_file) as f:
  recipe_stat = pickle.load(f)

nounPOS = ['NN', 'NNS', 'NNP', 'NP']
stemmer = PorterStemmer()
def getNouns(txt, txtPOS):
  ret = []

  txt = txt.split()
  txtPOS = txtPOS.split()

  for i in len(txt):
    if txtPOS[i] in nounPOS:
      ret.append(stemmer(txt[i]))

  return ret

def process_sem_group(sem_group):

  sem_group['pred'] = stemmer.stem(sem_group['pred'])
  sem_group['arg1'] = getNouns(sem_group['arg1'], sem_group['arg1POS'])
  sem_group['arg2'] = getNouns(sem_group['arg2'], sem_group['arg2POS'])
  return sem_group
  pass

'''
getArg1Arg2PredPredArg1Prob(a1s, a2s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)
getArg1Arg2PredPredProb(a1s, a2s, verb, overb) returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
getArg1PredPredArg1Prob(a1s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
getArg1PredPredProb(a1s, verb, overb) returns P(pred2 | pred1.arg1, pred1)
'''


def getArg1Arg2PredPredArg1Prob(sem_group1, sem_group2):
  '''returns P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1Arg2PredPredArg1Prob(sem_group1['arg1'], sem_group1['arg2'], sem_group1['pred'], sem_group2['pred'], sem_group2['arg1'])
  if not prob is None:
    print prob
  pass

def getArg1Arg2PredPredProb(sem_group1, sem_group2):
  '''returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1Arg2PredPredProb(sem_group1['arg1'], sem_group1['arg2'], sem_group1['pred'], sem_group2['pred'])
  if not prob is None:
    print prob
  pass

def getArg1PredPredArg1Prob(sem_group1, sem_group2):
  '''returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1PredPredArg1Prob(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'], sem_group2['arg1'])
  if not prob is None:
    print prob
  pass

def getArg1PredPredProb(sem_group1, sem_group2):
  '''returns P(pred2 | pred1.arg1, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1PredPredProb(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'])
  if not prob is None:
    print prob
  pass

def get_statistics():
  with open(stat_file) as f:
    recipe_stat1 = pickle.load(f)
    print recipe_stat1

  pass

if __name__ == '__main__':
  get_statistics()
  pass