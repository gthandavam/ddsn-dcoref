__author__ = 'gt'

from edu.sbu.stats.corpus.reader2 import RecipeReader2

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

pred_count = {}

def update_count(dish):
  global pred_count
  reader = RecipeReader2(dish)

  for recipe_index in xrange(len(reader.recipe_verbs)):
    for sent_index in xrange(len(reader.recipe_verbs[recipe_index])):
      for verb_index in xrange(len(reader.recipe_verbs[recipe_index][sent_index])):
        if reader.recipe_verbs[recipe_index][sent_index][verb_index] in pred_count:
          pred_count[reader.recipe_verbs[recipe_index][sent_index][verb_index]] += 1
        else:
          pred_count[reader.recipe_verbs[recipe_index][sent_index][verb_index]] = 1

  pass

def write_csv():
  with open('pred_dist.csv', 'w') as f:
    f.write('predicate,count\n')
    for key in pred_count.keys():
      f.write(key +',' + str(pred_count[key]) + '\n')

def main():
  for dish in dishes:
    update_count(dish)

  write_csv()
  pass

if __name__ == '__main__':
  main()