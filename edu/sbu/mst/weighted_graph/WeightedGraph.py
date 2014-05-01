__author__ = 'gt'
import logging
import edu.sbu.mst.MSTHeuristics as Heuristics
class WeightedGraph:
  def __init__(self, pNodes, rNodes, adj_list, ccs, v_props, id_node_map, heuristic):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.id_node_map = id_node_map
    self.v_props = v_props
    self.edge_list = []
    self.mst_nodes = []
    self.ccs_top = []
    self.ccs_bottom = []
    self.identify_ccs(ccs)
    self.get_edge_list(heuristic)


    self.logger = logging.getLogger('root')
    pass

  def get_edge_list(self, heuristic):
    """
    Process MST CCs to get the edge list
    edge is represented as
      [weight, from, to]
    """
    weight_heuristic = getattr(Heuristics, heuristic)
    for i in xrange(len(self.ccs_bottom)-1):
      for j in xrange(i+1, len(self.ccs_bottom)):
        #i before j
        #edge from i bottom to all j tops
        for k in xrange(len(self.ccs_top[j])):
          for l in xrange(len(self.ccs_bottom[i])):

            self.edge_list.append((weight_heuristic(self.ccs_bottom[i][l], self.ccs_top[j][k], self.id_node_map),self.ccs_bottom[i][l],self.ccs_top[j][k]))

        #j before i
        #edge from j bottom to all i tops
        for k in xrange(len(self.ccs_top[i])):
          for l in xrange(len(self.ccs_bottom[j])):
            self.edge_list.append((weight_heuristic(self.ccs_bottom[j][l], self.ccs_top[i][k], self.id_node_map), self.ccs_bottom[j][l], self.ccs_top[i][k]))

    pass

  def print_edges(self):
    # self.logger.error(len(self.edge_list))
    adj_list = {}
    for i in xrange(len(self.edge_list)):
      if self.edge_list[i][1] in adj_list.keys():
        adj_list[self.edge_list[i][1]][self.edge_list[i][2]] = self.edge_list[i][0]
      else:
        adj_list[self.edge_list[i][1]] = {self.edge_list[i][2] : self.edge_list[i][0]}
      self.logger.error("{} - > {} : {}".format(self.edge_list[i][1],self.edge_list[i][2],self.edge_list[i][0]))

    # a = set(adj_list.keys())
    # b = set(['T2','T3', 'T4'])
    # if len(set.intersection(a,b)) == 3 and len(a) == 3:
    #   self.logger.error("here")
    # for k in adj_list.keys():
    #   for k1 in adj_list[k].keys():
    #     self.logger.error("{} -> {}[label={}, color=cyan, style=dashed]".format(k,k1,adj_list[k][k1]))

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
      self.ccs_bottom.append([])
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
            self.ccs_bottom[-1].append(ccs[i][j])
            pass
          pass

    return

  pass