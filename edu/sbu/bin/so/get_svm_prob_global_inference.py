__author__ = 'gt'

from sklearn.externals import joblib

from edu.sbu.eval.so.tsp.tsp_adapter.tsp_instance import get_best_order
from edu.sbu.eval.so.svm.ml_framework import update_global_accuracy
from scipy.stats.mstats import kendalltau as ktau_m

dishes = (
'BananaMuffins',
'BeefChilli',
'BeefMeatLoaf',
'BeefStroganoff',
'CarrotCake',
'CheeseBurger',
'ChickenSalad',
'ChickenStirFry',
'Coleslaw',
'CornChowder',
'DeviledEggs',
'EggNoodles',
'FrenchToast',
'MacAndCheese',
'MeatLasagna',
'PecanPie',
'PotatoSalad',
'PulledPork',
'PumpkinPie',
'VeggiePizza'
)

archive = '/home/gt/Documents/AllRecipes-Exp1/'
def main():
  for dish in dishes:
    root = archive + dish + '_'
    weights = joblib.load(root + 'weights.pkl')
    pred_labels = joblib.load(root + 'pred_labels.pkl')
    pairs = joblib.load(root + 'pairs.pkl')
    recipeLength = joblib.load(root + 'recipeLength.pkl')

    prevItr = 0

    ktauSum = 0.0
    tspResultSet = []
    global_inf_labels = 0
    global_inf_correct = 0

    for i in xrange(len(recipeLength)):
      itr = recipeLength[i][1]
      order = get_best_order(weights[prevItr : prevItr + itr ], pred_labels[prevItr : prevItr + itr ], pairs[prevItr: prevItr + itr], recipeLength[i][0])
      global_inf_correct, global_inf_labels = update_global_accuracy(order, global_inf_correct, global_inf_labels)
      ktau_calc = ktau_m(range(recipeLength[i][0]), order, True, False)
      ktauSum += ktau_calc[0]
      tspResultSet.append(order)




  pass

if __name__ == '__main__':
  main()