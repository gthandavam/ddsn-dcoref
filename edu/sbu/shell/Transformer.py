__author__ = 'gt'

# from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.shell.rules.RuleEngine import RuleEngine
from edu.sbu.shell.semgraph.DCorefGraphBuilder import DCorefGraphBuilder
import commands
import edu.sbu.shell.logger.log as log
import sys
from sklearn.externals import joblib
import os
from edu.sbu.mst.MSTGraphTransformer import MSTGraphTransformer
from edu.sbu.mst.weighted_graph.solver.edmonds import upside_down_arborescence
from edu.sbu.stats.RecipeStats2 import RecipeStats2

mod_logger = log.setup_custom_logger('root')


"""
Test cases for trying different edge weights:
chipotle-mac-and-cheese
chipotle-macaroni-and-cheese
dannys-macaroni-and-cheese
reuben-mac-and-cheese
"""

# recipeName = 'ChickenSalad'
# recipeName = 'MacAndCheese'

#global variables that are over-written based on command line args passed by
#iterative_learning script
recipeName = ''
statFile = ""
statFile2 = ""
statFileForEval = ""


########################
train_files_hash = {}
########################

def get_text(swirl_output):
  """
  Parse the swirl output and return the structured data in a 3darray sent, row, column
  """

  ret = []
  #ret has 3 dimensions - sent, row, column
  with open(swirl_output) as f:
    sent_matrix = []
    for line in f.readlines():
      line = line.strip()
      line_matrix = line.split('\t')
      if len(line_matrix) == 1:
        if(len(sent_matrix) != 0):#for handling the case of consecutive empty lines in output
          ret.append(sent_matrix)
        sent_matrix = []
        continue #read next line
        pass

      sent_matrix.append(line_matrix)
      pass

  return ret
  pass

def get_semantic_roles(recipe_file):
  """
  Runs a SRL tool to get pred argument structure and
  returns pnodes and rnodes
  """
  ret = []

  #pre-process
  # with open(recipe_file) as f:
  #   lines = f.readlines()
  #
  # with open(recipe_file, 'w') as f:
  #   for line in lines:
  #     f.write('3 ' + line)


  swirl_file = recipe_file.replace(recipeName + '-3-steps', recipeName + '-swirl-files')
  #Polina - I need to setup swirl on your mac for you to be able to run this directly
  #I had to make changes to Swirl to get it running; on top of it I have made changes to
  #get output in the required format as well; so for now we could exchange swirl output files
  #and continue with development
  # if sys.platform != "linux2":
  #   senna_cmd = "senna-osx"
  # else:
  #   senna_cmd = "senna-linux64"
  cmd = 'cd /home/gt/Downloads/swirl-1.1.0/; swirl_parse_classify' + ' model_swirl/ model_charniak/ ' \
        + recipe_file + ' 1> ' + swirl_file

  # mod_logger.error(cmd)
  status, output = commands.getstatusoutput(cmd)

  if(status != 0):
    print 'error getting swirl output'
    return ret

  ret = get_text(swirl_file)
  return ret

def special_predicate_processing(sem_group):
  '''
  To handle special cases
  pour NP : None PP: in blah blah blah
  whisk NP : None PP: in blah blah blah
  stir NP: None PP: in blah blah blah
  cases
  '''
  if(sem_group['pred'] is None):
    return sem_group

  if(sem_group['pred'].lower() in ('pour', 'whisk', 'stir', 'fold', 'mix', 'cut', 'beat')):
    if(sem_group['arg1'] is None):
      if(not sem_group['arg2'] is None and sem_group['arg2'].lower().startswith('in')):
        arg2 = sem_group['arg2'].split()
        arg2 = arg2[1:]
        arg2 = ' '.join(arg2)

        arg2POS = sem_group['arg2POS'].split()
        arg2POS = arg2POS[1:]
        arg2POS = ' '.join(arg2POS)

        sem_group['pred'] = sem_group['pred'].lower() + ' in '
        sem_group['arg1'] = arg2
        sem_group['arg1POS'] = arg2POS
        sem_group['arg2'] = None
        sem_group['arg2POS'] = None
        pass

  return sem_group
  pass

def special_pp_processing(sem_group):
  '''
  To handle the case when because of a parse error, NP and PP are getting mentioned as NP
  eg:
  '''
  arg1 = []
  arg2 = []
  arg1POS = []
  arg2POS = []


  two = False
  if(sem_group['arg2'] is None and not sem_group['arg1'] is None):
    inp_arg1 = sem_group['arg1'].split()
    inp_arg1POS = sem_group['arg1POS'].split()
    for i in xrange(len(inp_arg1)):
      if(two):
        arg2.append(inp_arg1[i])
        arg2POS.append(inp_arg1POS[i])
        pass
      else:
        if inp_arg1POS[i].find('/IN') != -1:
          two = True
          arg2.append(inp_arg1[i])
          arg2POS.append(inp_arg1POS[i])
        else:
          arg1.append(inp_arg1[i])
          arg1POS.append(inp_arg1POS[i])
        pass
    pass

    if(len(arg1) > 0):
      arg1 = ' '.join(arg1)
      arg1POS = ' '.join(arg1POS)
      sem_group['arg1'] = arg1
      sem_group['arg1POS'] = arg1POS
    else:
      sem_group['arg1'] = None
      sem_group['arg1POS'] = None

    if(len(arg2) > 0):
      arg2 = ' '.join(arg2)
      arg2POS = ' '.join(arg2POS)
      sem_group['arg2'] = arg2
      sem_group['arg2POS'] = arg2POS
    else:
      sem_group['arg2'] = None
      sem_group['arg2POS'] = None


    # mod_logger.critical(' split up as ' + arg1POS + ' and ' + arg2POS)

  return sem_group
  pass

def make_nodes(args_file):
  """
  Reads args for the recipe and builds nodes
  """
  dcoref_graph_builder = DCorefGraphBuilder()
  dcoref_graph_builder.PNodes.append([])
  dcoref_graph_builder.RNodes.append([])
  sent_num = -1

  my_separator = 'TheGT'
  with open(args_file) as f:
    lines = f.readlines()
    for i in xrange(0, len(lines), 13):
      for j in xrange(abs(sent_num  - int(lines[i].split(my_separator)[-1].strip()))):
        dcoref_graph_builder.PNodes.append([])
        dcoref_graph_builder.RNodes.append([])

      #Note: Splitting based on a custom separator TheGT
      sent_num = int(lines[i].split(my_separator)[-1].strip())
      pred_num = int(lines[i+1].split(my_separator)[-1].strip())
      sem_group = {'pred':None, 'pred_start' : -1, 'pred_end' :-1, 'arg1':None, 'arg2':None, 'arg1POS': None, 'arg2POS' : None, 'arg1_start' : -1, 'arg1_end' : -1, 'arg2_start' : -1, 'arg2_end' : -1}
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
        sem_group['pred'] = pred
        sem_group['pred_start'] = pred_start
        sem_group['pred_end'] = pred_end
      if(arg1 != 'NULL'):
        sem_group['arg1'] = arg1
        sem_group['arg1POS'] = arg1POS
        sem_group['arg1_start'] = arg1_start
        sem_group['arg1_end'] = arg1_end
      if(arg2 != 'NULL'):
        sem_group['arg2'] = arg2
        sem_group['arg2POS'] = arg2POS
        sem_group['arg2_start'] = arg2_start
        sem_group['arg2_end'] = arg2_end

      sem_group = special_predicate_processing(sem_group)

      sem_group = special_pp_processing(sem_group)

      dcoref_graph_builder.make_nodes(sem_group, sent_num, pred_num)
  return dcoref_graph_builder

def make_svg(gv_file):
  of_name = gv_file.replace('.gv', '.svg')
  of_name = of_name.replace(recipeName + '-dot-files', recipeName + '-svg-files')
  #dot is in path
  status, output = commands.getstatusoutput('dot -Tsvg \"' + gv_file + '\" -o\"' + of_name + '\"')

  #print output in case of any error
  if(status != 0):
    mod_logger.error(output)

  return status

def generate_graph(pnodes_resolved, rnodes_resolved, r_stats, Wwt):
  arbor_adapter = MSTGraphTransformer(r_stats)
  weighted_graph = arbor_adapter.transform(pnodes_resolved, rnodes_resolved)
  weighted_graph.Wwt = Wwt
  weighted_graph.Warg = 1-Wwt

  return arbor_adapter, weighted_graph

def connect_arbor(weighted_graph, arbor_adapter, r_stats):
  #getting the required data structure from the weighted_graph for upside_down_arborescence
  g = weighted_graph.get_adj_ghost_graph('order_close_together')

  root = "Ghost"
  arbor_edges = upside_down_arborescence(root, g)

  pnodes_resolved, rnodes_resolved = arbor_adapter.reverse_transform(weighted_graph, arbor_edges, weighted_graph.adj_list)
  #for seeing coref-output comment the above line, uncomment the below line
  #pnodes_resolved, rnodes_resolved = arbor_adapter.reverse_transform(weighted_graph, {}, weighted_graph.adj_list)

  return pnodes_resolved, rnodes_resolved, arbor_edges
  pass

'''
API to find if a file is part of training data-set
'''
def is_training_file(args_file_name):

  #returning True always, as we needed this only for Sentence Re-ordering experiment
  # return True
  recipe_name = args_file_name.split('/')[-1]
  return recipe_name in train_files_hash.keys()
  pass

'''
helper method to load the list of recipes in training data, in memory
'''
def load_train_files_hash(recipeName):
  global train_files_hash
  with open('/home/gt/Documents/' + recipeName + '/trainFilesList') as f:
    for line in f.readlines():
      line = line.rstrip()
      # print line.split('/')[-1]
      train_files_hash[line.split('/')[-1]] = 1

    pass
  pass

def make_dir_no_exception(dirName):
  try:
    os.makedirs(dirName)
  except:
    pass


def main():
  global recipeName
  global statFile
  global statFile2
  global statFileForEval
  mode = ""
  if len(sys.argv)>1:
    mode = sys.argv[1]

  if len(sys.argv)>2:
    recipeName = sys.argv[2]
    load_train_files_hash(recipeName)

  if len(sys.argv) > 3:
    expName = sys.argv[3]


  make_dir_no_exception('/home/gt/Documents/' + recipeName + '/' + expName)


  # trans flag works only for -stat_for_eval*
  trans = False

  if len(sys.argv)>4 and sys.argv[4]=="-trans":
    trans = True

  iter_num = -1
  if len(sys.argv) > 5:
    iter_num = int(sys.argv[5])


  print sys.argv[1] + '  ' + str(iter_num)

  statFile = "/home/gt/Documents/"+ recipeName + "/"  + expName + "/RecipeStats2_init.pickle"
  statFile2 = "/home/gt/Documents/" + recipeName + "/" + expName + "/RecipeStats2_iter.pickle"
  statFileForEval = "/home/gt/Documents/" + recipeName + "/" + expName + "/RecipeStats2_forEval.pickle"

  print 'Processing ' + recipeName
  print 'Exp: ' + expName

  if mode=="-learn_init":
    learnStat(False, iter_num)
  elif mode=="-learn_iter":
    learnStat(True, iter_num, trans)
  elif mode=="-run_init":
    run(statFile,0)
  elif mode=="-run_iter":
    run(statFile2,0)
    # run(statFileForEval,0)
  elif mode=="-run_wt":
    run("",1)
  # Save stat from arborescence
  elif mode=="-stat_for_eval": # will also save dot and svg files
    run(statFile,0,True,True,trans, iter_num)
  # Save stat from arborescence (sentence index based weights)
  elif mode=="-stat_for_eval_wt": # will also save dot and svg files
    run("",1,True, True,trans, iter_num)
  # Save stat from connected components
  elif mode=="-stat_for_eval_cc": # will also save dot and svg files
    run("",1,True, False,trans, iter_num)
  # Save stat from 2nd iteration of arborescence
  elif mode=="-stat_for_eval_iter":
    run(statFile2,0,True,True,trans, iter_num)
  else:
    run("",0)

def learnStat(useArbo, iter_num=-1,transitive=False):
  #files sentence split using stanford sentence splitter - fsm based

  option = ""
  dirName = '/home/gt/Documents/' + recipeName + '/'
  if len(sys.argv) > 1:
    option = sys.argv[1]

  # try:
  #   os.makedirs(dirName+recipeName + '-dot-files'+option + 'iter' + str(iter_num))
  # except OSError:
  #   pass
  #
  # try:
  #   os.makedirs(dirName+recipeName + '-svg-files'+option + 'iter' + str(iter_num))
  # except OSError:
  #   pass

  i=0
  if useArbo:
    r_stats = joblib.load(statFile)
    # f = open(statFile)
    # r_stats = pickle.load(f)
    # f.close()
  else:
    r_stats = RecipeStats2()
    r_stats.computeStat(recipeName)
  stat_data = []


  for recipe_args_file in commands.getoutput('ls /home/gt/Documents/' + recipeName + '/' + recipeName + 'Args/*.txt').split('\n'):
    # print recipe_args_file
    if(not is_training_file(recipe_args_file)):
      #skipping if not training data
      continue

    i+=1


    mod_logger.error(recipe_args_file)
    dcoref_graph = make_nodes(recipe_args_file)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph)

    # Generate weighted graph
    arbor_adapter, weighted_graph = generate_graph(pnodes_resolved, rnodes_resolved, r_stats, 0)

    #apply MST Here
    arbor_edges = None
    if useArbo:
      pnodes_resolved, rnodes_resolved, arbor_edges = connect_arbor(weighted_graph, arbor_adapter, r_stats)
    #End of MST Section

      #no need to create diagrams here
      # dot_graph = arbor_adapter.dot_builder
      # gv_file_name = recipe_args_file.replace(recipeName +'Args',recipeName + '-dot-files'+option + 'iter' + str(iter_num))
      #
      # gv_file_name = gv_file_name.replace('.txt', '.gv')
      # try:
      #   dot_graph.write_gv(pnodes_resolved, rnodes_resolved, arbor_edges, gv_file_name)
      # except Exception as inst:
      #   print inst.args
      #   print inst.message
      #   print inst
      #   print recipe_args_file
      #   print "Error!!! 421" # temporal!!!
      #   pass
      #
      # make_svg(gv_file_name)


    stat_data.append([recipe_args_file, weighted_graph, arbor_adapter, arbor_edges])

  # Calculate statistics
  r_stats.calcStatFromGraph(stat_data, useArbo, transitive)
  # r_stats.test_flag = r_stats.args_verb_score
  print len(r_stats.args1_args2_verb_args_score)
  print len(r_stats.args1_verb_args_score)
  print len(r_stats.args1_args2_args_score)
  print len(r_stats.args1_args_score)
  print len(r_stats.args1_args2_verb_verb_score)
  print len(r_stats.args1_verb_verb_score)
  print len(r_stats.args1_args2_verb_verb_args1_score)
  print len(r_stats.args1_verb_verb_args1_score)

  if useArbo:
    joblib.dump(r_stats, statFile2)
    # f = open(statFile2,"w")
  else:
    joblib.dump(r_stats, statFile)
    # f = open(statFile,"w")
  # pickle.dump(r_stats,f, pickle.HIGHEST_PROTOCOL)
  print 'Recipes Processed: ' + str(i)
  # f.close()

def run(stFile, Wwt, stat_for_eval=False, useArbo=False, transitive=False, iter_num=-1):
  #files sentence split using stanford sentence splitter - fsm based
  i=0
  if stFile!="":
    # f = open(stFile)
    # r_stats = pickle.load(f)
    # f.close()
    r_stats = joblib.load(stFile)
    # r_stats.args_verb_score = r_stats.test_flag # due to some pickle bug!!!
  else:
    r_stats = RecipeStats2()
    r_stats.computeStat(recipeName)

  #need to take care of experiment type arbor/arbor_trans
  make_dir_no_exception('/home/gt/Documents/' + recipeName + '/Evolution/')
  make_dir_no_exception('/home/gt/Documents/' + recipeName + '/Implicit/')

  r_stats.printEvolutionProb('/home/gt/Documents/' + recipeName + '/Evolution/')
  r_stats.printImplicitProb('/home/gt/Documents/' + recipeName + '/Implicit/')
  dirName = '/home/gt/Documents/' + recipeName + '/'

  option = ""
  if len(sys.argv)>1:
    option = sys.argv[1]


  make_dir_no_exception(dirName+recipeName + '-dot-files'+option + 'iter' + str(iter_num))

  make_dir_no_exception(dirName+recipeName + '-svg-files'+option + 'iter' + str(iter_num))

  stat_data = []
  for recipe_args_file in commands.getoutput('ls '+dirName + recipeName +'Args/*.txt').split('\n'):


    #we are using recipeName to mean dishName here - let's accept it for now
    if(not is_training_file(recipe_args_file)):
      continue

    i+=1

    dcoref_graph = make_nodes(recipe_args_file)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph)

    # Generate weighted graph
    arbor_adapter, weighted_graph = generate_graph(pnodes_resolved, rnodes_resolved, r_stats, Wwt)
    dot_graph = arbor_adapter.dot_builder

    #apply MST Here
    pnodes_resolved, rnodes_resolved, arbor_edges = connect_arbor(weighted_graph, arbor_adapter, r_stats)
    #End of MST Section

    gv_file_name = recipe_args_file.replace(recipeName +'Args',recipeName + '-dot-files'+ option + 'iter' +str(iter_num))

    gv_file_name = gv_file_name.replace('.txt', '.gv')
    try:
      dot_graph.write_gv(pnodes_resolved, rnodes_resolved, arbor_edges, gv_file_name)
    except Exception as inst:
      print inst.args
      print inst.message
      print recipe_args_file
      print "Error!!!"
      pass

    make_svg(gv_file_name)

    stat_data.append([recipe_args_file, weighted_graph, arbor_adapter, arbor_edges])
    # break
  if stat_for_eval:
    # Calculate statistics
    r_stats.calcStatFromGraph(stat_data, useArbo, transitive)
    print len(r_stats.args1_args2_verb_args_score)
    print len(r_stats.args1_verb_args_score)
    print len(r_stats.args1_args2_args_score)
    print len(r_stats.args1_args_score)
    print len(r_stats.args1_args2_verb_verb_score)
    print len(r_stats.args1_verb_verb_score)
    print len(r_stats.args1_args2_verb_verb_args1_score)
    print len(r_stats.args1_verb_verb_args1_score)

    joblib.dump(r_stats, statFileForEval)

  print 'Recipes Processed: ' + str(i)
  pass


if __name__ == '__main__':

  main()

