__author__ = 'gt'

import math
import sys
from edu.sbu.shell.semgraph.RNode import RNode
from edu.sbu.shell.semgraph.PNode import PNode

def random(pNode_id, rNode_id, id_node_map):
  from random import randint
  return randint(1,100)
  pass


def order_close_together(pNode_id, Node_id, id_node_map, pNodes, rNodes):
  pNode = id_node_map[pNode_id]
  Node = id_node_map[Node_id]
  if isinstance(Node,RNode):
    return order_close_together_pr(pNode,Node,id_node_map,pNodes,rNodes)
  else:
    return order_close_together_pp(pNode,Node,id_node_map,pNodes,rNodes)

def order_close_together_pp(pNode, pNode2, id_node_map, pNodes, rNodes):

  #arbitrarily large value to penalize the back edges
  #note about maxint in python: Need to use with caution
  #as sometimes when numbers exceed this limit, they get promoted as long and so on
  #Ref: http://stackoverflow.com/a/7604981/1019673
  if pNode.snum > pNode2.snum:
    return sys.maxint - 10

  if pNode.snum == pNode2.snum:
    if pNode.pnum > pNode2.pnum:
      return sys.maxint - 10

  dist = len(pNodes[pNode.snum]) - pNode.pnum  - 1#accounting for zero based index
  for i in xrange(pNode.snum + 1, pNode2.snum):
    dist += len(pNodes[pNode.snum])
    pass

  dist += pNode2.pnum

  if dist < 0:
    print 'MST Heuristic bug: dist negative'

  return math.pow(2, dist)

  pass

def order_close_together_pr(pNode, rNode, id_node_map, pNodes, rNodes):
  #arbitrarily large value to penalize the back edges
  #note about maxint in python: Need to use with caution
  #as sometimes when numbers exceed this limit, they get promoted as long and so on
  #Ref: http://stackoverflow.com/a/7604981/1019673
  if pNode.snum > rNode.sent_num:
    return sys.maxint - 10

  if pNode.snum == rNode.sent_num:
    if pNode.pnum > rNode.pred_num:
      return sys.maxint - 10

  dist = len(pNodes[pNode.snum]) - pNode.pnum  - 1#accounting for zero based index
  for i in xrange(pNode.snum + 1, rNode.sent_num):
    dist += len(pNodes[pNode.snum])
    pass

  dist += rNode.pred_num

  if dist < 0:
    print 'MST Heuristic bug: dist negative'

  return math.pow(2, dist)

  pass