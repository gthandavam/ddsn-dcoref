__author__ = 'polina'
import commands
from nltk import wordpunct_tokenize

class RecipeReader2:

  def __init__(self, recipe_name):
    self.archive_root = '/home/gt/Documents/'
    self.recipe_name = recipe_name
    self.recipe_root = self.archive_root + self.recipe_name + '/' + self.recipe_name + '-steps/'

    self.pred_args_root = self.archive_root + self.recipe_name + '/' + self.recipe_name + 'Args/'
    self.words = []
    self.recipes = []
    self.recipe_verbs = []
    self.recipe_args1 = []
    self.recipe_args2 = []
    self.verbs = []
    self.sem_groups = []
    self.read()
    pass

  def read_corpus(self):
    for recipe_file in commands.getoutput('ls ' + self.recipe_root + '*.txt').split('\n'):
      with open(recipe_file) as f:
        lines = f.readlines()
        sentences = []
        for line in lines:
          line = line.lower()
          # self.words.extend(line.split())
          # self.words.extend(wordpunct_tokenize(line))
          sentences.append(wordpunct_tokenize(line))
        self.recipes.append(sentences)
      pass
    pass

  def read_verbs(self):
    my_separator = 'TheGT'
    for args_file in commands.getoutput('ls ' + self.pred_args_root + '*.txt').split('\n'):
      with open(args_file) as f:
        lines = f.readlines()
        sentences_verbs = []
        sentences_args1 = []
        sentences_args2 = []
        verbs = None
        args1 = None
        args2 = None
        prev_sent_num = -1
        for i in xrange(0, len(lines), 13):
          sent_num = int(lines[i].replace("sentNum: TheGT",""))
          sem_group = {'pred':None, 'arg1':None, 'arg2':None, 'arg1POS': None, 'arg2POS' : None, 'pred_start' : -1, 'pred_end' : -1, 'arg1_start' : -1, 'arg1_end' : -1, 'arg2_start' : -1, 'arg2_end' : -1}
          pred = lines[i+2].split(my_separator)[-1].strip()
          pred_start = int(lines[i+3].split(my_separator)[-1].strip())
          pred_end = int(lines[i+4].split(my_separator)[-1].strip())
          arg1 = lines[i+5].split(my_separator)[-1].strip()
          arg1POS = lines[i+6].split(my_separator)[-1].strip()
          arg1_start = int(lines[i+7].split(my_separator)[-1].strip())
          arg1_end = int(lines[i+8].split(my_separator)[-1].strip())
          arg2 = lines[i+9].split(my_separator)[-1].strip()
          arg2POS = lines[i+10].split(my_separator)[-1].strip()
          arg2_start = int(lines[i+11].split(my_separator)[-1].strip())
          arg2_end = int(lines[i+12].split(my_separator)[-1].strip())
          if(pred != 'NULL'):
            sem_group['pred'] = pred.lower()
            sem_group['pred_start'] = pred_start
            sem_group['pred_end'] = pred_end
          if(arg1 != 'NULL'):
            sem_group['arg1'] = arg1.lower()
            sem_group['arg1POS'] = arg1POS
            sem_group['arg1_start'] = arg1_start
            sem_group['arg1_end'] = arg1_end
          if(arg2 != 'NULL'):
            sem_group['arg2'] = arg2.lower()
            sem_group['arg2POS'] = arg2POS
            sem_group['arg2_start'] = arg2_start
            sem_group['arg2_end'] = arg2_end

          self.verbs.append(pred.lower())
          if sent_num!=prev_sent_num:
            if verbs!=None:
              sentences_verbs.append(verbs)
              sentences_args1.append(args1)
              sentences_args2.append(args2)
            verbs = []
            args1 = []
            args2 = []
          verbs.append(pred.lower())
          arrPOS = arg1POS.split()
          verb_args1 = []
          for e in arrPOS:
            arr = e.split("/")
            if len(arr)==2 and "NN" in arr[1]:
              verb_args1.append(arr[0].lower())
          args1.append(verb_args1)
          verb_args2 = []
          arrPOS = arg2POS.split()
          for e in arrPOS:
            arr = e.split("/")
            if len(arr)==2 and "NN" in arr[1]:
              verb_args2.append(arr[0].lower())
          args2.append(verb_args2)
          prev_sent_num = sent_num
          self.sem_groups.append(sem_group)
        if verbs!=None and len(verbs)!=0:
          sentences_verbs.append(verbs)
          sentences_args1.append(args1)
          sentences_args2.append(args2)
        self.recipe_verbs.append(sentences_verbs)
        self.recipe_args1.append(sentences_args1)
        self.recipe_args2.append(sentences_args2)
    pass

  def read(self):
    self.read_corpus()
    self.read_verbs()
    pass

  def save_all(self):
    pass

  pass