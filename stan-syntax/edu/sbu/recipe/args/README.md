####Reference
[Tregex Javadoc](http://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/trees/tregex/TregexPattern.html)
[SRL themes (arg1, arg2 etc..,) reference](http://naacl2013.naacl.org/Documents/semantic-role-labeling-part-1-naacl-2013-tutorial.pdf)
####Tregex Used for Semantic Parsing

VP !>>SBAR [ <, VBP | <, VB ] [ [ < NP=arg1 $-- PP=argSpecial2 ] | [ < NP=arg1 < PP=arg2 ] | [ < NP=arg1 ] | [ < PP=arg2  ] | [<, VBP=verb1 ] | [ <, VB=verb1] ]

  * VP !>> SBAR -> Verb phrases that are not part of subordinate clauses
  * VBP and VB -> Imperative verbs, if correctly identified, should come under these POS tags
  * NP as arg1
  * PP as arg2
  * Rest of the expression is about handling cases when arg1 and/or arg2 is absent or when both are absent.
  * $-- PP is an expression added to handle cases like In a small pot, add oil, onions. (PP, V, NP)
