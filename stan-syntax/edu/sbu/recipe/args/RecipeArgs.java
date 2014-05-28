package edu.sbu.recipe.args;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.PennTreebankLanguagePack;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TypedDependency;
import edu.stanford.nlp.trees.tregex.TregexMatcher;
import edu.stanford.nlp.trees.tregex.TregexPattern;
import edu.stanford.nlp.util.CoreMap;


public class RecipeArgs {

  public static void main(String[] args) throws IOException {
    
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/CheeseBurger/CheeseBurger-Isteps/ -type f");
    
    
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String fileName;
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    while( (fileName = reader.readLine()) != null) {
//      fileName = "/home/gt/Documents/MacAndCheese-Isteps/"
//          + "baked-macaroni-and-cheese-with-tomato.txt";
//      fileName = "/home/gt/Documents/MacAndCheese-Isteps/"
//          + "canadian-bacon-macaroni-and-cheese.txt";
//      fileName = "/home/gt/Documents/MacAndCheese-Isteps/"
//          + "best-mac-n-cheese-ever.txt";
      System.out.println("Processing Recipe " + fileName);
      Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(fileName));
      
      String argsFile = fileName.replace("CheeseBurger-Isteps", "CheeseBurgerArgs");
      
      FileWriter fw = new FileWriter(argsFile);
      
      pipeline.annotate(annotation);
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
      
      
      //separating individual VPs
      //TODO: 1. Check "Stir in pasta" - cases
      //Stir in pasta should be classified as stir->verb, pasta as arg1
      //but with the current scheme "in pasta" is identified as PP -> arg2
      //This corpus has this usage of in to talk about arg1
      //Ref: http://www.macmillandictionary.com/us/dictionary/american/stir-in
      // Looks like an american usage! snap!
      /*handle the following
       * whisk in
       * stir in
       * pour in
      */
      
      //TODO: 2. Modify NP ! << PRN -> use tregex to filter and later on post 
      //process PRN and all
      
      //TODO: 3. Handle "In a small bowl, VP NP cases"
      TregexPattern VPpattern = TregexPattern.compile("VP !>>SBAR  !>>PP "
          + "<<# /VBP/=verb [ [ < NP=arg1 < PP=arg2] | [ < NP=arg1 !<<PRN ] |"
          + " [ < (PP=arg2  !<: IN) ] | [ <: /VBP/=verb1 ] ]");

//      TregexPattern syntFeaturesPattern = TregexPattern.compile(
//          "NN=head > NP [$-- /NN/=appos | $-- JJ=adj | $-- DT=det]");
      
      TreebankLanguagePack tlp = new PennTreebankLanguagePack();
      GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
      
      /*
       * Test cases for getting modifiers and headNouns of a NP:
          8 inch baking dish
          large casserole dish
          9X11 inch baking dish
          greased 2-quart baking dish
          large pot of lightly salted water
       */
      
      String mySeparator = "TheGT";
      int sentNum = -1;
      for (CoreMap sentence : sentences) {
        System.out.println("sentence" + mySeparator + sentence);
        Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
        sentNum++;
        
        int predNum = -1;
  
        TregexMatcher matcher = VPpattern.matcher(tree);
        
        Tree verb = null;
        Tree arg1 = null;
        Tree arg2 = null;
  
        while (matcher.findNextMatchingNode()) {
          predNum++;
          Tree match = matcher.getMatch();
         
          verb = matcher.getNode("verb");
          
          if( arg1 != null && arg1 == matcher.getNode("arg1")){
            arg1 = null;
//            System.out.println("clearing previous arg1");
          }
          else 
            arg1 = matcher.getNode("arg1");
          
          if( arg2 != null && arg2 == matcher.getNode("arg2")) {
            arg2 = null;
//            System.out.println("clearing previous arg2");
          } 
          else
            arg2 = matcher.getNode("arg2");
          
          if(matcher.getNode("verb1") != null)
            System.out.println("VERB1");
          
          if(matcher.getNode("verb1") != null && 
              !matcher.getNode("verb1").equals(matcher.getNode("verb")))
            System.out.println("GGGG verb1 != verb");
          
          System.out.println("sentNum: " + sentNum);
          System.out.println("predNum: " + predNum);
          fw.write("sentNum: " + mySeparator + sentNum + "\n");
          fw.write("predNum: " + mySeparator + predNum + "\n");
//          if(match!=null)
//            System.out.println("match: " + Sentence.listToString(match.yield()));
          
          if(verb != null) {
//            System.out.println("verb: "  + Sentence.listToString(verb.yield()));
            fw.write("verb: " + mySeparator + Sentence.listToString(verb.yield()) + "\n");
          }
          
          if(arg1 != null) {
            System.out.println("Arg1: "  + Sentence.listToString(arg1.yield()));
            fw.write("Arg1: " + mySeparator + Sentence.listToString(arg1.yield()) + "\n");
            
            ArrayList<TaggedWord> arr = arg1.taggedYield();
            
            fw.write("Arg1POS:" + mySeparator);
            for(TaggedWord w: arr)
            {
              System.out.print(" "+w);
              fw.write(" " + w);
            }
            
            System.out.println();
            
            fw.write("\n");
          } else {
//            System.out.println("Arg1: NULL");
            fw.write("Arg1:"  + mySeparator + "NULL" + "\n");
            fw.write("Arg1POS:"  + mySeparator +"NULL" + "\n");
            
          }
          
          if(arg2 != null) {
            System.out.println("Arg2: "  + Sentence.listToString(arg2.yield()));
            fw.write("Arg2: "  + mySeparator + Sentence.listToString(arg2.yield()) + "\n");
//            GrammaticalStructure gs = gsf.newGrammaticalStructure(arg2);
//            Collection<TypedDependency> tdl = gs.allTypedDependencies();
//          
            fw.write("Arg2POS:" + mySeparator);
            ArrayList<TaggedWord> arr = arg2.taggedYield();
            
            for(TaggedWord w: arr)
            {
              fw.write(" " + w);
              System.out.print(" "+w);
            }
            System.out.println();
            
            fw.write("\n");
          } else {
//            System.out.println("Arg2: NULL");
            fw.write("Arg2: "  + mySeparator + "NULL" + "\n");
            fw.write("Arg2POS:"  + mySeparator +" NULL" + "\n");
          }
          
        }
      
      }
      
      fw.close();
//      break; //for debugging
    }
    reader.close();
    
  }

}
