__author__ = 'gt'
adj_list = [
  [8],
  [2,9],
  [],
  [],
  [],
  [0],
  [0],
  [1],
  [1],
  [2],
  [],
  [3],
  [3],
  [4],
  [4]
  ]

v_props = [
    #cc, s, d
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0],
    [-1,0,0]
  ]

def dfs(node, tkr, ccs):
  global v_props
  # global adj_list #not needed for reading
  v_props[node][0] = tkr
  for neighbor in adj_list[node]:
    if v_props[neighbor][0] == -1: #if node not visited
      ccs[tkr] = set.union(ccs[tkr], set([neighbor]))
      v_props[neighbor][0] = tkr
      ccs = dfs(neighbor, tkr, ccs)

  return ccs


def get_connected_components(adj_list):
  tkr = 0
  ccs = []
  # global v_props # no need for reading


  for node in xrange(len(v_props)):
    if v_props[node][0] == -1:
      ccs.append(set([node]))
      ccs = dfs(node, tkr, ccs)
      tkr += 1

  return ccs
  pass

def get_top_bottom_nodes(adj_list):
  for i in xrange(len(adj_list)):
    for neighbor in adj_list[i]:
      v_props[i][1] = 1
      v_props[neighbor][2] = 1
  pass

def directed_to_undirected(adj_list):
  ret = [[] for i in xrange(len(adj_list)) ]
  for i in xrange(len(adj_list)):
    for neighbor in adj_list[i]:
      ret[i].append(neighbor)
      ret[neighbor].append(i)

  return ret



def main():

    # (5,0),
    # (6,0),
    # (7,1),
    # (8,1),
    # (0,8),
    # (9,2),
    # (1,9),
    # (1,2),
    # (11,3),
    # (12,3),
    # (13,4),
    # (14,4)
    # ]
  global adj_list
  global v_props

  get_top_bottom_nodes(adj_list)

  adj_list = directed_to_undirected(adj_list)

  ccs = get_connected_components(adj_list)

  for cc in ccs:
    print cc

  for i in xrange(len(v_props)):
    if v_props[i][1] == 0 and v_props[i][2] == 1:
      print ' {} : bottom ; cc = {}'.format(i, v_props[i][0])
    elif v_props[i][1] == 1 and v_props[i][2] == 0:
      print ' {} : top ; cc = {}'.format(i, v_props[i][0])
    elif v_props[i][1] == 1 and v_props[i][1] == 1:
      print ' {} : middle ; cc = {}'.format(i, v_props[i][0])
    else:
      print 'null instant replaced with a pred (shell coref) node number {} ; cc {}'.format(i, v_props[i][0])

  pass

if __name__ == '__main__':
  main()