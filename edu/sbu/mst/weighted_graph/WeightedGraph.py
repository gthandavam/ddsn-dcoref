__author__ = 'gt'
import logging
import edu.sbu.mst.MSTHeuristics as Heuristics
from edu.sbu.shell.semgraph.RNode import RNode
from edu.sbu.shell.semgraph.PNode import PNode
import sys, math
class WeightedGraph:
  Wwt = 0
  Warg = 1
  def __init__(self, pNodes, rNodes, ccs, v_props, adj_list, id_node_map, r_stats):
    self.pNodes = pNodes
    self.rNodes = rNodes
    self.id_node_map = id_node_map
    self.v_props = v_props
    self.adj_list = adj_list
    self.edge_list = []
    self.mst_nodes = []
    self.ccs_top = []
    self.ccs_bottom = []
    self.ccs = ccs
    self.find_active_nodes_per_cc(ccs)
    self.root = None
    self.recipe_stats = r_stats

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
    # import sys
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
            wt = weight_heuristic(self.ccs_rep_bottom[i], self.ccs_rep_top[j], self.id_node_map, self.pNodes, self.rNodes)
            g[self.ccs_rep_bottom[i]][self.ccs_rep_top[j]] = wt

    #adding top->bottom edge within the same component
    for i in xrange(len(self.ccs_top)):
      g[self.ccs_rep_top[i]] = {self.ccs_rep_bottom[i] : -100}

    # g['Ghost'] = {}
    # #add dummy node:
    # for i in xrange(len(self.ccs_top)):
    #   g['Ghost'][self.ccs_rep_bottom[i]] = sys.maxint - 1
    #   g['Ghost'][self.ccs_rep_top[i]] = sys.maxint - 1

    return g
    pass

  # --- get graph plus ghost node with incoming edges from all connected components.
  # graph will serve as an input to "upside-down" arborescence
  def get_adj_ghost_graph(self, heuristic):
    weight_heuristic = getattr(Heuristics, heuristic)

    root = self.get_simple_components_root()
    g = {}
    reverse_g = {}
    for node in self.adj_list:
      g[node] = {}
      for ch in self.adj_list[node]:
        g[node][ch] = -100
        if ch not in reverse_g:
          reverse_g[ch] = {}
        reverse_g[ch][node] = -100

    for node in self.adj_list:
      node_obj = self.id_node_map[node]
      input_node = self.recipe_stats.findInputArgument(node_obj, reverse_g,self.id_node_map)
      input_node2 = self.recipe_stats.findInputArgument2(node_obj, reverse_g,self.id_node_map)
      for ch in self.adj_list[node]:
        ch_obj = self.id_node_map[ch]
        ch_input_node = self.recipe_stats.findInputArgument(ch_obj, reverse_g,self.id_node_map)
        if isinstance(node_obj,PNode) and isinstance(ch_obj,RNode):
          score = self.recipe_stats.getPredOuputArgProb(node_obj,input_node,input_node2,ch_obj)
          g[node][ch] = score
          reverse_g[ch][node] = score
        if isinstance(node_obj,PNode) and isinstance(ch_obj,PNode):
          score = self.recipe_stats.getPredPredProb(node_obj,input_node,input_node2,ch_obj,ch_input_node)
          g[node][ch] = score
          reverse_g[ch][node] = score

    # if True:
    #   return g

    # #len of ccs_top == len of ccs_bottom == no of ccs
    # for i in xrange(len(self.ccs_bottom)):
    #   for b in xrange(len(self.ccs_bottom[i])):
    #     g[ b ] = {}
    #     for j in xrange(len(self.ccs_top)):
    #       if not i == j: #avoiding bottom to top edge within component
    #         for t in xrange(len(self.ccs_top[j])):
    #           #only considering edges not incident on root
    #           # also disallow edges from bottom nodes of later sentences to top nodes of previous sentences
    #           bottom = self.id_node_map[self.ccs_bottom[i][b]]
    #           top = self.id_node_map[self.ccs_top[j][t]]
    #           if root != self.ccs_rep_top[j] and bottom.snum < top.sent_num:
    #             wt = weight_heuristic(self.ccs_rep_bottom[i], self.ccs_rep_top[j], self.id_node_map, self.pNodes, self.rNodes)
    #             g[self.ccs_rep_bottom[i]][self.ccs_rep_top[j]] = wt

    # #len of ccs_top == len of ccs_bottom == no of ccs
    # for i in xrange(len(self.ccs_bottom)):
    #   for b in xrange(len(self.ccs_bottom[i])):
    #     g[ b ] = {}
    #     bottom = self.id_node_map[self.ccs_bottom[i][b]]
    #     for j in xrange(len(self.ccs)):
    #       if not i == j: #avoiding bottom to top edge within component
    #         for t in self.ccs[j]:
    #           top = self.id_node_map[t]
    #           if isinstance(top,PNode) and bottom.snum < top.snum:
    #           # if root != self.ccs_rep_top[j] and bottom.snum < top.sent_num:
    #             wt = weight_heuristic(self.ccs_rep_bottom[i], t, self.id_node_map, self.pNodes, self.rNodes)
    #             # g[self.ccs_rep_bottom[i]][t] = wt
    #             g[self.ccs_bottom[i][b]][t] = wt
    #           elif isinstance(top,RNode) and bottom.snum < top.sent_num and top.arg_type!='arg2':
    #           # if root != self.ccs_rep_top[j] and bottom.snum < top.sent_num:
    #           #   wt = weight_heuristic(self.ccs_rep_bottom[i], self.ccs_rep_top[j], self.id_node_map, self.pNodes, self.rNodes)
    #             wt = weight_heuristic(self.ccs_rep_bottom[i], t, self.id_node_map, self.pNodes, self.rNodes)
    #             # g[self.ccs_rep_bottom[i]][t] = wt
    #             g[self.ccs_bottom[i][b]][t] = wt

    # #adding top->bottom edge within the same component
    # for i in xrange(len(self.ccs_top)):
    #   g[self.ccs_rep_top[i]] = {self.ccs_rep_bottom[i] : -100}

    g['Ghost'] = {}
    # for i in range(len(self.pNodes)):
    #   for p in range(len(self.pNodes[i])):
    for i in range(len(self.ccs_bottom)):
      for p in range(len(self.ccs_bottom[i])):
        node1 = self.id_node_map[self.ccs_bottom[i][p]]
        # consider only nodes with 0 out degree
        if len(g[node1.id])>0:
          continue
        g[node1.id] = {}
        # g[node1.id]['Ghost'] = sys.maxint - 1
        g[node1.id]['Ghost'] = -0.0000000000001
        # extract input argument of type arg1
        input_node = self.recipe_stats.findInputArgument(node1,reverse_g,self.id_node_map)
        input_node2 = self.recipe_stats.findInputArgument2(node1,reverse_g,self.id_node_map)
        # Predicate-Predicate edges
        for j in range(len(self.pNodes)):
          for q in range(len(self.pNodes[j])):
            # if i==j and p==q:
            #   continue
            node2 = self.pNodes[j][q]
            if node1.id == node2.id:
              continue
            if node1==node2 or node1.snum>node2.snum or node1.snum==node2.snum and node1.pnum>node2.pnum:
              continue
            wt = weight_heuristic(node1.id, node2.id, self.id_node_map, self.pNodes, self.rNodes)
            input2_node = self.recipe_stats.findInputArgument(node2,reverse_g,self.id_node_map)
            if node1.id=="T0" and node2.id=="T2":
                pass
            arg_probability = self.recipe_stats.getPredPredProb(node1,input_node,input_node2,node2,input2_node)
            g[node1.id][node2.id] = self.Wwt*wt + self.Warg*arg_probability
        # Predicate-Argument edges
        # for j in range(len(self.ccs_top)):
        for j in range(len(self.rNodes)):
          # skip arguments from the same connected component - temporally off
          # if i==j:
          #   continue
          # for q in range(len(self.ccs_top[j])):
          for q in range(len(self.rNodes[j])):
            for k in range(2):
              node2 = self.rNodes[j][q][k+1]
              # node2 = self.id_node_map[self.ccs_top[j][q]]
              if not isinstance(node2,RNode) or len(node2.shell_coref)>0 and node2.shell_coref[0][1]!="ArgString":
                continue
              # # consider only argument nodes with 0 in degree
              # if node2.id in reverse_g and len(reverse_g[node2.id])>0:
              #   continue
              if node1.snum>node2.sent_num or node1.snum==node2.sent_num and node1.pnum>=node2.pred_num:
                continue
              wt = weight_heuristic(node1.id, node2.id, self.id_node_map, self.pNodes, self.rNodes)
              # probability of argument being the output of the predicate
              arg_probability = self.recipe_stats.getPredOuputArgProb(node1,input_node,input_node2,node2)
              g[node1.id][node2.id] = self.Wwt*wt + self.Warg*arg_probability

    # # adding Ghost node
    # g['Ghost'] = {}
    # # connect all bottom nodes to Ghost node
    # for i in xrange(len(self.ccs_bottom)):
    #   for j in xrange(len(self.ccs_bottom[i])):
    #     g[self.ccs_bottom[i][j]]['Ghost'] = sys.maxint - 1

    # g['Ghost'] = {}
    # #add dummy node:
    # for i in xrange(len(self.ccs_top)):
    #   g['Ghost'][self.ccs_rep_bottom[i]] = sys.maxint - 1
    #   g['Ghost'][self.ccs_rep_top[i]] = sys.maxint - 1

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
        self.mst_nodes.append(ccs[i][j])
        #top and bottom nodes have diff flags (different in and out degree)
        # @Ganesa: what about components with a single node? in and out degree are both 0
        # if not (self.v_props[ccs[i][j]][1] == self.v_props[ccs[i][j]][2]):
        # Covers cases 0,0; 1,0 and 0,1
        if self.v_props[ccs[i][j]][1] + self.v_props[ccs[i][j]][2] < 2:
          #process the top or bottom nodes
          if self.v_props[ccs[i][j]][1] == 1:
            #top node
            # self.mst_nodes.append(ccs[i][j])
            self.ccs_top[-1].append(ccs[i][j])
            pass
          else:
            #bottom node
            #only one bottom node per cc
            # self.mst_nodes.append(ccs[i][j])
            self.ccs_bottom[-1].append(ccs[i][j])
            pass
          pass

    return


  def connected_component(self, id):
    if id=='Ghost':
      return -1
    # for i in xrange(len(self.ccs_rep_top)):
    #   if id == self.ccs_rep_top[i]:
    #     return i
    #
    # for i in xrange(len(self.ccs_rep_bottom)):
    #   if id == self.ccs_rep_bottom[i]:
    #     return i

    for i in xrange(len(self.ccs)):
      if id in self.ccs[i]:
        return i

    self.logger.error("Code should never reach here!!!")
  pass
