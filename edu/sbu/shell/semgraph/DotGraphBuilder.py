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
    self.graph_lines = []
    self.pred_node_list = {}
    self.arg1_node_list = {}
    self.arg2_node_list = {}
    self.node_num = 0
    self.logger = logging.getLogger('root')


  def process_pnodes(self, pnodes):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        self.pred_node_list[(i,j)] = 'T' + str(self.node_num)

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
          if not rnodes[i][j][k].is_null:
            node_id = 'T'+str(self.node_num)
            line = node_id
            if rnodes[i][j][k].arg_type == 'arg1':
              self.arg1_node_list[(i,j,k)] = node_id
              line += '[label=\"{}\"'.format(rnodes[i][j][k].text)
              for key in self.arg1_props.keys():
                line +=', {}={}'.format(key, self.arg_props[key])
              line += ']'
            elif rnodes[i][j][k].arg_type == 'arg2':
              self.arg2_node_list[(i,j,k)] = node_id
              line += '[label=\"{}\"'.format(rnodes[i][j][k].text)
              for key in self.arg2_props.keys():
                line +=', {}={}'.format(key, self.arg2_props[key])
              line += ']'
            else:
              self.logger.warn('unknown arg type')
              continue

            self.node_num += 1
            self.graph_lines.append(line)
    pass

  def get_edges(self, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        for k in xrange(1,3):
          if rnodes[i][j][k].is_null:
            #implicit arg edge
            if len(rnodes[i][j][k].shell_coref) != 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0]]
              pred_node  = self.pred_node_list[(i,j)]
              line = '{} -> {}'.format(shell_node, pred_node)
              self.graph_lines.append(line)
          else:
            if rnodes[i][j][k].arg_type == 'arg1':
              arg_node = self.arg1_node_list[(i,j,k)]
            elif rnodes[i][j][k].arg_type == 'arg2':
              arg_node = self.arg2_node_list[(i,j,k)]
            else:
              self.logger.warn('unknown arg type')
            line =  '{} -> {}'.format(arg_node, self.pred_node_list[(i,j)])
            self.graph_lines.append(line)

            if len(rnodes[i][j][k].shell_coref) > 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0]]
              line = '{} -> {}'.format(shell_node, arg_node)
              self.graph_lines.append(line)
    pass

  def get_header(self):
    self.graph_lines.append('Digraph G {')

  def get_footer(self):
    self.graph_lines.append('};')

  def write_gv(self, pnodes, rnodes, file_name):
    self.get_header()
    self.process_pnodes(pnodes)
    self.process_rnodes(rnodes)
    self.get_edges(rnodes)
    self.get_footer()

    with codecs.open(file_name, 'w', encoding) as f:
      for line in self.graph_lines:
        f.write(line+'\n')

    #to prepare dish network
    ing_flow_file = file_name.replace('-dot-files', '-ing-flow')
    ing_flow_file = ing_flow_file.replace('.gv','.txt')
    self.write_ingredient_flow(pnodes, ing_flow_file)


  def write_ingredient_flow(self, pnodes, file_name):
    with open(file_name, 'w') as f:
      for i in xrange(len(pnodes)):
        for j in xrange(len(pnodes[i])):

          line = '{}[label=\"{}\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate)
          # line = self.pred_node_list[(i,j)] + '[label=\"' + pnodes[i][j].predicate + '\"'
          for ing in pnodes[i][j].pIngs:
            line += ', {}'.format(ing)

          line += '\n'

          self.logger.warn(pnodes[i][j].predicate)
          self.logger.error(len(pnodes[i][j].pIngs))
          f.write(line)


