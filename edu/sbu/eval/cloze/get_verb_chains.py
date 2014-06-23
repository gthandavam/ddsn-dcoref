__author__ = 'gt'

from edu.sbu.shell.Transformer import special_pp_processing, special_predicate_processing

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


#Only now I realize the need to distinguish dish and recipe :)
dishName = 'MacAndCheese'
argsArchive = '/home/gt/Documents/' + dishName + '/' + dishName + 'Args/'
testFileList = '/home/gt/Documents/' + dishName + '/testFilesList'


def get_sem_groups(args_file):
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

def get_verbs(dish):
  import os
  ret = {}
  global dishName
  global argsArchive
  dishName = dish
  argsArchive = '/home/gt/Documents/' + dishName + '/' + dishName +'Args/'
  # with open(testFileList) as f:
  for file in os.listdir(argsArchive):
    # with open(file) as f:
    #   for line in f.readlines():
    #     line = line.strip()
    #     if len(line) != 0:
    #       recipeName = line.split('/')[-1]
    sem_groups = get_sem_groups(argsArchive + file)

    for sem_group in sem_groups:
      if(sem_group['pred'].endswith(' in ')):
        pred = sem_group['pred'].split()[0].lower()
      else:
        pred = sem_group['pred'].lower()

      if not pred in ret.keys():
        ret[pred] = 1

  return ret.keys()

  pass


if __name__ == '__main__':
  mc_verbs =  set(get_verbs('MacAndCheese'))
  # print len(mc_verbs)
  # print mc_verbs
  cs_verbs = set(get_verbs('ChickenSalad'))
  # print len(cs_verbs)
  # print cs_verbs
  eg_verbs = set(get_verbs('EggNoodles'))
  # print len(eg_verbs)
  # print eg_verbs

  print len(set.intersection(mc_verbs, cs_verbs))
  print len(set.intersection(mc_verbs, eg_verbs))
  print len(set.intersection(eg_verbs, cs_verbs))

