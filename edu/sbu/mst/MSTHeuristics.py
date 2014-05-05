__author__ = 'gt'

import math
import sys

def random(pNode_id, rNode_id, id_node_map):
  from random import randint
  return randint(1,100)
  pass


def order_close_together(pNode_id, rNode_id, id_node_map):
  pNode = id_node_map[pNode_id]
  rNode = id_node_map[rNode_id]

  #arbitrarily large value to penalize the back edges
  #note about maxint in python: Need to use with caution
  #as sometimes when numbers exceed this limit, they get promoted as long and so on
  #Ref: http://stackoverflow.com/a/7604981/1019673
  if pNode.snum > rNode.sent_num:
    return sys.maxint - 10

  if pNode.snum == rNode.sent_num:
    if pNode.pnum > rNode.pred_num:
      return sys.maxint - 10

  return math.pow(2, rNode.sent_num - pNode.snum)

  pass