__author__ = 'gt'

def diff_edges(graph1, graph2):
  '''
  API to find A - B, B - A : Edge set difference
  '''
  set_a = set(graph1)
  set_b = set(graph2)

  a_diff_b = list(set_a - set_b)
  b_diff_a = list(set_b - set_a)

  return list(a_diff_b), list(b_diff_a)
  pass

def common_graph_lines(graph1, graph2):
  set_a = set(graph1)
  set_b = set(graph2)

  return set_a.intersection(set_b)

def same_list(a_list, b_list):
  a_set = set(a_list)
  b_set = set(b_list)

  if(len(list(a_set - b_set)) > 0):
    return False

  if(len(list(b_set - a_set)) > 0):
    return False

  return True
  pass

if __name__ == '__main__':
  a_output = '/home/gt/Documents/UserEvaluation/AlgoA/avocado-mac-and-cheese.gv'
  b_output = '/home/gt/Documents/UserEvaluation/AlgoB/avocado-mac-and-cheese.gv'

  a_edges = []
  b_edges = []

  with open(a_output) as f_a:
    a_lines =  set(f_a.readlines())

  with open(b_output) as f_b:
    b_lines = set(f_b.readlines())

  a_out, b_out = diff_edges(a_lines, b_lines)

  if same_list(a_out, a_lines):
    print 'a reconstructed'

  if same_list(b_out, b_lines):
    print 'b reconstructed'

  pass