__author__ = 'gt'
import sys
import os
import re
import traceback
######################
# Script to compute recall on the evolving entities/implicit arguments
#
# Input Parameters:
# 1. Directory containing .gv files for human annotations and
#
# 2. the directory that has automatically generated .gv files within one of its subdirectories
######################

######################
IMPLICIT_EDGE_LABEL = 'implicit'
EVOLUTION_EDGE_LABEL = 'evolution'
######################


def is_overlap(a,b, a1, b1):
  '''
  To determine if two interval [a,b] and [a1,b1] overlap
  '''
  if b < a1:
    return False

  if b1 < a:
    return False

  return True

def edge_found(edge, node_map, node_map_other, edge_list_other):
  '''
  Checks if the edge is present in the other diagram
  '''

  #overlap of span boundaries is considered a match; relaxed heuristic
  a = node_map[edge['node2']]['span_start']
  b = node_map[edge['node2']]['span_end']
  c = node_map[edge['node1']]['span_start']
  d = node_map[edge['node1']]['span_end']
  for other_edge in edge_list_other:
    a1 = node_map_other[other_edge['node2']]['span_start']
    b1 = node_map_other[other_edge['node2']]['span_end']
    # print other_edge['node1']
    c1 = node_map_other[other_edge['node1']]['span_start']
    d1 = node_map_other[other_edge['node1']]['span_end']

    if(is_overlap(a, b, a1, b1) and is_overlap(c, d, c1, d1)):
      return True
      pass
    pass

  # print edge['type']
  return False
  pass

def get_graph(gv_file):
  '''
  Reads a gv file and returns node_map and an edge_list
  '''
  node_map = {}
  edge_list = []

  with open(gv_file) as f:
    for line in f.readlines():
      if line.startswith('T') and line.find('->') == -1: #node definition
        name = re.search('(T.+)\[', line).group(1)
        value = re.search('\[label=\"(.+)\"', line).group(1).strip()
        start = int(re.search(';#(.+),(.+)', line).group(1).strip())
        end = int(re.search(';#(.+),(.+)', line).group(2).strip())
        node_map[name] = {'name' : name, 'value' : value, 'span_start' : start, 'span_end' : end}
        pass

      if line.startswith('Ghost'):
        name = 'Ghost'
        value = re.search('\[label=\"(.+)\"', line).group(1).strip()
        node_map[name] = {'name' : name, 'value' : value, 'span_start' : -1, 'span_end' : -1}

      if line.find('->') != -1:#edge
        m = re.search('(.+)->(.+);#', line)
        if not m:
          m = re.search('(.+)->(.+);', line) #automatic graphs do not have edge types followed by ;#

        type = 'UNKNOWN'
        m_type = re.search(';#(.+)', line)

        if m_type:
          type = m_type.group(1).strip()

        new_edge = {'node2' : m.group(1).strip(), 'node1' : m.group(2).strip(), 'type' : type}
        edge_list.append(new_edge)


  return node_map, edge_list
  pass

def get_auto_file(recipe_name, experiment):
  import commands
  out = commands.getoutput('find /home/gt/Documents/  -name ' + '\'' + recipe_name +'\' | grep \"' + experiment + '\"')
  return out.split('\n')[0]

def main():

  if(len(sys.argv) != 3):
    print 'USAGE:python compute_metric.py <INPUT_DIR_GV_file_for_BRAT_ANNOTATIONS> <Automatically_created_GV_files_directory>'
    # print (len(sys.argv))
    exit(1)

  INPUT_DIR = sys.argv[1]
  EXP = sys.argv[2]


  files = os.listdir(INPUT_DIR)

  for brat_file in files:

    recipe_name = brat_file.split(os.sep)[-1].strip()

    auto_file = get_auto_file(recipe_name, EXP)
    # print auto_file
    # auto_file = '/home/gt/svg-dir/auto_dir/FrenchToast/FrenchToast-dot-files-stat_for_eval_iteriter1000/chocolate-french-toast-2.gv'

    # print '##############' + recipe_name

    recipe_name = auto_file.split(os.sep)[-1]

    # print recipe_name, auto_file

    try:
      # print 'brat_file'
      node_map, edge_list = get_graph(os.path.join(INPUT_DIR,brat_file))
      # print 'auto_file'
      node_map_auto, edge_list_auto = get_graph(auto_file)

      implicit_ground_truth = 0
      implicit_recall = 0
      evolution_ground_truth = 0
      evolution_recall = 0
      ground_truth = len(edge_list)
      pairwise_recall = 0

      for edge in edge_list:

        edge_result = edge_found(edge, node_map,node_map_auto, edge_list_auto)

        if(edge_result):
            pairwise_recall += 1

        if( edge['type'] == IMPLICIT_EDGE_LABEL ):
          implicit_ground_truth += 1
          if(edge_result):
            # print '{} IMPLICIT {}'.format(node_map[edge['node2']], node_map[edge['node1']])
            implicit_recall += 1
          pass

        if( edge['type'] == EVOLUTION_EDGE_LABEL ):
          evolution_ground_truth += 1
          if(edge_result):
            # print '{} EVOLUTION {}'.format(node_map[edge['node2']], node_map[edge['node1']])


            evolution_recall += 1
          pass


      edges_extracted = len(edge_list_auto)
      pairwise_precision = 0
      for edge in edge_list_auto:
        edge_result = edge_found(edge, node_map_auto, node_map, edge_list)
        if(edge_result):
          pairwise_precision += 1

      # print 'recipe_name,implicit_ground_truth#,implicit_recall,evolution_ground_truth#,evolution_recall, no of edges, recall for no of edges, no of edges extracted, precision for extracted edges'
      #subtracting one from ground truth for ignoring edge on Ghost node (number subtracted should be in fact in-degree of Ghost node, for now keeping it as 1)

      #TODO: check whether edges on Ghost are getting counted correctly
      print recipe_name + ',' + str(implicit_ground_truth) + ',' + str(implicit_recall) + ',' + str(evolution_ground_truth) + ',' + str(evolution_recall) + ',' + str(ground_truth) + ',' + str(pairwise_recall) + ',' + str(edges_extracted) + ',' + str(pairwise_precision)
    except Exception as e:
      print 'exception while processing ' + recipe_name
      exc_type, exc_value, exc_traceback = sys.exc_info()
      traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
      print e.message
      print traceback.format_exception_only(type(e), e)

      pass



  #TODO calculate precision stat - precision_evolution and precision_implicit can be calculated by
  #considering pred->pred edge or pred->arg edge


  pass


if __name__ == '__main__':
  main()