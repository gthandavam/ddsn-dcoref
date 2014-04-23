__author__ = 'gt'

from edu.sbu.shell.semgraph.DotGraphBuilder import DotGraphBuilder
from edu.sbu.shell.rules.RuleEngine import RuleEngine
from edu.sbu.shell.semgraph.DCorefGraphBuilder import DCorefGraphBuilder
import commands
import edu.sbu.shell.logger.log as log
from edu.sbu.mst.MSTGraphAdapter import MSTGraphAdapter
from edu.sbu.mst.MSTSolver import MSTSolver

mod_logger = log.setup_custom_logger('root')

def get_text(senna_file):
  ret = ""
  with open(senna_file) as fp:
    for line in fp:
      ret += line

  return ret

def get_semantic_roles(recipe_file):
  """
  Runs a SRL tool to get pred argument structure and
  returns pnodes and rnodes
  """
  ret = ""
  senna_file = recipe_file.replace('MacAndCheese-steps', 'MacAndCheese-senna-files')
  cmd = 'cd /home/gt/Downloads/senna/; ./senna-linux64 -srl -posvbs -offsettags < \"' \
        + recipe_file + '\" > \"' + senna_file + '\"'
  status, output = commands.getstatusoutput(cmd)

  if(status != 0):
    ret += "NONE"
    return ret

  ret = get_text(senna_file)
  return ret


def make_nodes(srl_list):
  """
  takes the srl list - with each sentence separated by empty string in the list
  returns PNodes and RNodes list by invoking the respective graph builder
  (graph builder depends on the SRL tool used)
  """
  dcoref_graph_builder = DCorefGraphBuilder()
  dcoref_graph_builder.build_graph(srl_list)

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

def connect_mst(pnodes_resolved, rnodes_resolved):
  mst_adapter = MSTGraphAdapter()

  mst_graph = mst_adapter.transform(pnodes_resolved, rnodes_resolved)

  mst_solver = MSTSolver()

  mst_solution = mst_solver.solve(mst_graph)

  return mst_adapter.reverse_transform(mst_solution)
  pass

def main():

  #files sentence split using stanford sentence splitter - fsm based
  for recipe_file in commands.getoutput('ls /home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-steps/*.txt').split('\n'):

    # print recipe_file
    # recipe_file = '/home/gt/NewSchematicSummary/recipe-split/Asian-Garlic-Toast.txt'
    recipe_srl = get_semantic_roles(recipe_file)
    if recipe_srl.startswith("NONE"):
      mod_logger.warn("error getting SRL roles " + recipe_file + " skipping...")
      continue

    dcoref_graph_builder = make_nodes(recipe_srl.split('\n'))
    # print dcoref_graph_builder

    rule_engine = RuleEngine()
    pnodes_resolved, rnodes_resolved = rule_engine.apply_rules(dcoref_graph_builder)

    #apply MST Here
    # pnodes_resolved, rnodes_resolved = connect_mst(pnodes_resolved, rnodes_resolved)
    #End of MST Section

    graph_builder = DotGraphBuilder()
    gv_file_name = recipe_file.replace('MacAndCheese-steps','MacAndCheese-dot-files')
    gv_file_name = gv_file_name.replace('.txt', '.gv')
    graph_builder.write_gv(pnodes_resolved, rnodes_resolved, gv_file_name)

    make_svg(gv_file_name)
  pass


if __name__ == '__main__':


  main()

