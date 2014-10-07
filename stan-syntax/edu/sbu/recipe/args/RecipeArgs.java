package edu.sbu.recipe.args;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Properties;
import java.util.regex.Pattern;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.tokensregex.MultiWordStringMatcher;
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
import edu.stanford.nlp.util.IntPair;


public class RecipeArgs {
  
  

  public static void main(String[] args) throws IOException {
    
    final String recipeName = args[0];
    
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/" + recipeName + "/" + recipeName + "-Isteps/ -type f");
    
    String outDirName = "/home/gt/Documents/" + recipeName + "/" + recipeName + "NArgs/";
    
    try {
      File outDir = new File(outDirName);
      outDir.mkdirs();
    } catch (Exception e) {
      System.out.println("Exception while creating output Directory " + e.fillInStackTrace());
    }
    
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String fileName;
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    while( (fileName = reader.readLine()) != null) {
      System.out.println("Processing Recipe " + fileName);
      
      String recipe = IOUtils.slurpFileNoExceptions(fileName);
      Annotation annotation = new Annotation(recipe);
      
      Pattern pattern = Pattern.compile("I would");
      
      List<IntPair> offsets = MultiWordStringMatcher.findOffsets(pattern, recipe);
      
      int offSetIdx = 0;
      
      
      String argsFile = fileName.replace(recipeName + "-Isteps", recipeName + "Args");
      
      FileWriter fw = new FileWriter(argsFile);
      
      pipeline.annotate(annotation);
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
      
      //TODO: 3. Handle "In a small bowl, VP NP cases"
      //case 1
//      TregexPattern VPpattern = TregexPattern.compile("VP !>>SBAR  !>>PP "
//          + "[<<# /VBP/=verb | <<# VB=verb] [ [ < NP=arg1 < PP=arg2] | "
//          + "[ < NP=arg1 !<<PRN ] | [ < (PP=arg2  !<: IN) ] | [ <, /VBP/=verb1 ] | [ <, VB=verb1 ] ]");
      
      
      TregexPattern VPpattern = TregexPattern.compile("VP !>>SBAR [<, VBP=verb | <, VB=verb] " +
      " [ [< NP=arg1 $-- PP=argSpecial2] | [ < NP=arg1 < PP=arg2] | " +
      " [ < NP=arg1 ] | [ < PP=arg2  ] | [<, VBP=verb1 ] | [ <, VB=verb1] ]");
      
      
//      
//      TregexPattern VPpattern = TregexPattern.compile("VP !>>SBAR  "
//          + "[<, /VBP/=verb | <, VB=verb] [ [ < NP=arg1 < PP=arg2] | "
//          + "[ < NP=arg1 ] | [ < PP=arg2  ] | [ <, /VBP/=verb1 ] | [ <, VB=verb1 ] ]");
//            
      TreebankLanguagePack tlp = new PennTreebankLanguagePack();
      GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
      
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
          //checking not equality but if arg1 and matcher.getNode(arg1) are pointing to the same reference hence using '=='
            arg1 = null;
//            System.out.println("clearing previous arg1");
          }
          else 
            arg1 = matcher.getNode("arg1");
          
          if(matcher.getNode("argSpecial2") != null && arg2 != matcher.getNode("argSpecial2")) {
            System.out.println("argspecial " + matcher.getNode("argSpecial2"));
            arg2 = matcher.getNode("argSpecial2");
          } else if( arg2 != null && arg2 == matcher.getNode("arg2")) {
            //checking not equality but if arg2 and matcher.getNode(arg2) are pointing to the same reference hence using '==' 
            arg2 = null;
//            System.out.println("clearing previous arg2");
          } 
          else
            arg2 = matcher.getNode("arg2");
          
          if(matcher.getNode("verb1") != null) {
            System.out.println("VERB1");
            System.out.println(matcher.getNode("verb1"));
          }
          
          if(matcher.getNode("verb1") != null && 
              !matcher.getNode("verb1").equals(matcher.getNode("verb")))
            System.out.println("verb1 != verb " + matcher.getNode("verb1") +  " != " + matcher.getNode("verb"));
          
          System.out.println("sentNum: " + sentNum);
          System.out.println("predNum: " + predNum);
          fw.write("sentNum: " + mySeparator + sentNum + "\n");
          fw.write("predNum: " + mySeparator + predNum + "\n");
          if(match!=null) {
            System.out.println("match: " + Sentence.listToString(match.yield()));
          }
          
                    
          if(verb != null) {
            System.out.println("verb: "  + Sentence.listToString(verb.yield()));
            
            while(offSetIdx < offsets.size()) {
              if(verb.taggedYield().get(0).beginPosition() > offsets.get(offSetIdx).getSource())
                offSetIdx++;
              else
                break;
            }
            
            fw.write("verb: " + mySeparator + Sentence.listToString(verb.yield()) + "\n");
            fw.write("Begin:" + mySeparator + (verb.taggedYield().get(0).beginPosition() - (offSetIdx * 9)) + "\n");
            fw.write("End:" + mySeparator + (verb.taggedYield().get(0).endPosition() - (offSetIdx * 9)) + "\n" );
            System.out.println("Verb Begin :" + (verb.taggedYield().get(0).beginPosition() - (offSetIdx * 9)));
            System.out.println("Verb End :" + (verb.taggedYield().get(0).endPosition() - (offSetIdx * 9)));
          } else {
            
            System.out.println("VERB NULL");
            System.out.println(matcher.getNode("verb1"));
            System.out.println(matcher.getNode("arg1"));
            System.out.println(matcher.getNode("arg2"));
          }
          
          if(arg1 != null) {
            
            System.out.println("Arg1: "  + Sentence.listToString(arg1.yield()));
            fw.write("Arg1: " + mySeparator + Sentence.listToString(arg1.yield()) + "\n");
            
            GrammaticalStructure gs = gsf.newGrammaticalStructure(arg1);
            Collection<TypedDependency> tdl = gs.allTypedDependencies();
            
//            for (TypedDependency dep: tdl) {
//              System.out.println(dep.reln()+"~~~~~"+dep.gov()+"~~~~~"+dep.dep());
//            }
            
            ArrayList<TaggedWord> arr = arg1.taggedYield();
            
            fw.write("Arg1POS:" + mySeparator);
            int begin = -1;
            int end = -1;
            for(TaggedWord w: arr)
            {
              if(begin == -1)
                begin = w.beginPosition();
              
              end = w.endPosition();
              
              System.out.print(" "+w);
              fw.write(" " + w);
            }

            fw.write("\n");
            
            fw.write("Begin:" + mySeparator + (begin - (offSetIdx * 9)) + "\n");
            fw.write("End:" + mySeparator + (end - (offSetIdx * 9)) + "\n" );
           
            System.out.println("Arg1Begin:" + (begin - (offSetIdx * 9)) );
            System.out.println("Arg1End:" + (end - (offSetIdx * 9)));
            
          } else {
//            System.out.println("Arg1: NULL");
            fw.write("Arg1:"  + mySeparator + "NULL" + "\n");
            fw.write("Arg1POS:"  + mySeparator +"NULL" + "\n");
            fw.write("Begin:" + mySeparator + -1 + "\n");
            fw.write("End:" + mySeparator + -1 + "\n" );
          }
          
          if(arg2 != null) {
            System.out.println("Arg2: "  + Sentence.listToString(arg2.yield()));
            fw.write("Arg2: "  + mySeparator + Sentence.listToString(arg2.yield()) + "\n");
            GrammaticalStructure gs = gsf.newGrammaticalStructure(arg2);
            Collection<TypedDependency> tdl = gs.allTypedDependencies();
            
//            for (TypedDependency dep: tdl) {
//              System.out.println(dep.reln()+"~~~~~"+dep.gov()+"~~~~~"+dep.dep());
//            }
          
            fw.write("Arg2POS:" + mySeparator);
            ArrayList<TaggedWord> arr = arg2.taggedYield();
            int begin = -1;
            int end = -1;
            for(TaggedWord w: arr)
            {
              if(begin == -1)
                begin = w.beginPosition();
              
              end = w.endPosition();
              
              fw.write(" " + w);
              System.out.print(" "+w);
            }
            System.out.println();
            
            System.out.println("Arg2Begin:" + (begin - (offSetIdx * 9) ));
            System.out.println("Arg2End:" + (end - (offSetIdx * 9)));
            
            
            fw.write("\n");
            
            fw.write("Begin:" + mySeparator + (begin - (offSetIdx * 9)) + "\n");
            fw.write("End:" + mySeparator + (end - (offSetIdx * 9)) + "\n" );
          } else {
//            System.out.println("Arg2: NULL");
            fw.write("Arg2:"  + mySeparator + "NULL" + "\n");
            fw.write("Arg2POS:"  + mySeparator +"NULL" + "\n");
            fw.write("Begin:" + mySeparator + -1 + "\n");
            fw.write("End:" + mySeparator + -1 + "\n" );
          }
          
        }
      
      }
      fw.close();
//      break; //for debugging
    }
    reader.close();
    
  }

}
