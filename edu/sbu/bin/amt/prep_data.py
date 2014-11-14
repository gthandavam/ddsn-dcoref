__author__ = 'gt'

import os

from nltk.tag.stanford import POSTagger
from nltk import wordpunct_tokenize
import csv

dishes = (
# 'BananaMuffins',
# 'BeefChilli',
# 'BeefMeatLoaf',
# 'BeefStroganoff',
# 'CarrotCake',
# 'CheeseBurger',
# 'ChickenSalad',
# 'ChickenStirFry',
# 'Coleslaw',
# 'CornChowder',
# 'DeviledEggs',
# 'EggNoodles',
# 'FrenchToast',
'MacAndCheese',
# 'MeatLasagna',
# 'PecanPie',
# 'PotatoSalad',
# 'PulledPork',
# 'PumpkinPie',
# 'VeggiePizza'
)

def get_all_verbs(dish, all_verbs, posTagger, writer, out):
  processed_steps = '/home/gt/Documents/' + dish + '/' + dish + '-Isteps/'

  steps = '/home/gt/Documents/' + dish + '/' + dish + '-ss-steps/'

  recipes = os.listdir(steps)

  for recipe in recipes:
    lines = []
    recipe_text = ''
    with open(steps + recipe) as f:
      lines = f.readlines()
      for line in lines:
        recipe_text += line
        recipe_text += '\n'


    with open(processed_steps + recipe) as f:
      sent_number = 0
      for line in f.readlines():
        tokens = wordpunct_tokenize(line)
        tags = posTagger.tag(tokens)

        for tag in tags:
          if tag[1] in ('VB', 'VBP') and tag[0].lower() not in ('shhhhhh', 're', 'are', 'be', '.)', '\'.', '(', ')', ').', '[', '***'):
            writer.writerow([dish, recipe, recipe_text, sent_number, lines[sent_number], tag[0].lower()])

            all_verbs.append(tag[0].lower())

        sent_number += 1

    out.flush()

  pass

def main():
  all_verbs = []

  posTagger = POSTagger('/home/gt/Downloads/stanford-postagger-2014-01-04/models/english-left3words-distsim.tagger', '/home/gt/Downloads/stanford-postagger-2014-01-04/stanford-postagger-3.3.1.jar')

  with open('amt_input_mac.csv', 'w') as out:
    writer = csv.writer(out)
    for dish in dishes:
      print dish
      get_all_verbs(dish, all_verbs, posTagger, writer, out)
      # break # for debugging

  print len(all_verbs)
  print all_verbs

  pass

if __name__ == '__main__':
  main()
