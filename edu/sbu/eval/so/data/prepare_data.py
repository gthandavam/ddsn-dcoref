__author__ = 'gt'

import random
import codecs
import numpy as np
from scipy.stats import kendalltau as ktau
from edu.sbu.shell.Transformer import special_predicate_processing, special_pp_processing

###Parameters
testFileList    = 'testFilesList'
trainFileList   = 'trainFilesList'
devFileList     = 'devFilesList'
negP            = 0.51 # rand >= negativeP for negative sample
trainTSPFile    = 'TSPtrainSamples.txt'
testTSPFile     = 'TSPtestSamples.txt'
devTSPFile      = 'TSPdevSamples.txt'

sentSeparator   = '#SENTENCE#'
recipeSeparator = '#RECIPE#'
pairSeparator   = '#PAIR#'
encoding        = 'utf-8' #encoding per website
stopLimit       = 612 #dev parameter - to control the generation process
labelSeparator  = '#LABEL#' # separates the block and the label
###Parameters

def get_tsp_experiment_data(expFile):
  expF   = codecs.open(expFile, 'r',encoding)
  sents  = []
  labels = []
  pairs  = []
  recipeLength = []

  for line in expF.readlines():
    if line.find(recipeSeparator) != -1:
      line.rstrip()
      x,y = line.split(recipeSeparator)
      x,y = x.split(',')
      #no of nodes, no of samples in this recipe
      recipeLength.append((int(x),int(y)))
      continue

    sent, label = line.split(labelSeparator)
    label = label.rstrip()
    label, pair = label.split(pairSeparator)
    pair = pair.rstrip()
    sents.append(sent)
    labels.append(label)
    pairs.append(str(pair)) #comma separated


  expF.close()
  return sents, labels, pairs, recipeLength


def prepare_tsp_experiment_data(inpFileList, outFile):

  # print 'data already prepared'
  # return

  samples      = open(outFile, 'w')
  files        = open(inpFileList)

  for arg_file in files.readlines():

    arg_file = arg_file.rstrip()
    arg_file = arg_file.replace('\n','')

    my_separator = 'TheGT'
    sentences = []
    sent_num = -1
    with open(arg_file) as f:
      lines = f.readlines()
      for i in xrange(0, len(lines), 7):
        #Note: Splitting based on a custom separator TheGT
        sem_group = {'pred':None, 'arg1':None, 'arg2':None, 'arg1POS': None, 'arg2POS' : None}
        pred = lines[i+2].split(my_separator)[-1].strip()
        arg1 = lines[i+3].split(my_separator)[-1].strip()
        arg1POS = lines[i+4].split(my_separator)[-1].strip()
        arg2 = lines[i+5].split(my_separator)[-1].strip()
        arg2POS = lines[i+6].split(my_separator)[-1].strip()
        if(pred != 'NULL'):
          sem_group['pred'] = pred
        if(arg1 != 'NULL'):
          sem_group['arg1'] = arg1
          sem_group['arg1POS'] = arg1POS
        if(arg2 != 'NULL'):
          sem_group['arg2'] = arg2
          sem_group['arg2POS'] = arg2POS

        sem_group = special_predicate_processing(sem_group)
        sem_group = special_pp_processing(sem_group)

        if(sem_group['pred'] is None):
          continue
        else:
          pred = sem_group['pred']
        if(sem_group['arg1'] is None):
          arg1 = 'NULL'
        else:
          arg1 = sem_group['arg1']
        if(sem_group['arg2'] is None):
          arg2 = 'NULL'
        else:
          arg2 = sem_group['arg2']


        exp_line = pred + ' ' + arg1 + ' ' + arg2
        sentences.append(exp_line)

    # for line in f.readlines():
    #   line = line.replace('\n', ' ')
    #   re.sub(r'([\w\W])(\.+)([\w\W])', repl, line)
    #   text += line

    lines = sentences
    sampleCtr = 0

    for i in range(len(lines)):
      predecessor = lines[i]

      for j in range(i+1, len(lines)):
        successor = lines[j]

        tP = round(random.random(),2)
        if tP >= negP:
          sample = successor + sentSeparator + predecessor + labelSeparator + '-' + pairSeparator + str(j) + ',' + str(i)
        else:
          sample = predecessor + sentSeparator + successor + labelSeparator + '+' + pairSeparator + str(i) + ',' + str(j)
        sampleCtr += 1
        samples.write(sample + '\n')
    #dont know why this is needed
    samples.write( str(len(lines)) + ',' + str(sampleCtr) + recipeSeparator + '\n' )
    # break #for debugging

  files.close()
  samples.close()


def get_tsp_test_data():
  return get_tsp_experiment_data(testTSPFile)

def get_tsp_train_data():
  return get_tsp_experiment_data(trainTSPFile)

def get_tsp_validation_data():
  return get_tsp_experiment_data(devTSPFile)


def get_stat(expFile):
  f = codecs.open(expFile, 'r')
  p = 0
  ctr = 0
  for line in f.readlines():
    line = line.rstrip()
    if(len(line.split()) == 0):
      continue

    if(line.find(recipeSeparator) != -1):
      continue

    ctr += 1

    label = line.split(labelSeparator)[1]
    label = label.rstrip()
    # print label
    if label.startswith('+'):
      p += 1

  print "Number of positives " + str(p)
  print "Number of samples " + str(ctr)


def main():
  prepare_tsp_experiment_data(trainFileList, trainTSPFile)
  prepare_tsp_experiment_data(devFileList, devTSPFile)
  prepare_tsp_experiment_data(testFileList, testTSPFile)
  print '~~~Training Set~~~'
  get_stat(trainTSPFile)
  print '~~~Dev Set~~~'
  get_stat(devTSPFile)
  print '~~~Test Set~~~'
  get_stat(testTSPFile)
  pass


if __name__ == '__main__':
  main()
  print '#############'

'''
~~~Training Set~~~
Number of positives 2200
Number of samples 4484

~~~Dev Set~~~
Number of positives 467
Number of samples 922

~~~Test Set~~~
Number of positives 612
Number of samples 1212
'''