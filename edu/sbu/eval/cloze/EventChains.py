__author__ = 'gt'

from edu.sbu.shell.Transformer import special_pp_processing, special_predicate_processing

from pydot import graph_from_dot_file

'''
task 1: Get all the verbs in a chain in the final recipe graph.
Read .gv file and get the verbs from there

1. Test set is contained in <recipe>/testFiles.txt
2. For these recipes, identify chains having a length of at least 5 and perform
cloze evaluation
3. Identify all the verbs in the recipe;
4. Try to fill in probability values for all the verbs
5. Obtain a rank
6. Get Recall @ N score like Jans et al 2012..,
'''

class EventChains:
  def __init__(self, dish, expName):
    self.dishName = dish
    self.argsArchive = '/home/gt/Documents/' + self.dishName + '/' + self.dishName + 'Args/'
    self.testFileList = '/home/gt/Documents/' + self.dishName + '/testFilesList'
    self.chainLength = 5
    self.expName = expName
    self.gv_dir = '/home/gt/Documents/' + self.dishName + '/' + self.dishName + '-dot-files-' + self.expName + '/'
    self.sem_groups = {}
    self.verbs = self.get_verbs()
    self.sentinel = 'Ghost'
    pass

  def get_verbs(self):
    import os
    ret = {}

    argsArchive = '/home/gt/Documents/' + self.dishName + '/' + self.dishName +'Args/'
    # with open(testFileList) as f:
    for file in os.listdir(argsArchive):
      # with open(file) as f:
      #   for line in f.readlines():
      #     line = line.strip()
      #     if len(line) != 0:
      #       recipeName = line.split('/')[-1]
      sem_groups = self.get_sem_groups(argsArchive + file)
      self.sem_groups[argsArchive + file] = sem_groups

      for sem_group in sem_groups:
        if(sem_group['pred'].endswith(' in ')):
          pred = sem_group['pred'].split()[0].lower()
        else:
          pred = sem_group['pred'].lower()

        if not pred in ret.keys():
          ret[pred] = 1

    return ret.keys()
    pass

  def get_adj_list(self, recipe_graph):
    verbs = {}
    arg1 = {}
    arg2 = {}
    graph = graph_from_dot_file(self.gv_dir + recipe_graph)
    print graph
    return graph
    pass

  def get_verb_chains(self):
    with open(self.testFileList) as f:
      for recipe in f.readlines():
        recipe = recipe.strip()
        recipe = recipe.split('/')[-1]
        recipe = recipe.replace('.txt', '.gv')
        adj_list = self.get_adj_list(recipe)
        # adj_list = self.reverse(adj_list)

        pass
    pass

  def get_sem_groups(self, args_file):
    sem_groups = []
    my_separator = 'TheGT'
    with open(args_file) as f:
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
        sem_groups.append(sem_group)

    return sem_groups