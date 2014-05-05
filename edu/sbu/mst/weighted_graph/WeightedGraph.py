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

    #for single top/bottom node per CC
    self.ccs_rep_top = []
    self.ccs_rep_bottom = []

    self.logger = logging.getLogger('root')
    pass

  def get_simple_components_root(self):
    """
    processes the top nodes in the connected components and returns the root node.
    Also simplifies the connected components to have one top and one bottom node
    """
    import sys
    if not self.root is None:
      return self.root

    r_min_s = sys.maxint
    r_min_p = sys.maxint
    self.ccs_rep_top = [None for i in xrange(len(self.ccs_top))]
    self.ccs_rep_bottom = [None for i in xrange(len(self.ccs_bottom))]

    root = None
    for i in xrange(len(self.ccs_top)):
      rep_min_s = sys.maxint
      rep_min_p = sys.maxint
      for j in xrange(len(self.ccs_top[i])):
        #for identifying root
        top = self.id_node_map[self.ccs_top[i][j]]
        if top.sent_num < r_min_s:
          r_min_s = top.sent_num
          r_min_p = top.pred_num
          root = self.ccs_top[i][j]
        elif top.sent_num == r_min_s:
          if top.pred_num < r_min_p:
            r_min_p = top.pred_num
            root = self.ccs_top[i][j]

        #for identifying top rep
        if top.sent_num < rep_min_s:
          rep_min_s = top.sent_num
          rep_min_p = top.pred_num
          self.ccs_rep_top[i] = self.ccs_top[i][j]
        elif top.sent_num == rep_min_s:
          if top.pred_num < rep_min_p:
            rep_min_p = top.pred_num
            self.ccs_rep_top[i] = self.ccs_top[i][j]


    #for identifying bottom rep
    for i in xrange(len(self.ccs_bottom)):
      rep_max_p = - sys.maxint
      rep_max_s = - sys.maxint
      for j in xrange(len(self.ccs_bottom[i])):
        bottom = self.id_node_map[self.ccs_bottom[i][j]]
        if bottom.snum > rep_max_s:
          rep_max_s = bottom.snum
          rep_max_p = bottom.pnum
          self.ccs_rep_bottom[i] = self.ccs_bottom[i][j]
        elif bottom.snum == rep_max_s:
          if bottom.pnum > rep_max_p:
            rep_max_p = bottom.pnum
            self.ccs_rep_bottom[i] = self.ccs_bottom[i][j]
        pass

    self.root = root

    return self.root

  def get_adj_dict(self, heuristic):
    """
    Process the representatives per component and generate the adj dictionary.
    Add ghost node at the end to facilitate edmonds.py #not sure why this is needed
    """
    import sys
    weight_heuristic = getattr(Heuristics, heuristic)

    root = self.get_simple_components_root()
    g = {}
    #len of ccs_top == len of ccs_bottom == no of ccs
    for i in xrange(len(self.ccs_rep_bottom)):
      g[ self.ccs_rep_bottom[i] ] = {}
      for j in xrange(len(self.ccs_rep_top)):

        if not i == j: #avoiding bottom to top edge within component
          #only considering edges not incident on root
          if root != self.ccs_rep_top[j]:
            wt = weight_heuristic(self.ccs_rep_bottom[i], self.ccs_rep_top[j], self.id_node_map)
            g[self.ccs_rep_bottom[i]][self.ccs_rep_top[j]] = 100 + wt

    #adding top->bottom edge within the same component
    for i in xrange(len(self.ccs_top)):
      g[self.ccs_rep_top[i]] = {self.ccs_rep_bottom[i] : 100}

    g['Ghost'] = {}
    #add dummy node:
    for i in xrange(len(self.ccs_top)):
      g['Ghost'][self.ccs_rep_bottom[i]] = sys.maxint - 1
      g['Ghost'][self.ccs_rep_top[i]] = sys.maxint - 1

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


  def connected_component(self, id):
    for i in xrange(len(self.ccs_rep_top)):
      if id == self.ccs_rep_top[i]:
        return i

    for i in xrange(len(self.ccs_rep_bottom)):
      if id == self.ccs_rep_bottom[i]:
        return i

    self.logger.error("Code should never reach here!!!")
  pass