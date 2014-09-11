__author__ = 'gt'

# from gt.sbu.so.data \
#   import get_training_data, get_validation_data, get_tsp_test_data
#
# import sys,os.path
#
# sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))


from edu.sbu.eval.so.data.prepare_data import *

from edu.sbu.eval.so.features.ft_extraction import get_features
from scipy.stats import kendalltau as ktau
from scipy.stats.mstats import kendalltau as ktau_m
from sklearn import svm
from sklearn.externals import joblib
from pprint import pprint
import math
import edu.sbu.eval.so.tsp.tsp_adapter.tsp_instance as tsp

def train(sents, labels, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4):
  ft_extractor,scaler, X = get_features(sents, 1, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4)

  print 'Features extracted'
  clf = svm.SVC(C=1.0, cache_size=2000, class_weight=None, coef0=0.0, degree=3, gamma=0.0,
      kernel='linear', max_iter=-1, probability=True, random_state=None,
      shrinking=True, tol=0.001, verbose=False)

  clf.fit(X,labels)
  # print ft_extractor.get_feature_names()
  return ft_extractor,scaler,clf

def getBestEstimator(X, labels):
  # from sklearn.preprocessing import Scaler
  import numpy as np
  from sklearn.grid_search import GridSearchCV
  from sklearn.cross_validation import StratifiedKFold

  # scaler = Scaler()
  # X = scaler.fit_transform(X)

  C_range = 10. ** np.arange(-4, 6)
  # gamma_range = 10. ** np.arange(-5, 4)

  # param_grid = dict(gamma=gamma_range, C=C_range)
  param_grid = dict(C=C_range)
  grid = GridSearchCV(svm.SVC(kernel='linear'), param_grid=param_grid, cv=StratifiedKFold(y=labels, k=5))

  grid.fit(X, labels)

  print("The best classifier is: ", grid.best_estimator_)


def test(sents, ft_extractor, scaler, clf, labels, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4):
  if len(sents) <= 1:
    print 'here'

  vec,scaler, X = get_features(sents, ft_extractor, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4, scaler)

  y = clf.predict(X)
  prob = clf.predict_proba(X)

  # return y
  return prob,y

def evaluate(observed, expected, test_sents, logF):

  if len(observed) != len(expected):
    raise 'Number of observations != Number of experiments'

  ctr = 0
  tpr = 0
  fpr = 0

  for i in range(len(observed)):
    # if observed[i] != expected[i]:
      # print '************'
      # print 'expected ' + str(expected[i])
      # print test_sents[i].split(blockSeparator)[0]
      # print test_sents[i].split(blockSeparator)[1]
      # print '************'
    if observed[i] != expected[i] and observed[i] == '+':
      fpr += 1
    if observed[i] == expected[i]:
      if(observed[i] == '+'):
        tpr +=1
      ctr+=1

  tpr = tpr * 1.0
  fpr = fpr * 1.0
  tpr = tpr / (len([x for x in expected if x == '+']))
  fpr = fpr / (len([x for x in expected if x == '-']))
  # print "TPR " + str(tpr)
  logF.write("TPR " + str(tpr) + "\n")
  # print "FPR " + str(fpr)
  logF.write("FPR " + str(fpr) + "\n")
  # print "Observed + " + str(len([x for x in observed if x == '+']))
  logF.write("Observed + " + str(len([x for x in observed if x == '+'])) + "\n")
  # print "Observed - " + str(len([x for x in observed if x == '-']))
  logF.write("Observed - " + str(len([x for x in observed if x == '-'])) + "\n")
  return ctr


#
# def run_classifier():
#   # print 'getting training data...'
#   sents, labels = get_training_data()
#   # pprint(sents)
#   # pprint(labels)
#   print 'Training set size ' + str(len(labels))
#
#   # print 'training on the data...'
#   ft_xtractor, clf = train(sents, labels)
#
#   print 'number of features: ' + str(len(ft_xtractor.get_feature_names()))
#
#   # print 'getting test data...'
#   valid_sents, expected_labels = get_validation_data()
#   # pprint(test_sents)
#   # pprint(expected_labels)
#   print 'Testing set size ' + str(len(expected_labels))
#
#   # print 'using the model to predict...'
#   pred_labels = test(valid_sents, ft_xtractor, clf)
#   correct = evaluate(pred_labels, expected_labels)
#
#   print 'prediction accuracy...'
#   print str( (correct * 100.0) / len(expected_labels))
#



def findEstimator(ft_extractor_file, scaler_file, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4):

  ft_extractor = joblib.load(ft_extractor_file)
  scaler = joblib.load(scaler_file)

  sents, labels, pairs, recipeLength = get_tsp_validation_data(recipeName)

  ft_extractor, X = get_features(sents, ft_extractor, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4, scaler)

  getBestEstimator(X,labels)

def train_and_save(recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logF):
  # print 'getting training data...'
  sents, labels, pairs, recipeLength = get_tsp_train_data(recipeName)
  # pprint(sents)
  # pprint(labels)
  print 'Training set size ' + str(len(labels))

  print 'training on the data...'
  ft_xtractor, scaler, clf = train(sents, labels, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4)

  print 'number of features: ' + str(len(ft_xtractor.get_feature_names()))
  # joblib.dump(ft_xtractor, 'models/fx_UB_TrainD_notag.pkl')
  # joblib.dump(clf, 'models/clf_UB_TrainD_notag.pkl')
  #
  joblib.dump(ft_xtractor, 'models/ft_scale_' + recipeName + '_' + expName + '.pkl')
  joblib.dump(clf, 'models/clf_scale_' + recipeName + '_' + expName + '.pkl')
  joblib.dump(scaler, 'models/scaler_' + recipeName + '_' + expName + '.pkl')

def load_and_validate(ft_ext_file, scaler_file, clf_file, recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logF):

  ft_xtractor = joblib.load(ft_ext_file)
  clf = joblib.load(clf_file)
  scaler = joblib.load(scaler_file)

  # print 'getting test data...'
  #valid_sents, expected_labels = get_test_data()

  # sents, labels, pairs, recipeLength = get_tsp_validation_data()
  sents, labels, pairs, recipeLength = get_tsp_test_data(recipeName)

  #Experiment 1 : SVM prediction using different features
  weights, pred_labels = test(sents, ft_xtractor, scaler, clf, labels, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4)

  correct = evaluate(pred_labels, labels, sents, logF)

  # print 'prediction accuracy...'
  logF.write('prediction accuracy...' + '\n')
  # print str((correct * 100.0) / len(labels))
  logF.write(str((correct * 100.0) / len(labels)) + '\n')

  stats_obj = StatFeatures(recipeName, stat_type, cp0, cp1, cp2, cp3, cp4)

  prevItr = 0

  #### SVM prob formulation
  tspResultSet = []
  ktauSum = 0.0
  global_inf_correct = 0
  global_inf_labels = 0

  #### stat prob formulation
  tspResultSet_cp = []
  ktauSum_cp = 0.0
  global_inf_correct_cp = 0
  global_inf_labels_cp = 0

  for i in xrange(len(recipeLength)):
    itr = recipeLength[i][1]
    test_sents = sents[prevItr: prevItr + itr-1]
    # print 'Recipe No ' + str(i+1)
    # print 'Testing set size ' + str(itr)
    # print 'Number of nodes ' + str(recipeLength[i][0])

    if recipeLength[i][0] > 20:
      # print 'Skipping >20 Recipe No ' + str(i + 1)
      logF.write('Skipping >20 Recipe No ' + str(i + 1) + '\n')
      tspResultSet.append([])
      prevItr += itr
      continue

    if len(test_sents) <= 1:
      # print 'Skipping Recipe No ' + str(i + 1)
      logF.write('Skipping Recipe No ' + str(i + 1) + '\n')
      tspResultSet.append([])
      prevItr += itr
      continue

    #Experiment 2 : TSP formulation with SVM probability weights
    edge_weights = tsp.pick_edge_weights(weights[prevItr : prevItr + itr -1], pred_labels[prevItr : prevItr + itr -1], pairs[prevItr: prevItr + itr-1], recipeLength[i][0])
    # # print 'Ordering for Recipe No ' + str(i+1) + ' is '
    # pprint(edge_weights)
    order = test_tsp_solver(edge_weights)

    #Experiment 3 : TSP formulation with stat weights
    edge_weights_cp = tsp.pick_stat_edge_weights(test_sents, pairs[prevItr : prevItr + itr -1], recipeLength[i][0], stats_obj)

    order_cp = test_tsp_solver(edge_weights_cp)


    #Updating for Experiment 2
    global_inf_correct, global_inf_labels = update_global_accuracy(order, global_inf_correct, global_inf_labels)
    ktau_calc = ktau_m(range(recipeLength[i][0]), order, True, False)
    ktauSum += ktau_calc[0]
    tspResultSet.append(order)

    #Updating for Experiment 3
    global_inf_correct_cp, global_inf_labels_cp = update_global_accuracy(order_cp, global_inf_correct_cp, global_inf_labels_cp)
    ktau_calc_cp = ktau_m(range(recipeLength[i][0]), order_cp, True, False)
    ktauSum_cp += ktau_calc_cp[0]
    tspResultSet_cp.append(order_cp)

    prevItr += itr

  import pickle

  with open('results/' + recipeName + '_' + expName + '.pkl', 'w') as f:
    pickle.dump(tspResultSet, f)

  with open('results/cp_' + recipeName + '_' + expName + '.pkl', 'w') as f:
    pickle.dump(tspResultSet_cp, f)

  #log results for Exp 2
  logF.write('Average KTau: ' + str(ktauSum/len(recipeLength)) + '\n')
  logF.write('global inference prediction accuracy...')
  logF.write(str((global_inf_correct * 100.0) / global_inf_labels) + '\n')

  #log results for Exp 3
  logF.write('Average KTau_cp: ' + str(ktauSum_cp/len(recipeLength)) + '\n')
  logF.write('global inference prediction accuracy...')
  logF.write(str((global_inf_correct_cp * 100.0) / global_inf_labels_cp) + '\n')

  if(len(labels) != global_inf_labels):
    # print 'global_inf_labels suspicious'
    logF.write('len of global_inf_labels != len of labels')


def update_global_accuracy(order, correct, total):
  for i in xrange(len(order)):
    for j in xrange(i+1, len(order)):
      total += 1
      if order[i] < order[j]:
        correct += 1
      if order[i] == order[j]:
        print 'Order_i cannot be equal to Order_j'
      pass

  return correct, total
  pass

def test_tsp_solver(distances):
  '''
  distances -> adjacency matrix
  '''

  # input = tsp.prepare_tsp_solver_input(distances)
  output = tsp.tsp_dyn_solver(distances)

  print 'solution'
  pprint(output)
  return output

def main(i, recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logFile):
  # run_classifier()
  with open(logFile, 'w') as logF:
    if i == 0:
       train_and_save(recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logF)
    load_and_validate('models/ft_scale_' + recipeName + '_' + expName + '.pkl', 'models/scaler_' + recipeName + '_' + expName + '.pkl', 'models/clf_scale_' + recipeName + '_' + expName + '.pkl', recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logF)


  # findEstimator('models/ft_noscale_' + recipeName + '_' + expName + '.pkl', recipeName, stat_type, cp0, cp1, cp2, cp3, cp4)
  # test_tsp_solver([[0, 1, 100, 200], [100, 0, 1000, 1], [100, 1000, 0, 200], [100, 100, 2, 0]])
  pass


if __name__ == '__main__':
  import time
  import sys

  if(len(sys.argv) != 8):
    print 'ml_framework.py <recipe_name> <stat_type> <cp0 - 0/1> <cp1 - 0/1> <cp2 - 0/1> <cp3 - 0/1> <cp4 - 0/1>\n stat_type is one of arbor, arbor_trans, cc, text_order'
    exit(1)

  recipeName = sys.argv[1]
  stat_type = sys.argv[2]

  cp0 = False if sys.argv[3] == '0' else True
  cp1 = False if sys.argv[4] == '0' else True
  cp2 = False if sys.argv[5] == '0' else True
  cp3 = False if sys.argv[6] == '0' else True
  cp4 = False if sys.argv[7] == '0' else True

  expName = recipeName + '_UGBG_CP_'
  expName = expName + '0' if cp0 else expName
  expName = expName + '1' if cp1 else expName
  expName = expName + '2' if cp2 else expName
  expName = expName + '3' if cp3 else expName
  expName = expName + '4' if cp4 else expName

  expName += stat_type

  logFile = '/home/gt/Documents/' + recipeName + '/' + expName + '.out'
  start_time = time.time()
  for i in range(1):
    main(i, recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logFile)
  print time.time() - start_time, "seconds"
  print '#############'
