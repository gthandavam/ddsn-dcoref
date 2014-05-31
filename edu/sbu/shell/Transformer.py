__author__ = 'gt'

# from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.shell.rules.RuleEngine import RuleEngine
from edu.sbu.shell.semgraph.DCorefGraphBuilder import DCorefGraphBuilder
import commands
import edu.sbu.shell.logger.log as log
import sys
import pickle
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

statFile = "/home/gt/Documents/RecipeStats2_init.pickle"
statFile2 = "/home/gt/Documents/RecipeStats2.pickle"

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


  swirl_file = recipe_file.replace('MacAndCheese-3-steps', 'MacAndCheese-swirl-files')
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

  if(sem_group['pred'].lower() in ('pour', 'whisk', 'stir')):
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

def make_nodes(args_file):
  """
  Reads args for th recipe and builds nodes
  """
  dcoref_graph_builder = DCorefGraphBuilder()
  dcoref_graph_builder.PNodes.append([])
  dcoref_graph_builder.RNodes.append([])
  sent_num = -1

  my_separator = 'TheGT'
  with open(args_file) as f:
    lines = f.readlines()
    for i in xrange(0, len(lines), 7):
      for j in xrange(abs(sent_num  - int(lines[i].split(my_separator)[-1].strip()))):
        dcoref_graph_builder.PNodes.append([])
        dcoref_graph_builder.RNodes.append([])

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

      dcoref_graph_builder.make_nodes(sem_group, sent_num, pred_num)
  return dcoref_graph_builder

def make_svg(gv_file):
  of_name = gv_file.replace('.gv', '.svg')
  of_name = of_name.replace('MacAndCheese-dot-files', 'MacAndCheese-svg-files')
  #dot is in path
  status, output = commands.getstatusoutput('dot -Tsvg \"' + gv_file + '\" -o\"' + of_name + '\"')

  #print output in case of any error
  if(status != 0):
    mod_logger.error(output)

  return status

def generate_graph(pnodes_resolved, rnodes_resolved, r_stats):
  arbor_adapter = MSTGraphTransformer(r_stats)
  weighted_graph = arbor_adapter.transform(pnodes_resolved, rnodes_resolved)
  g = weighted_graph.get_adj_ghost_graph('order_close_together')
  return arbor_adapter, weighted_graph

def connect_arbor(weighted_graph, arbor_adapter, r_stats):
  g = weighted_graph.get_adj_ghost_graph('order_close_together')
  # root = weighted_graph.get_simple_components_root()
  # print 'root' + root
  root = "Ghost"
  arbor_edges = upside_down_arborescence(root, g)

  pnodes_resolved, rnodes_resolved = arbor_adapter.reverse_transform(weighted_graph, arbor_edges, weighted_graph.adj_list)

  return pnodes_resolved, rnodes_resolved, arbor_edges
  pass

def main():
  mode = ""
  if len(sys.argv)>1:
    mode = sys.argv[1]
  if mode=="-learn_init":
    learnStat(False)
  elif mode=="-learn":
    learnStat(True)
  elif mode=="-run_init":
    run(statFile)
  elif mode=="-run_iter":
    run(statFile2)
  else:
    run("")

def learnStat(useArbo):
  #files sentence split using stanford sentence splitter - fsm based
  i=0
  if useArbo:
    f = open(statFile)
    r_stats = pickle.load(f)
    f.close()
  else:
    r_stats = RecipeStats2()
    r_stats.computeStat("MacAndCheese")
  stat_data = []
  for recipe_args_file in commands.getoutput('ls /home/gt/Documents/MacAndCheese/MacAndCheeseArgs/*.txt').split('\n'):
    i+=1
    # if i>20:
    #   break
    # if i!=4:
    #   continue

    mod_logger.error(recipe_args_file)
    dcoref_graph = make_nodes(recipe_args_file)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph)

    # Generate weighted graph
    arbor_adapter, weighted_graph = generate_graph(pnodes_resolved, rnodes_resolved, r_stats)

    #apply MST Here
    pnodes_resolved, rnodes_resolved, arbor_edges = connect_arbor(weighted_graph, arbor_adapter, r_stats)
    #End of MST Section

    stat_data.append([weighted_graph, arbor_adapter, arbor_edges])

  # Calculate statistics
  r_stats.calcStatFromGraph(stat_data, useArbo)
  r_stats.test_flag = r_stats.args_verb_score
  print len(r_stats.args1_args2_verb_args_score)
  print len(r_stats.args1_verb_args_score)
  print len(r_stats.args1_args2_args_score)
  print len(r_stats.args1_args_score)

  if useArbo:
    f = open(statFile2,"w")
  else:
    f = open(statFile,"w")
  pickle.dump(r_stats,f)
  f.close()

def run(stFile):

  #files sentence split using stanford sentence splitter - fsm based
  i=0
  if stFile!="":
    f = open(stFile)
    r_stats = pickle.load(f)
    f.close()
  else:
    r_stats = RecipeStats2()
    r_stats.computeStat("MacAndCheese")
  r_stats.args_verb_score = r_stats.test_flag # due to some pickle bug!!!
  print len(r_stats.args1_args2_verb_args_score)
  print len(r_stats.args1_verb_args_score)
  print len(r_stats.args1_args2_args_score)
  print len(r_stats.args1_args_score)
  for recipe_args_file in commands.getoutput('ls /home/gt/Documents/MacAndCheese/MacAndCheeseArgs/*.txt').split('\n'):
    i+=1
    # if i>1:
    #   break
    # if i!=3:
    #   continue

    mod_logger.critical(recipe_args_file)

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/mac-and-cheese-bake.txt'

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/pumpkin-lobster-mac-and-cheese.txt'

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/baked-mac-and-cheese-with-sour-cream-and-cottage-cheese.txt'
    # recipe_args_file = '/home/gt/Documents/MacAndCheese/MacAndCheeseArgs/baked-mac-and-cheese-with-sour-cream-and-cottage-cheese.txt'
    # recipe_args_file = '/home/gt/Documents/MacAndCheese/MacAndCheeseArgs/healthy-creamy-mac-and-cheese.txt'
    # recipe_args_file = '/home/gt/Documents/MacAndCheese/MacAndCheeseArgs/bevs-mac-and-cheese.txt'

    dcoref_graph = make_nodes(recipe_args_file)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph)

    # Generate weighted graph
    arbor_adapter, weighted_graph = generate_graph(pnodes_resolved, rnodes_resolved, r_stats)
    dot_graph = arbor_adapter.dot_builder

    #apply MST Here
    pnodes_resolved, rnodes_resolved, arbor_edges = connect_arbor(weighted_graph, arbor_adapter, r_stats)
    #End of MST Section

    gv_file_name = recipe_args_file.replace('MacAndCheeseArgs','MacAndCheese-dot-files')

    gv_file_name = gv_file_name.replace('.txt', '.gv')
    dot_graph.write_gv(pnodes_resolved, rnodes_resolved, arbor_edges, gv_file_name)

    make_svg(gv_file_name)
    # break
  pass


if __name__ == '__main__':
  main()
