__author__ = 'gt'

from edu.sbu.stats.corpus.reader2 import RecipeReader2
import os
from nltk import word_tokenize
from nltk.tag.stanford import POSTagger

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


def get_all_verbs(dish, all_verbs, posTagger):

  global pred_count

  steps = '/home/gt/Documents/' + dish + '/' + dish + '-Isteps/'

  recipes = os.listdir(steps)

  for recipe in recipes:
    with open(steps + recipe) as f:
      text = ''
      for line in f.readlines():
        line = line.lower()
        text += line
        text += '\n'


      tokens = word_tokenize(text)

      tags = posTagger.tag(tokens)

      # print tags

      for tag in tags:
        if tag[1] in ('VB', 'VBP'):
          if tag[0] in pred_count:
            pred_count[tag[0]] += 1
          else:
            pred_count[tag[0]] = 1

          all_verbs.append(tag[0])



  pass

def get_all_verbs_tregex(dish, all_verbs):
  pass

def main():
  # for dish in dishes:
  #   update_recipes_with_N_predicates(dish)
  #
  # write_csv()
  all_verbs = []

  posTagger = POSTagger('/home/gt/Downloads/stanford-postagger-2014-01-04/models/english-left3words-distsim.tagger', '/home/gt/Downloads/stanford-postagger-2014-01-04/stanford-postagger-3.3.1.jar')

  for dish in dishes:
    get_all_verbs(dish, all_verbs, posTagger)

  with open('verb_cloud_input_I_would_word_tokenize', 'w') as f:
    for verb in all_verbs:
      f.write(' ' + verb)

  with open('all_pred_dist_I_would_word_tokenize.csv', 'w') as f:
    f.write('predicate,count\n')
    for key in pred_count:
      f.write(key + ',' + str(pred_count[key]) + '\n')

  print len(all_verbs)

  pass

if __name__ == '__main__':
  main()