__author__ = 'gt'
import pickle
from nltk.stem.porter import PorterStemmer

from edu.sbu.shell.Transformer import recipeName



stat_file = '/home/gt/Documents/' + recipeName + '/RecipeStats2_forEval.pickle'

with open(stat_file) as f:
  recipe_stat = pickle.load(f)

nounPOS = ['NN', 'NNS', 'NNPS', 'NNP']
stemmer = PorterStemmer()
def getNouns(txt, txtPOS):
  ret = []

  if txt is None or txt == 'NULL':
    return ret

  txt = txt.split()
  txtPOS = txtPOS.split()

  for i in xrange(len(txt)):
    if txtPOS[i].split('/')[-1] in nounPOS:
      ret.append(txt[i])

  return ret

def process_sem_group(sem_group):
  ret = {}
  ret['pred'] = stemmer.stem(sem_group['pred'])
  ret['arg1'] = getNouns(sem_group['arg1'], sem_group['arg1POS'])
  ret['arg2'] = getNouns(sem_group['arg2'], sem_group['arg2POS'])
  return ret
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
  # print 'P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)'
  # if not prob is None:
  #   print 1000.0 * prob
  # else:
  #   print 'None'

  return -1000.0 * prob
  pass

def getArg1Arg2PredPredProb(sem_group1, sem_group2):
  '''returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1Arg2PredPredProb(sem_group1['arg1'], sem_group1['arg2'], sem_group1['pred'], sem_group2['pred'])

  # print 'P(pred2 | pred1.arg1, pred1.arg2, pred1)'
  #
  # if not prob is None:
  #   print 1000.0 * prob
  # else:
  #   print 'None'
  # pass
  return -1000.0 * prob

def getArg1PredPredArg1Prob(sem_group1, sem_group2):
  '''returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1PredPredArg1Prob(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'], sem_group2['arg1'])

  # print 'P(pred2, pred2.arg1 | pred1.arg1, pred1)'
  #
  # if not prob is None:
  #   print 1000.0 * prob
  # else:
  #   print 'None'
  pass

  return -1000.0 * prob

def getArg1PredPredProb(sem_group1, sem_group2):
  '''returns P(pred2 | pred1.arg1, pred1)
  '''
  sem_group1 = process_sem_group(sem_group1)
  sem_group2 = process_sem_group(sem_group2)
  prob = recipe_stat.getArg1PredPredProb(sem_group1['arg1'], sem_group1['pred'], sem_group2['pred'])

  # print 'P(pred2 | pred1.arg1, pred1)'
  #
  # if not prob is None:
  #   print 1000.0 * prob
  # else:
  #   print 'None'
  # pass

  return -1000.0 * prob

def get_statistics():
  with open(stat_file) as f:
    recipe_stat1 = pickle.load(f)
    print recipe_stat1

  pass

def print_probability(sem_group1, sem_group2):
  getArg1Arg2PredPredArg1Prob(sem_group1, sem_group2)
  getArg1Arg2PredPredProb(sem_group1, sem_group2)
  getArg1PredPredArg1Prob(sem_group1, sem_group2)
  getArg1PredPredProb(sem_group1, sem_group2)

if __name__ == '__main__':
  get_statistics()
  pass