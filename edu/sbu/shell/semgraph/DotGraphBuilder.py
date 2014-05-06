__author__ = 'gt'
import codecs
import logging
encoding = 'UTF-8'

class DotGraphBuilder:

  def __init__(self):
    #TODO: refactor the class based on extensible number and type of arguments per predicate
    self.pred_props = {'shape':'diamond','style':'filled','fillcolor':'gray'}
    self.arg1_props = {}
    self.arg2_props = {'shape':'rectangle','style':'filled','fillcolor':'goldenrod'}
    self.edge_props = {
      'DerivationallyRelated' : {'label':'DerivationallyRelated', 'color': 'blue', 'style' : 'dotted'},
      'ArgString' : {'label':'ArgString', 'color' : 'gray'},
      'IArgHeuristics' : {'label' : 'IArg','color':'red', 'style':'dashed'},
      'CC' : {'label' : 'CC', 'color' : 'green', 'style':'bold'}
    }
    self.graph_lines = []
    self.pred_node_list = {}
    self.arg1_node_list = {}
    self.arg2_node_list = {}
    self.node_num = 0
    self.logger = logging.getLogger('root')
    ###MST specific
    self.adj_list = {}
    self.id_node_map = {}


  def process_pnodes(self, pnodes):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        #assuming pred node can never be null
        self.pred_node_list[(i,j)] = 'T' + str(self.node_num)

        self.id_node_map[self.pred_node_list[(i,j)]] = pnodes[i][j]

        line = '{}[label=\"{}\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate)
        # line = self.pred_node_list[(i,j)] + '[label=\"' + pnodes[i][j].predicate + '\"'
        for key in self.pred_props.keys():
          line += ', {}={}'.format(key,self.pred_props[key])

        line += ']'
        self.graph_lines.append(line)
        self.node_num += 1
    pass

  def process_rnodes(self, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        #TODO: dont fix argument slots : process based on arg_type in RNode
        for k in xrange(1,3):
          node_id = 'T'+str(self.node_num)
          self.id_node_map[node_id] = rnodes[i][j][k]
          if not rnodes[i][j][k].is_null:

            line = node_id
            if rnodes[i][j][k].arg_type == 'arg1':
              self.arg1_node_list[(i,j,k)] = node_id
              line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              for key in self.arg1_props.keys():
                line +=', {}={}'.format(key, self.arg1_props[key])
              line += ']'
            elif rnodes[i][j][k].arg_type == 'arg2':
              self.arg2_node_list[(i,j,k)] = node_id
              line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              for key in self.arg2_props.keys():
                line +=', {}={}'.format(key, self.arg2_props[key])
              line += ']'
            else:
              self.logger.error('unknown arg type')
              continue

            self.graph_lines.append(line)
          else:
            #handling the null instantiations to identify active nodes in connected components
            #a node is active when it can be connected

            if rnodes[i][j][k].arg_type == 'arg1':
              self.arg1_node_list[(i,j,k)] = node_id
            elif rnodes[i][j][k].arg_type == 'arg2':
              self.arg2_node_list[(i,j,k)] = node_id
            else:
              self.logger.error('unknown arg type')
            pass
            #not appending this node to the graph for display

          self.node_num += 1
    pass

  def add_to_adj_list(self, fro, to):
    if fro in self.adj_list.keys():
      self.adj_list[fro].append(to)
    else:
      self.adj_list[fro] = [to]

  def get_edges(self, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        for k in xrange(1,3):
          if rnodes[i][j][k].is_null:
            #implicit arg edge
            if len(rnodes[i][j][k].shell_coref) != 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              edge_type = rnodes[i][j][k].shell_coref[0][1]
              pred_node  = self.pred_node_list[(i,j)]
              line = '{} -> {}[label=\"{}\"'.format(shell_node, pred_node, edge_type)
              for prop in self.edge_props[edge_type]:
                line += ', {}={}'.format(prop, self.edge_props[edge_type][prop])
              line += ']'
              self.graph_lines.append(line)
              # self.logger.error(line + ' shell')
              self.add_to_adj_list(shell_node, pred_node)
            else:
              #null instant edge
              if rnodes[i][j][k].arg_type == 'arg1':
                null_node = self.arg1_node_list[(i,j,k)]
              elif rnodes[i][j][k].arg_type == 'arg2':
                null_node = self.arg2_node_list[(i,j,k)]
              else:
                self.logger.error('unknown arg type')

              # self.logger.error('{} -> {} null'.format(null_node, self.pred_node_list[(i,j)]))

              self.add_to_adj_list(null_node, self.pred_node_list[(i,j)])
              pass
          else:
            if rnodes[i][j][k].arg_type == 'arg1':
              arg_node = self.arg1_node_list[(i,j,k)]
            elif rnodes[i][j][k].arg_type == 'arg2':
              arg_node = self.arg2_node_list[(i,j,k)]
            else:
              self.logger.warn('unknown arg type')
            line =  '{} -> {}[label={}]'.format(arg_node, self.pred_node_list[(i,j)], 'SRL')
            # self.logger.error(line)
            self.add_to_adj_list(arg_node, self.pred_node_list[(i,j)])
            self.graph_lines.append(line)

            if len(rnodes[i][j][k].shell_coref) > 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              edge_type = rnodes[i][j][k].shell_coref[0][1]

              line = '{} -> {}[label=\"{}\"'.format(shell_node, arg_node, edge_type)

              for prop in self.edge_props[edge_type]:
                line += ', {}={}'.format(prop, self.edge_props[edge_type][prop])
              line += ']'

              self.graph_lines.append(line)
              # self.logger.error(line + ' shell')
              self.add_to_adj_list(shell_node, arg_node)

    pass

  def get_header(self):
    self.graph_lines.insert(0, 'Digraph G {')

  def get_footer(self):
    self.graph_lines.append('}')

  def get_edge_list_mst(self, pnodes, rnodes):
    self.process_pnodes(pnodes)
    self.process_rnodes(rnodes)
    for key in self.id_node_map.keys():
      self.adj_list[key] = []

    self.get_edges(rnodes)

    return self.adj_list, self.id_node_map

  def write_gv(self, pnodes, rnodes, file_name):
    self.get_header()
    # self.process_pnodes(pnodes)
    # self.process_rnodes(rnodes)
    # self.get_edges(rnodes)
    self.get_cc_edges(pnodes)
    self.get_footer()

    with codecs.open(file_name, 'w', encoding) as f:
      for line in self.graph_lines:
        f.write(line+'\n')

    # #to prepare dish network
    # ing_flow_file = file_name.replace('-dot-files', '-ing-flow')
    # ing_flow_file = ing_flow_file.replace('.gv','.txt')
    # self.write_ingredient_flow(pnodes, rnodes, ing_flow_file)

  def get_cc_edges(self, pnodes):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        # if len(pnodes[i][j].cc_edge) > 0:
        for k in xrange(len(pnodes[i][j].cc_edge)):
          start_node = self.pred_node_list[(i,j)]
          arg_node = self.id_node_map[pnodes[i][j].cc_edge[k]]

          if arg_node.is_null:
            arg_node = self.pred_node_list[(arg_node.sent_num,arg_node.pred_num)]
          else:
            if arg_node.arg_type == 'arg1':
              arg_node = self.arg1_node_list[(arg_node.sent_num,arg_node.pred_num, 1)]
            elif arg_node.arg_type == 'arg2':
              arg_node = self.arg2_node_list[(arg_node.sent_num,arg_node.pred_num, 2)]
            else:
              self.logger.error('Unknown arg type')

          line = '{} -> {} [label=\"{}\"'.format(start_node, arg_node, 'CC')

          for prop in self.edge_props['CC'].keys():
            line += ',{}={}'.format(prop, self.edge_props['CC'][prop])

          line += ']'

          self.graph_lines.append(line)

          pass
        pass

  def write_ingredient_flow(self, pnodes, rnodes, file_name):
    with open(file_name, 'w') as f:
      for i in xrange(len(pnodes)):
        for j in xrange(len(pnodes[i])):

          line = '{}[label=\"{}\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate)
          # line = self.pred_node_list[(i,j)] + '[label=\"' + pnodes[i][j].predicate + '\"'
          for ing in pnodes[i][j].pIngs:
            line += ', {}'.format(ing)

          line += ']'

          line += '\n'

          self.logger.warn(pnodes[i][j].predicate)
          # self.logger.error(len(pnodes[i][j].pIngs))
          f.write(line)

      for i in xrange(len(rnodes)):
        for j in xrange(len(rnodes[i])):
          for k in xrange(1,3):
            # if not rnodes[i][j][k].is_null:
            #   rnode_label = self.arg1_node_list[(i,j, k)] if k == 1 else self.arg2_node_list[(i,j,k)]
            # else:
            #   rnode_label = 'NULL_INST'

            #commented the above lines since even null nodes have IDs
            rnode_label = self.arg1_node_list[(i,j, k)] if k == 1 else self.arg2_node_list[(i,j,k)]
            line = '{}[label=\"{}\"'.format(rnode_label, rnodes[i][j][k].text)
            for ing in rnodes[i][j][k].argIngs:
              line += ', {}'.format(ing)

            line += ']'
            line += '\n'
            f.write(line)