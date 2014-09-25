ddsn-dcoref
===========

Discourse deictic shell noun resolution that helps in summarisation

Repo name is a misnomer - the name for the project evolved over time; so please dont read too much into the repo name.

Package Structure

1. edu.sbu.bin -> Meant to keep the utility scripts for the project.

2. edu.sbu.eval -> package focussing on different evaluation techniques for the project.
    a. Sentence re-ordering experiment (extrinsic evaluation)
    b. Cloze task ( may or may not be included in the final version )
    c. User evaluation - Users felt that the task is really hard in our pilot experiments
    d. Possibly we could have some gold standard annotations and report P/R as a metric for the semantic parsing and graphs that we build.

3. edu.sbu.shell -> core of diagram generation
    a. edu.sbu.shell.Transformer -> Driver program for diagram generation
    b. edu.sbu.shell.rules -> Package for coref-resolution heuristics ( coref resolution connects the verb, arg1, arg2 triplets extracted by our Tregex to give us connected components )
    c. edu.sbu.shell.semgraph -> Package for our semantic graph representation and the equivalent representation in graphviz (DCorefGraph -> our semantic graph; DotGraph -> equivalent graph in graphviz parlance)
    d. PNode, RNode -> Representation for Predicate nodes and argument nodes

4. edu.sbu.mst -> Formulating the problem of diagramming as arborescence. We have connected components given by our coref heuristics. We try to string these connected components together (so that they participate in a partial order relation) by making use of arborescence algorithm and content models that we build.
    a. This package has the arborescence solvers, transformation (back and forth) of the semantic graph for arborescence formulation.

5. edu.sbu.stats -> Our content models
  This is what the package is believed to give us 
  '''
  getArg1Arg2PredPredArg1Prob(a1s, a2s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1.arg2, pred1)
  getArg1Arg2PredPredProb(a1s, a2s, verb, overb) returns P(pred2 | pred1.arg1, pred1.arg2, pred1)
  getArg1PredPredArg1Prob(a1s, verb, overb, oas) returns P(pred2, pred2.arg1 | pred1.arg1, pred1)
  getArg1PredPredProb(a1s, verb, overb) returns P(pred2 | pred1.arg1, pred1)
  '''
