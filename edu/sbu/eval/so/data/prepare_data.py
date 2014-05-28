__author__ = 'gt'

import random
import codecs
import numpy as np
from scipy.stats import kendalltau as ktau
from edu.sbu.shell.Transformer import special_predicate_processing

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

def get_experiment_data(expFile):
  expF   = codecs.open(expFile, 'r',encoding)
  sents  = []
  labels = []

  for line in expF.readlines():

    sent, label = line.split(labelSeparator)
    label = label.rstrip()
    sents.append(sent)
    labels.append(label)

  expF.close()
  return sents, labels

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



def display_tsp_results(inpFileList, tspResultSet_file):
  from bs4 import BeautifulSoup
  from sklearn.externals import joblib

  tspResultSet = joblib.load(tspResultSet_file)

  files = open(inpFileList)
  itr = 0

  kTau = 0
  kTauCtr = 0
  for htmlf in files.readlines():

    htmlf = htmlf.rstrip()
    htmlf = htmlf.replace('\n', '')
    f = codecs.open(htmlf, 'r', encoding)
    text = ''
    for line in f.readlines():
      line = line.replace('\n', ' ')
      text += line
    f.close()

    #TODO When moving between blockCoref and the rest remember to change this
    #Also to update trainFileList, testFileList and valFileList
    outhtmlf = htmlf.replace('transitions-2', 'Results/UBEGGist')
    outf = codecs.open(outhtmlf, 'w', encoding)

    name = outhtmlf.split('/')[-1]
    my_html = '<html>'
    my_html += '<head> <meta charset=\'' + encoding + '\'/>'
    my_html += ('<title>' + name + '</title> </head>')
    my_html += ('<body>')

    my_html += ('<table border ="1">')
    my_html += ('<tr>')
    my_html += ('<th> Gold Standard Order </th> <th> Experiment Order </th>')
    my_html += ('</tr>')

    soup = BeautifulSoup(text)
    tables = soup.findAll('table')
    #first table contains the steps
    trs = tables[0].findAll('tr')

    if len(trs) <= 1 or len(tspResultSet[itr]) == 0:
      print 'No data for ordering ' + htmlf
      #dont break here - itr has to be incremented
    else:
      kTau += ktau(range(len(tspResultSet[itr])),\
                                  tspResultSet[itr], False)[0]
      kTauCtr += 1



    print ' recipe from ' + htmlf
    i=1
    for j in tspResultSet[itr]:
      my_html += '<tr> <td> ' + trs[i].findAll('td')[1].text + ' </td> '
      my_html += ' <td> ' + trs[j + 1].findAll('td')[1].text + ' </td> </tr> '
      i += 1

    my_html += '</body></html>'

    outf.write(my_html)
    outf.close()
    itr += 1

  files.close()
  print ' kTau average ' + str(kTau/kTauCtr)


def repl(m):
  one = m.group(1)
  two = m.group(2)
  three = m.group(3)
  return one + two + ' ' + three

def prepare_tsp_experiment_data(inpFileList, outFile):

  print 'data already prepared'
  return

  samples      = open(outFile, 'w')
  files        = open(inpFileList)

  for arg_file in files.readlines():

    arg_file = arg_file.rstrip()
    arg_file = arg_file.replace('\n','')
    f = codecs.open(arg_file, 'r')


    my_separator = 'TheGT'
    sentences = []
    sent_num = -1
    with open(arg_file) as f:
      lines = f.readlines()
      for i in xrange(0, len(lines), 7):
        for j in xrange(abs(sent_num  - int(lines[i].split(my_separator)[-1].strip()))):

          #Note: Splitting based on a custom separator TheGT
          sent_num = int(lines[i].split(my_separator)[-1].strip())
          pred_num = int(lines[i+1].split(my_separator)[-1].strip())
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
          sample = successor + sentSeparator + predecessor + labelSeparator + '-'
        else:
          sample = predecessor + sentSeparator + successor + labelSeparator + '+'
        sampleCtr += 1
        samples.write(sample + '\n')
    #dont know why this is needed
    # samples.write( str(len(lines)) + ',' + str(sampleCtr) + recipeSeparator + '\n' )

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
    ctr += 1


    label = line.split(labelSeparator)[1]
    label = label.rstrip()
    # print label
    if label == '+':
      p += 1

  print "Number of positives " + str(p)
  print "Number of samples " + str(ctr)


def main():
  # prepare_tsp_experiment_data(trainFileList, trainTSPFile)
  # prepare_tsp_experiment_data(devFileList, devTSPFile)
  # prepare_tsp_experiment_data(testFileList, testTSPFile)
  # print '~~~Training Set~~~'
  # get_stat(trainTSPFile)
  # print '~~~Dev Set~~~'
  # get_stat(devTSPFile)
  # print '~~~Test Set~~~'
  # get_stat(testTSPFile)
  pass


if __name__ == '__main__':
  main()
  print '#############'

'''
~~~Training Set~~~
Number of positives 1921
Number of samples 3782

~~~Dev Set~~~
Number of positives 390
Number of samples 765

~~~Test Set~~~
Number of positives 496
Number of samples 1010
'''