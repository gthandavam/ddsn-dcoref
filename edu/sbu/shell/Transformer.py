__author__ = 'gt'

# from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.shell.rules.RuleEngine import RuleEngine
from edu.sbu.shell.semgraph.DCorefGraphBuilder import DCorefGraphBuilder
import commands
import edu.sbu.shell.logger.log as log
import sys
from edu.sbu.mst.MSTGraphTransformer import MSTGraphTransformer
from edu.sbu.mst.weighted_graph.solver.edmonds import upside_down_arborescence

mod_logger = log.setup_custom_logger('root')

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


def make_nodes(srl_matrix):
  """
  takes the srl list - with each sentence separated by empty string in the list
  returns PNodes and RNodes list by invoking the respective graph builder
  (graph builder depends on the SRL tool used)
  """
  from test.swirl_parser.SwirlCorefGraphBuilder import SwirlCorefGraphBuilder
  dcoref_graph_builder = SwirlCorefGraphBuilder()
  dcoref_graph_builder.build_graph(srl_matrix)

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

def connect_arbor(pnodes_resolved, rnodes_resolved):
  arbor_adapter = MSTGraphTransformer()
  weighted_graph = arbor_adapter.transform(pnodes_resolved, rnodes_resolved)
  g = weighted_graph.get_adj_ghost_graph('order_close_together')
  root = weighted_graph.get_simple_components_root()
  # print 'root' + root
  arbor_edges = upside_down_arborescence(root, g)

  pnodes_resolved, rnodes_resolved = arbor_adapter.reverse_transform(weighted_graph, arbor_edges)

  return pnodes_resolved, rnodes_resolved, arbor_adapter.dot_builder
  pass

def main():

  #files sentence split using stanford sentence splitter - fsm based
  # i=0
  for recipe_file in commands.getoutput('ls /home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-3-steps/*.txt').split('\n'):
    # i+=1
    # if i>10:
    #   break

    mod_logger.error(recipe_file)

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/mac-and-cheese-bake.txt'

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/pumpkin-lobster-mac-and-cheese.txt'

    # recipe_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/baked-mac-and-cheese-with-sour-cream-and-cottage-cheese.txt'

    recipe_srl = get_semantic_roles(recipe_file)
    if len(recipe_srl) == 0:
      mod_logger.warn("Empty SRL roles " + recipe_file + " skipping...")
      continue

    dcoref_graph = make_nodes(recipe_srl)

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph)

    #apply MST Here
    pnodes_resolved, rnodes_resolved,dot_graph = connect_arbor(pnodes_resolved, rnodes_resolved)
    #End of MST Section

    gv_file_name = recipe_file.replace('MacAndCheese-3-steps','MacAndCheese-dot-files')
    gv_file_name = gv_file_name.replace('.txt', '.gv')
    dot_graph.write_gv(pnodes_resolved, rnodes_resolved, gv_file_name)

    make_svg(gv_file_name)
  pass


if __name__ == '__main__':
  main()

