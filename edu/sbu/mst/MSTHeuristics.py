__author__ = 'gt'

import math

def random(pNode_id, rNode_id, id_node_map):
  from random import randint
  return randint(1,100)
  pass


def order_close_together(pNode_id, rNode_id, id_node_map):
  pNode = id_node_map[pNode_id]
  rNode = id_node_map[rNode_id]

  #arbitrarily large value to ignore the edges
  #assume sentences can never diff by more than 29 to fix this
  #large value (assumed  2^29)
  if pNode.snum > rNode.sent_num:
    return 10000000000

  if pNode.snum == rNode.sent_num:
    if pNode.pnum > rNode.pred_num:
      return 10000000000

  return math.pow(2, rNode.sent_num - pNode.snum)

  pass