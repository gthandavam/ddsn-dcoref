__author__ = 'gt'
import logging
import random
class WeightedGraph:
  def __init__(self, pNodes, rNodes, adj_list, ccs, v_props, id_node_map):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.id_node_map = id_node_map
    self.v_props = v_props
    self.edge_list = []
    self.mst_nodes = []
    self.ccs_top = []
    #one bottom node per cc - Incorrect assumption
    self.ccs_bottom = []
    self.identify_ccs(ccs)
    self.get_edge_list()

    self.logger = logging.getLogger('root')
    pass

  def get_edge_list(self):
    """
    Process MST CCs to get the edge list
    edge is represented as
      [from, to, weight]
    """
    for i in xrange(len(self.ccs_bottom)):
      for j in xrange(len(self.ccs_bottom)):
        if i == j:
          continue

        #i before j
        #edge from i bottom to all j tops
        for k in xrange(len(self.ccs_top[j])):

          self.edge_list.append([self.ccs_bottom[i],self.ccs_top[j][k],random.randint(1,100)])

        #j before i
        #edge from j bottom to all i tops
        for k in xrange(len(self.ccs_top[i])):
          self.edge_list.append([self.ccs_bottom[j], self.ccs_top[i][k], random.randint(1,100)])

    pass

  def print_edges(self):
    for i in xrange(len(self.edge_list)):
      self.logger.error("{} - > {} : {}".format(self.edge_list[i][0],self.edge_list[i][1],self.edge_list[i][2]))

  def identify_ccs(self, g_ccs):
    """
    Transform DCoref CCs to MST CCs
    """
    ccs = []
    #hack to work with list indices
    for i in xrange(len(g_ccs)):
      ccs.append([x for x in iter(g_ccs[i])])


    for i in xrange(len(ccs)):
      if len(ccs[i]) == 1:
        #Left over implicit args form isolated cc
        #dont process
        continue

      self.ccs_top.append([])
      # self.ccs_bottom.append([])
      for j in xrange(len(ccs[i])):
        #top and bottom nodes have diff flags
        if not (self.v_props[ccs[i][j]][1] == self.v_props[ccs[i][j]][2]):
          #process the top or bottom nodes
          if self.v_props[ccs[i][j]][1] == 1:
            #top node
            self.mst_nodes.append(ccs[i][j])
            self.ccs_top[-1].append(ccs[i][j])
            pass
          else:
            #bottom node
            #only one bottom node per cc
            self.mst_nodes.append(ccs[i][j])
            self.ccs_bottom.append(ccs[i][j])
            pass
          pass

    return

  def get_vertex_list(self):
    """
    process pNodes and rNodes to get island vertices
    """
    ret = []
    return ret

  def add_edges(self, edge_list):
    self.edge_list.extend(edge_list)

  def identify_islands(self):
    pass

  def add_edges_between_islands(self, island1, island2):
    pass

  pass