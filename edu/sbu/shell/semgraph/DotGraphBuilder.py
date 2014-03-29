__author__ = 'gt'
import codecs
encoding = 'UTF-8'

class DotGraphBuilder:

  def __init__(self):
    self.pred_properties = {'shape':'diamond','style':'filled','fillcolor':'gray'}
    self.arg1_props = {}
    self.arg2_props = {'shape':'rectangle','style':'filled','fillcolor':'goldenrod'}
    self.graph_lines = []
    self.node_list = {}
    self.node_num = 0

  def process_pnodes(self, pnodes):
    pass

  def process_rnodes(self, rnodes):
    pass

  def get_edges(self):
    pass

  def get_header(self):
    self.graph_lines.append('Digraph G {')

  def get_footer(self):
    self.graph_lines.append('};')

  def write_gv(self, pnodes, rnodes, file_name):
    self.get_header()
    self.process_pnodes(pnodes)
    self.process_rnodes(rnodes)
    self.get_edges()
    self.get_footer()

    with codecs.open(file_name, 'w', encoding) as f:
      for line in self.graph_lines:
        f.write(line+'\n')