__author__ = 'gt'
import logging
import edu.sbu.mst.MSTHeuristics as Heuristics
class WeightedGraph:
  def __init__(self, pNodes, rNodes, ccs, v_props, id_node_map):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.id_node_map = id_node_map
    self.v_props = v_props
    self.edge_list = []
    self.mst_nodes = []
    self.ccs_top = []
    self.ccs_bottom = []
    self.find_active_nodes_per_cc(ccs)
    self.root = None

    self.logger = logging.getLogger('root')
    pass

  def get_root(self):
    """
    processes the top nodes in the connected components and returns the root node
    """
    import random
    if self.root is None:
      i = random.randint(0, len(self.ccs_top) - 1)
      self.root =  str(i) + 't'

    return self.root

  def get_adj_dict(self, heuristic):
    """
    Process MST CCs to get the edge list
    edge is represented as
      [weight, from, to]
    """
    import random, sys
    # weight_heuristic = getattr(Heuristics, heuristic)

    root = self.get_root()
    g = {}
    #len of ccs_top == len of ccs_bottom == no of ccs
    for i in xrange(len(self.ccs_top)):
      g[ str(i) + 'b' ] = {}
      for j in xrange(len(self.ccs_top)):
        if not i == j:
          if i < j:
            wt = random.randint(1,100)
          else:
            wt = sys.maxint - 1

          #skipping all edges leading to root
          if root != str(j) + 't':
            g[str(i) + 'b'][str(j) + 't'] = wt

    for i in xrange(len(self.ccs_top)):
      g[str(i) + 't'] = {str(i) + 'b' : -1000}

    g['Ghost'] = {}
    #add dummy node:
    for i in xrange(len(self.ccs_top)):
      g['Ghost'][str(i) + 't'] = sys.maxint - 1
      g['Ghost'][str(i) + 'b'] = sys.maxint - 1

    return g
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

  def find_active_nodes_per_cc(self, g_ccs):
    """
    Identify nodes with in/out degree zero per CC
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