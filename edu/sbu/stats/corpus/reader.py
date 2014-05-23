__author__ = 'gt'
import commands
class RecipeReader:

  def __init__(self, recipe_name):
    self.archive_root = '/home/gt/Documents/'
    self.recipe_name = recipe_name
    self.recipe_root = self.archive_root + self.recipe_name + '/'
    + self.recipe_name + '-steps/'

    self.pred_args_root = self.archive_root + self.recipe_name + '/'
    + self.recipe_name + 'Args/'
    self.words = []
    self.verbs = []
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
    for args_file in commands.getoutput('ls ' + self.recipe_root + '*.txt').split('\n'):
      with open(args_file) as f:
        lines = f.readlines()
        for i in xrange(0, len(lines), 7):
          verb = lines[i+2].split(my_separator)[-1].strip()
          self.verbs.extend(verb)
    pass

  def read(self):
    self.read_corpus()
    self.read_verbs()
    pass

  def save_all(self):
    pass

  pass