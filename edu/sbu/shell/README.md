#####Transformer.py

  * iterative_learning.py has different invocations for Transformer.py
  
  
######How iterative learning is implemented now ?

  * For arbor and arbor_trans, first iteration is based on cc weights. In the following iterations, nodes connected by arborescence algorithm become adjacent and/or part of the transitive closure.
  
  * We collect these statistics iteratively
  
  * For CC and text_order there is no iterative learning, we compute weights and save them. 


######Different ways of collecting statistics

  * arbor -> Learn weights from adjacent nodes in graphs connected by arborescence
  
  * arbor_trans -> Learn weights from nodes in the transitive closure in graphs connected by arborescence
  
  * cc -> Learn weights based on adjacent nodes only within a connected component returned by DCoref heuristics
  
  * text_order -> Weights purely based on textual order (dist ( (sent 1, predicate 1), (sent 5, predicate 2) )
