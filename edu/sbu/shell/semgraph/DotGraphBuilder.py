__author__ = 'gt'
import codecs
import logging
from edu.sbu.shell.semgraph.RNode import RNode
encoding = 'UTF-8'

class DotGraphBuilder:

  def __init__(self):
    #TODO: refactor the class based on extensible number and type of arguments per predicate
    self.pred_props = {'shape':'oval','style':'filled','fillcolor':'gray'}
    self.arg1_props = {}
    self.arg2_props = {}
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
    self.Ghost = 'Bon appetit!'
    self.debug = True


  def process_pnodes(self, pnodes):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        #assuming pred node can never be null
        self.pred_node_list[(i,j)] = 'T' + str(self.node_num)

        self.id_node_map[self.pred_node_list[(i,j)]] = pnodes[i][j]
        pnodes[i][j].id = self.pred_node_list[(i,j)]

        # line = '{}[label=\"{}\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate)
        # # line = self.pred_node_list[(i,j)] + '[label=\"' + pnodes[i][j].predicate + '\"'
        # for key in self.pred_props.keys():
        #   line += ', {}={}'.format(key,self.pred_props[key])
        #
        # line += ']'
        # self.graph_lines.append(line)
        self.node_num += 1
    pass

  def print_pnodes(self, pnodes, arbo_edges):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        if self.debug:
          line = '{}[label=\"{} ({},sent={})\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate, pnodes[i][j].id, pnodes[i][j].snum)
        else:
          line = '{}[label=\"{}\"'.format(self.pred_node_list[(i,j)], pnodes[i][j].predicate)
        # line = self.pred_node_list[(i,j)] + '[label=\"' + pnodes[i][j].predicate + '\"'
        for key in self.pred_props.keys():
          line += ', {}={}'.format(key,self.pred_props[key])

        line += '];#{},{}'.format(pnodes[i][j].span_start, pnodes[i][j].span_end)
        self.graph_lines.append(line)
        # self.node_num += 1
    pass

  def process_rnodes(self, rnodes):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        #TODO: dont fix argument slots : process based on arg_type in RNode
        for k in xrange(1,3):
          if rnodes[i][j][k]==None:
            continue
          node_id = 'T'+str(self.node_num)
          self.id_node_map[node_id] = rnodes[i][j][k]
          rnodes[i][j][k].id = node_id
          if not rnodes[i][j][k].is_null:

            # line = node_id
            if rnodes[i][j][k].arg_type == 'arg1':
              self.arg1_node_list[(i,j,k)] = node_id
              # line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              # for key in self.arg1_props.keys():
              #   line +=', {}={}'.format(key, self.arg1_props[key])
              # line += ']'
            elif rnodes[i][j][k].arg_type == 'arg2':
              self.arg2_node_list[(i,j,k)] = node_id
              # line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              # for key in self.arg2_props.keys():
              #   line +=', {}={}'.format(key, self.arg2_props[key])
              # line += ']'
            else:
              self.logger.error('unknown arg type')
              continue

            # self.graph_lines.append(line)
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

  def print_rnodes(self, rnodes, arbo_edges):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        #TODO: dont fix argument slots : process based on arg_type in RNode
        for k in xrange(1,3):
          if rnodes[i][j][k]==None:
            continue
          if not rnodes[i][j][k].is_null:

            line = rnodes[i][j][k].id
            if rnodes[i][j][k].arg_type == 'arg1':
              if self.debug:
                line += '[label=\"{} ({}, sent={})\"'.format(rnodes[i][j][k].raw_text, rnodes[i][j][k].id, rnodes[i][j][k].sent_num)
              else:
                line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              for key in self.arg1_props.keys():
                line +=', {}={}'.format(key, self.arg1_props[key])
              line += ']'
            elif rnodes[i][j][k].arg_type == 'arg2':
              if self.debug:
                line += '[label=\"{} ({},sent={})\"'.format(rnodes[i][j][k].raw_text, rnodes[i][j][k].id, rnodes[i][j][k].sent_num)
              else:
                line += '[label=\"{}\"'.format(rnodes[i][j][k].raw_text)
              for key in self.arg2_props.keys():
                line +=', {}={}'.format(key, self.arg2_props[key])
              line += ']'
            else:
              self.logger.error('unknown arg type')
              continue

            line += ';#{},{}'.format(rnodes[i][j][k].span_start, rnodes[i][j][k].span_end)
            self.graph_lines.append(line)

          # self.node_num += 1
    self.graph_lines.append("Ghost[label=\"{}\"];#{},{}".format(self.Ghost, -1, -1))
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
          if rnodes[i][j][k]==None or rnodes[i][j][k].text=="Ghost":
            continue
          if rnodes[i][j][k].is_null:
            #implicit arg edge
            if len(rnodes[i][j][k].shell_coref) != 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              edge_type = rnodes[i][j][k].shell_coref[0][1]
              pred_node  = self.pred_node_list[(i,j)]
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
            # self.logger.error(line)
            self.add_to_adj_list(arg_node, self.pred_node_list[(i,j)])

            if len(rnodes[i][j][k].shell_coref) > 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              edge_type = rnodes[i][j][k].shell_coref[0][1]

              # self.logger.error(line + ' shell')
              self.add_to_adj_list(shell_node, arg_node)

    pass

  def print_edges(self, rnodes, arbo_edges):
    for i in xrange(len(rnodes)):
      for j in xrange(len(rnodes[i])):
        for k in xrange(1,3):
          if rnodes[i][j][k]==None or rnodes[i][j][k].text=="Ghost":
            continue
          if rnodes[i][j][k].is_null:
            #implicit arg edge
            if len(rnodes[i][j][k].shell_coref) != 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              edge_type = rnodes[i][j][k].shell_coref[0][1]
              pred_node  = self.pred_node_list[(i,j)]
              if shell_node not in arbo_edges or pred_node not in arbo_edges[shell_node]:
                continue
              if self.debug:
                line = '{} -> {}[label=\"{}({})\"'.format(shell_node, pred_node, edge_type,arbo_edges[shell_node][pred_node])

                for prop in self.edge_props[edge_type]:
                  if prop=="label":
                    continue
                  line += ', {}={}'.format(prop, self.edge_props[edge_type][prop])
                line += '];'

              else:
                line = '{} -> {};'.format(shell_node, pred_node)

              self.graph_lines.append(line)

          else:
            if rnodes[i][j][k].arg_type == 'arg1':
              arg_node = self.arg1_node_list[(i,j,k)]
            elif rnodes[i][j][k].arg_type == 'arg2':
              arg_node = self.arg2_node_list[(i,j,k)]
            else:
              self.logger.warn('unknown arg type')
            if arg_node not in arbo_edges or self.pred_node_list[(i,j)] not in arbo_edges[arg_node]:
              continue
            if self.debug:
              line =  '{} -> {}[label=\"{}({})\"];'.format(arg_node, self.pred_node_list[(i,j)], 'SRL',arbo_edges[arg_node][self.pred_node_list[(i,j)]])
            else:
              # line =  '{} -> {}[label={}]'.format(arg_node, self.pred_node_list[(i,j)], 'SRL')
               line =  '{} -> {};'.format(arg_node, self.pred_node_list[(i,j)])
            self.graph_lines.append(line)

            if len(rnodes[i][j][k].shell_coref) > 0:
              shell_node = self.pred_node_list[rnodes[i][j][k].shell_coref[0][0]]
              if shell_node not in arbo_edges or arg_node not in arbo_edges[shell_node]:
                continue
              edge_type = rnodes[i][j][k].shell_coref[0][1]

              if self.debug:
                line = '{} -> {}[label=\"{}({})\"'.format(shell_node, arg_node, edge_type,arbo_edges[shell_node][arg_node])
                for prop in self.edge_props[edge_type]:
                  if prop=="label":
                    continue
                  line += ', {}={}'.format(prop, self.edge_props[edge_type][prop])
                line += '];'
              else:
                line = '{} -> {};'.format(shell_node, arg_node)

              self.graph_lines.append(line)
    pass

  def get_header(self):
    self.graph_lines.insert(0, 'Digraph G {')

  def get_footer(self):
    import sys
    if sys.platform != 'linux2':
      self.graph_lines.append('}')
    else:
      self.graph_lines.append('};')

  def get_edge_list_mst(self, pnodes, rnodes):
    self.process_pnodes(pnodes)
    self.process_rnodes(rnodes)
    for key in self.id_node_map.keys():
      self.adj_list[key] = []

    self.get_edges(rnodes)

    return self.adj_list, self.id_node_map

  def write_gv(self, pnodes, rnodes, arbo_edges, file_name):
    self.get_header()
    self.print_pnodes(pnodes,arbo_edges)
    self.print_rnodes(rnodes,arbo_edges)
    self.print_edges(rnodes,arbo_edges)
    self.get_cc_edges(pnodes,arbo_edges)
    self.get_footer()

    with codecs.open(file_name, 'w') as f:
      for line in self.graph_lines:
        f.write(line+'\n')

  def get_cc_edges(self, pnodes, arbo_edges):
    for i in xrange(len(pnodes)):
      for j in xrange(len(pnodes[i])):
        # if len(pnodes[i][j].cc_edge) > 0:
        for k in xrange(len(pnodes[i][j].cc_edge)):
          start_node = self.pred_node_list[(i,j)]
          target_node = self.id_node_map[pnodes[i][j].cc_edge[k]]
          line = target_node.id

          if isinstance(target_node, RNode):

            if target_node.is_null:
              target_node = self.pred_node_list[(target_node.sent_num,target_node.pred_num)]
            else:
              if target_node.arg_type == 'arg1':
                target_node = self.arg1_node_list[(target_node.sent_num,target_node.pred_num, 1)]
              elif target_node.arg_type == 'arg2':
                target_node = self.arg2_node_list[(target_node.sent_num,target_node.pred_num, 2)]
              else:
                target_node = target_node.text
                self.logger.error('Unknown arg type')
          else:
            target_node = target_node.id

          if self.debug:
            #temporary bug fix - TODO: Is it good to assume that start and target node will always be in arbor_edges ?
            if start_node in arbo_edges and target_node in arbo_edges[start_node]:
              temp_wt = arbo_edges[start_node][target_node]
            else:
              temp_wt = 'CC No wt'

            line = '{} -> {} [label=\"{}({})\"'.format(start_node, target_node, 'CC', temp_wt)
            for prop in self.edge_props['CC'].keys():
              if prop=="label":
                continue
              line += ',{}={}'.format(prop, self.edge_props['CC'][prop])

            line += '];'

          else:
            line = '{} -> {};'.format(start_node, target_node)


          self.graph_lines.append(line)

          pass
        pass