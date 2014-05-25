__author__ = 'gt'
import commands
class RecipeReader:

  def __init__(self, recipe_name):
    self.archive_root = '/home/gt/Documents/'
    self.recipe_name = recipe_name
    self.recipe_root = self.archive_root + self.recipe_name + '/' + self.recipe_name + '-steps/'

    self.pred_args_root = self.archive_root + self.recipe_name + '/' + self.recipe_name + 'Args/'
    self.words = []
    self.verbs = []
    self.sem_groups = []
    self.read()
    pass

  def read_corpus(self):
    for recipe_file in commands.getoutput('ls ' + self.recipe_root + '*.txt').split('\n'):
      with open(recipe_file) as f:
        lines = f.readlines()
        for line in lines:
          line = line.lower()
          self.words.extend(line.split())
      pass
    pass

  def read_verbs(self):
    my_separator = 'TheGT'
    for args_file in commands.getoutput('ls ' + self.pred_args_root + '*.txt').split('\n'):
      with open(args_file) as f:
        lines = f.readlines()
        for i in xrange(0, len(lines), 7):
          sem_group = {'pred':None, 'arg1':None, 'arg2':None, 'arg1POS': None, 'arg2POS' : None}
          pred = lines[i+2].split(my_separator)[-1].strip()
          arg1 = lines[i+3].split(my_separator)[-1].strip()
          arg1POS = lines[i+4].split(my_separator)[-1].strip()
          arg2 = lines[i+5].split(my_separator)[-1].strip()
          arg2POS = lines[i+6].split(my_separator)[-1].strip()
          if(pred != 'NULL'):
            sem_group['pred'] = pred.lower()
          if(arg1 != 'NULL'):
            sem_group['arg1'] = arg1.lower()
            sem_group['arg1POS'] = arg1POS
          if(arg2 != 'NULL'):
            sem_group['arg2'] = arg2.lower()
            sem_group['arg2POS'] = arg2POS

          self.verbs.append(pred)
          self.sem_groups.append(sem_group)
    pass

  def read(self):
    self.read_corpus()
    self.read_verbs()
    pass

  def save_all(self):
    pass

  pass