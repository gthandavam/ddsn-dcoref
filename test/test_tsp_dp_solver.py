__author__ = 'gt'

from edu.sbu.eval.so.tsp.tsp_adapter.tsp_instance import tsp_dyn_solver



if __name__ == '__main__':
  input = [[0,100,1,50], [10,0,2,5], [1000,1,0,100], [1,20,30,0]]

  print input

  res = tsp_dyn_solver(input)

  for j in xrange(1,len(input)):
    input[0][:], input[j][:] = input[j][:], input[0][:]
    input[:][0], input[:][j] = input[:][j], input[:][0]
    res1 = tsp_dyn_solver(input)
    #swap in the result
    print res1
    for k in xrange(len(res1)):
      if res1[1][k] == 0:
        res1[1][k] = j
      if res1[1][k] == j:
        res1[1][k] = 0
    print res1
    res = res1 if(res[0] > res1[0]) else res
    pass

  print 'result'
  print res
  #
  # print input
  # input = ((0,6,2), (2,0,0.5), (1,1,0))
  #
  # print tsp_dyn_solver(input)