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

#counting predicate distribution for the entire corpus
pred_count = {}


#counting recipes having N predicates
recipes_with_N_predicates = {}

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

def update_recipes_with_N_predicates(dish):
  global recipes_with_N_predicates

  reader = RecipeReader2(dish)

  for recipe_index in xrange(len(reader.recipe_verbs)):
    cnt = 0
    for sent_index in xrange(len(reader.recipe_verbs[recipe_index])):
      for verb_index in xrange(len(reader.recipe_verbs[recipe_index][sent_index])):
        cnt += 1

    if cnt in recipes_with_N_predicates:
      recipes_with_N_predicates[cnt] += 1
    else:
      recipes_with_N_predicates[cnt] = 1

  pass

def write_csv():
  with open('number_of_predicates_dist.csv', 'w') as f:
    f.write('No of Predicates, No of Recipes\n')
    for key in recipes_with_N_predicates:
      f.write(str(key) +',' + str(recipes_with_N_predicates[key]) + '\n')

def main():
  for dish in dishes:
    update_recipes_with_N_predicates(dish)

  write_csv()
  pass

if __name__ == '__main__':
  main()