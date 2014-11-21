__author__ = 'gt'
import logging
import edu.sbu.mst.MSTHeuristics as Heuristics
from edu.sbu.shell.semgraph.RNode import RNode
from edu.sbu.shell.semgraph.PNode import PNode
import sys, math
class WeightedGraph:

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

    self.logger = logging.getLogger('root')

    self.Wwt = 0
    self.Warg = 1
    pass

  # --- get graph plus ghost node with incoming edges from all connected components.
  # graph will serve as an input to "upside-down" arborescence
  def get_adj_ghost_graph(self, heuristic):
    weight_heuristic = getattr(Heuristics, heuristic)

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


    g['Ghost'] = {}
    for i in range(len(self.ccs_bottom)):
      for p in range(len(self.ccs_bottom[i])):
        node1 = self.id_node_map[self.ccs_bottom[i][p]]
        # consider only nodes with 0 out degree
        if len(g[node1.id])>0:
          continue
        g[node1.id] = {}

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

            arg_probability = self.recipe_stats.getPredPredProb(node1,input_node,input_node2,node2,input2_node)
            g[node1.id][node2.id] = self.Wwt*wt + self.Warg*arg_probability


        for j in range(len(self.rNodes)):
          for q in range(len(self.rNodes[j])):
            for k in range(2):
              node2 = self.rNodes[j][q][k+1]
              # node2 = self.id_node_map[self.ccs_top[j][q]]
              if not isinstance(node2,RNode) or (isinstance(node2, RNode) and node2.is_null):
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
        # @Polina: We always have null nodes - so there cannot be a node with in and out degree both 0

        # Covers cases 0,0; 1,0 and 0,1
        if self.v_props[ccs[i][j]][1] + self.v_props[ccs[i][j]][2] < 2:
          #process the top or bottom nodes
          if self.v_props[ccs[i][j]][1] == 1:
            self.ccs_top[-1].append(ccs[i][j])
            pass
          else:
            #bottom node
            self.ccs_bottom[-1].append(ccs[i][j])
            pass
          pass

    return


  def connected_component(self, id):
    if id=='Ghost':
      return -1

    for i in xrange(len(self.ccs)):
      if id in self.ccs[i]:
        return i

    self.logger.error("Code should never reach here!!!")
  pass
