package edu.sbu.recipe.args;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.trees.tregex.TregexMatcher;
import edu.stanford.nlp.trees.tregex.TregexPattern;
import edu.stanford.nlp.util.CoreMap;


public class RecipeArgs {

  public static void main(String[] args) throws IOException {
    
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/MacAndCheese-Isteps/ -type f");
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String fileName;
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    while( (fileName = reader.readLine()) != null) {
     
      Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(fileName));
      
      String argsFile = fileName.replace("MacAndCheese-Isteps", "MacAndCheeseArgs");
      
      FileWriter fw = new FileWriter(argsFile);
      
      pipeline.annotate(annotation);
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
      
      //separating individual VPs
      int predNum = 0;
      int sentNum = 0;
      for (CoreMap sentence : sentences) {
        System.out.println("sentence:" + sentence);
        Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
        sentNum++;
        
        
        TregexPattern VPpattern = TregexPattern.compile("VP !>>SBAR  !>>PP <<# /VB.?/=verb [ [ < NP=arg1 < PP=arg2] | [ < NP=arg1 !<<PRN ] | [ < (PP=arg2  !<: IN) ] | [ <: /VBP/ ] ]");
  
        TregexMatcher matcher = VPpattern.matcher(tree);
  
        while (matcher.findNextMatchingNode()) {
          predNum++;
          Tree match = matcher.getMatch();
          Tree verb = matcher.getNode("verb");
          Tree arg1 = matcher.getNode("arg1");
          Tree arg2 = matcher.getNode("arg2");
          
          System.out.println("sentNum: " + sentNum);
          System.out.println("predNum: " + predNum);
          fw.write("sentNum: " + sentNum + "\n");
          fw.write("predNum: " + predNum + "\n");
          if(match!=null)
            System.out.println("match: " + Sentence.listToString(match.yield()));
          
          if(verb != null) {
            System.out.println("verb: "  + Sentence.listToString(verb.yield()));
            fw.write("verb: "  + Sentence.listToString(verb.yield()) + "\n");
          }
          
          if(arg1 != null) {
            System.out.println("Arg1: "  + Sentence.listToString(arg1.yield()));
            fw.write("Arg1: "  + Sentence.listToString(arg1.yield()) + "\n");
          } else {
            System.out.println("Arg1: NULL");
            fw.write("Arg1: NULL" + "\n");
          }
          
          if(arg2 != null) {
            System.out.println("Arg2: "  + Sentence.listToString(arg2.yield()));
            fw.write("Arg2: "  + Sentence.listToString(arg2.yield()) + "\n");
          } else {
            System.out.println("Arg2: NULL");
            fw.write("Arg2: NULL" + "\n");
          }
          
        }
      
      }
      
      fw.close();
    }
    reader.close();
    
  }

}
