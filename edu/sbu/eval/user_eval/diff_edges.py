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
  import os
  files = os.listdir('/home/gt/Documents/UserEvaluation/AlgoA/')

  for file in files:
    print 'processing ' + file
    a_output = '/home/gt/Documents/UserEvaluation/AlgoA/' + file
    b_output = '/home/gt/Documents/UserEvaluation/AlgoB/' + file

    a_edges = []
    b_edges = []

    with open(a_output) as f_a:
      a_lines =  set(f_a.readlines())

    with open(b_output) as f_b:
      b_lines = set(f_b.readlines())

    a_out, b_out = diff_edges(a_lines, b_lines)

    if(len(a_out) != len(b_out)):
      print 'differing in length'

    a_out.sort()
    b_out.sort()
    for i in xrange(len(a_out)):
      start_a = a_out[i].split('->')[0].strip()
      start_b = b_out[i].split('->')[0].strip()

      print a_out[i]
      print b_out[i]
      if start_a != start_b:
        print 'different starting point for edges'


    pass