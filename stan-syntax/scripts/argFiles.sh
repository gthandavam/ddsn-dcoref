#! /bin/bash

modelDir=/home/gt/Downloads/stanford-corenlp-full-2014-01-04/
classpath=/home/gt/eclipse_workspace/dcoref-Jan4-14/bin/
recipeName=$1

#java -Djava.ext.dirs=$modelDir  -cp $classpath  edu.sbu.recipe.preprocess.PrefixI  $recipeName
#java -Djava.ext.dirs=$modelDir  -cp $classpath  edu.sbu.recipe.trees.PrintParseTrees  $recipeName
java -Djava.ext.dirs=$modelDir  -cp $classpath  edu.sbu.recipe.args.RecipeArgs  $recipeName
