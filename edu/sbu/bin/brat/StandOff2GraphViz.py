__author__ = 'gt'


import commands
import sys
import os

####################
#
#chloe guidelines
# T -> node label
#eg: T2      predicate 37 44 combine
# Skip Lines starting with T that are Evolution and user_comment
# R -> edge label
#eg: R1      object Arg1:T2 Arg2:T3
# E -> event, EID followed by Evolution, consider as edge label
#eg: E2      Evolution:T33 Cause:T2

# also skip lines that start with # (notes)
####################

NODE_LABEL = 'T'
EDGE_LABEL = 'R'
EVOLUTION_LABEL = 'E'
EVOLUTION = 'Evolution'
USER_COMMENT = 'user_comment'
GV_DIR = 'dot_files'
SVG_DIR = 'svg_files'


edge_list = [] #list of hashes : ( {}, {}, {})
node_list = [] #list of hashes : ( {}, {}, {})
event_node_map = {} #for handling EVOLUTION edges

def print_nodes(f):
  #add image logic later on
  for node in node_list:
    line = node['name'] + '[label=\"' + node['value'] + '\"'
    if node['type'] == 'predicate':
      line += ', shape=oval, style=filled, fillcolor=gray'
    else:
      line += ', shape=oval'

    line += '];'
    f.write(line+'\n')
  pass

def print_edges(f):
  for edge in edge_list:
    f.write(edge['node2'] + ' -> ' + edge['node1'] + ';\n')

def print_header(f, recipe_name):
  f.write('digraph \"'+ recipe_name + '\" { \n')
  # f.write('digraph G { \n')

def print_footer(f):
  if sys.platform != 'linux2':
    f.write('}\n')
  else:
    f.write('}\n')


def make_svg(OUTPUT_DIR, f_name):
  of_name = f_name.replace('.gv', '.svg')
  of_name = os.path.join(OUTPUT_DIR, SVG_DIR, of_name)
  f_name = os.path.join(OUTPUT_DIR, GV_DIR, f_name)
  status, output = commands.getstatusoutput('dot -Tsvg ' + f_name + ' -o' + of_name)

  #print output in case of any error
  if(status == 0):
    print output
  return status

def get_link(node_list, span_start, span_end):
  '''
  search through the node_list and identify the node that contains the span_start, span_end
  '''

  for node in node_list:
    if node['span_start'] <= span_start and node['span_end'] >= span_end:
      return node['name']
    pass

  print 'this should never happen'
  return 'BLAH'
  pass

if __name__ == '__main__':
  global edge_list
  global node_list

  if len(sys.argv) != 3:

    print 'USAGE: python StandOff2GraphViz.py <INPUT_DIR> <OUTPUT_DIR>'
    print '<OUTPUT_DIR> will be created, if not already available'
    exit(1)
  INPUT_DIR = sys.argv[1]
  OUTPUT_DIR = sys.argv[2]

  #make out dir
  try:
    os.makedirs(OUTPUT_DIR)
  except Exception as e:
    pass

  try:
    os.makedirs(os.path.join(OUTPUT_DIR, GV_DIR))
  except Exception as e:
    pass

  try:
    os.makedirs(os.path.join(OUTPUT_DIR, SVG_DIR))
  except Exception as e:
    pass

  #read all .ann files
  for file_name in commands.getoutput('ls ' + os.path.join(INPUT_DIR, '*.ann')).split('\n'):
    node_list = []
    edge_list = [] #re-initializing per file

    #filename is the last component in the path
    file_name = file_name.split(os.sep)[-1]
    # file_name = 'arizona-roadhouse-chili.ann' #for debugging
    of_name = file_name.replace('.ann', '.gv')
    out_f = open(os.path.join(OUTPUT_DIR, GV_DIR, of_name), 'w')
    f = open(os.path.join(INPUT_DIR, file_name))

    print 'pass 1: ' + file_name
    for line in f.readlines():
      if(line.startswith(NODE_LABEL)):
        cols = line.split('\t')

        if cols[1].split()[0] == USER_COMMENT:
          continue

        if cols[1].split()[0] == EVOLUTION:
          #do nothing in first pass
          continue
          pass

        new_node = {'name': cols[0], 'type': cols[1].split()[0], 'span_start': int(cols[1].split()[1]), 'span_end':int(cols[1].split()[2]) ,'value' : cols[2].rstrip('\n')}

        node_list.append(new_node)

      elif(line.startswith(EDGE_LABEL)):
        name = line.split('\t')[0]
        cols = line.split('\t')[1]
        cols = cols.rstrip('\n') #removing \n at the end
        type = cols.split()[0]
        cols = cols.split()[1:] #getting Relation args alone
        node1 = cols[0].split(':')[1]
        node2 = cols[1].split(':')[1]

        new_edge = {'name': name, 'type': type, 'node1' : node1,
                      'node2' : node2}
        edge_list.append(new_edge)

      elif(line.startswith(EVOLUTION_LABEL)):
        #do nothing in first pass
        continue

      else:
        print "Skipping following line in " + file_name + '\n' + line

    f.close()

    f = open(os.path.join(INPUT_DIR, file_name))

    print 'pass 2: ' + file_name
    for line in f.readlines():
      if(line.startswith(NODE_LABEL)):
        cols = line.split('\t')

        if cols[1].split()[0] == USER_COMMENT:
          continue

        if cols[1].split()[0] == EVOLUTION:
          #Link the Evolution node name to the corresponding arg*
          #update event_node_map
          span_start = int(cols[1].split()[1])
          span_end = int(cols[1].split()[2])
          link_node = get_link(node_list, span_start, span_end)
          event_node_map[cols[0]] = link_node
          continue
          pass



      elif(line.startswith(EVOLUTION_LABEL)):
        name = line.split('\t')[0]
        cols = line.split('\t')[1].rstrip('\n')
        cols = cols.split() #args for R* are space separated
        type = cols[0].split(':')[0]


        node1 = event_node_map[cols[0].split(':')[1]]
        node2 = cols[1].split(':')[1]
        new_edge = {'name': name, 'type': type, 'node1' : node1,
                      'node2' : node2}
        edge_list.append(new_edge)


    f.close()

    recipe_name = of_name.split('.gv')[0]
    print_header(out_f, recipe_name)
    print_nodes(out_f)
    out_f.flush()
    print_edges(out_f)
    out_f.flush()
    print_footer(out_f)
    out_f.close()

    #making svg file
    if (make_svg(OUTPUT_DIR, of_name) != 0):
      print 'error while creating svg file'

    # break #for debugging
