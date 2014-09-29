__author__ = 'gt'

import os
import sys
import shutil
import commands
'''
This script is meant
1. to copy the steps to the brat folder
2. create empty .ann files so that brat can display the content
'''

##################
BRAT_DATA = '/home/gt/Downloads/brat-v1.3_Crunchy_Frog/data/ActivityDiagramming/'
RECIPE_TEXT_LOCATION = '/home/gt/Documents/'
##################

dishes = (
#'BananaMuffins',
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
def main(recipeName):

  inputDir = RECIPE_TEXT_LOCATION + recipeName + '/' + recipeName + '-ss-steps/'
  outputDir = BRAT_DATA + recipeName + '/'
  print 'INPUT DIR : ' + inputDir
  print 'OUTPUT DIR : ' + outputDir
  try:
    os.makedirs(outputDir)
  except Exception as e:
    print e

  files = os.listdir(inputDir)

  for file in files:
    shutil.copyfile(inputDir + file, outputDir + file)

    ann_file = file.replace('.txt', '.ann')
    commands.getoutput(' touch ' + outputDir + ann_file)
    pass

  return


if __name__ == '__main__':
  for dish in dishes:
    main(dish)
  pass