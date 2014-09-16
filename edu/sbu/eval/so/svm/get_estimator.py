__author__ = 'gt'


from edu.sbu.eval.so.data.prepare_data import *

from edu.sbu.eval.so.features.ft_extraction import get_features
from sklearn import svm

def getBestEstimator(X, labels, recipeName):
  # from sklearn.preprocessing import Scaler
  import numpy as np
  from sklearn.grid_search import GridSearchCV
  from sklearn.cross_validation import StratifiedKFold

  # scaler = Scaler()
  # X = scaler.fit_transform(X)

  C_range = 10. ** np.arange(-5, 2)
  # gamma_range = 10. ** np.arange(-5, 4)

  # param_grid = dict(gamma=gamma_range, C=C_range)
  param_grid = dict(C=C_range)
  grid = GridSearchCV(svm.SVC(kernel='linear', cache_size=2000), param_grid=param_grid, cv=StratifiedKFold(y=labels, n_folds=5))

  grid.fit(X, labels)

  print("The best classifier  " + recipeName + " is:\n", grid.best_estimator_)



def findEstimator(ft_extractor, scaler, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4, indicator):
  # ft_extractor = joblib.load(ft_extractor_file)
  # scaler = joblib.load(scaler_file)

  sents_train, labels_train, pairs, recipeLength = get_tsp_train_data(recipeName)
  sents_test, labels_test, pairs, recipeLength = get_tsp_test_data(recipeName)
  sents_val, labels_val, pairs, recipeLength = get_tsp_validation_data(recipeName)

  sents = []
  sents.extend(sents_train)
  sents.extend(sents_val)
  sents.extend(sents_test)
  labels = []
  labels.extend(labels_train)
  labels.extend(labels_val)
  labels.extend(labels_test)

  ft_extractor, scaler, X = get_features(sents, ft_extractor, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4, scaler, indicator)

  getBestEstimator(X,labels,recipeName)


def main(i, recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logFile, indicator):

  findEstimator(1, 1, recipeName, stat_type, cp0, cp1, cp2, cp3, cp4, indicator)
  # test_tsp_solver([[0, 1, 100, 200], [100, 0, 1000, 1], [100, 1000, 0, 200], [100, 100, 2, 0]])
  pass


if __name__ == '__main__':
  import time
  import sys

  if(len(sys.argv) != 9):
    print 'ml_framework.py <recipe_name> <stat_type> <cp0 - 0/1> <cp1 - 0/1> <cp2 - 0/1> <cp3 - 0/1> <cp4 - 0/1> <indicator - 0/1> \n stat_type is one of arbor, arbor_trans, cc, text_order'
    exit(1)

  recipeName = sys.argv[1]
  stat_type = sys.argv[2]

  cp0 = False if sys.argv[3] == '0' else True
  cp1 = False if sys.argv[4] == '0' else True
  cp2 = False if sys.argv[5] == '0' else True
  cp3 = False if sys.argv[6] == '0' else True
  cp4 = False if sys.argv[7] == '0' else True
  indicator = False if sys.argv[8] == '0' else True

  expName = recipeName + '_UGBG_CP_'
  expName = expName + '0' if cp0 else expName
  expName = expName + '1' if cp1 else expName
  expName = expName + '2' if cp2 else expName
  expName = expName + '3' if cp3 else expName
  expName = expName + '4' if cp4 else expName
  expName = expName + '_indicator_' if indicator else expName + '_prob_wt_'

  expName += stat_type

  logFile = '/home/gt/Documents/' + recipeName + '/' + expName + '.out'
  start_time = time.time()
  for i in range(1):
    main(i, recipeName, expName, stat_type, cp0, cp1, cp2, cp3, cp4, logFile, indicator)
  print time.time() - start_time, "seconds"
  print '#############'
