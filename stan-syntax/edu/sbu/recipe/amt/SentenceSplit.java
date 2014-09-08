package edu.sbu.recipe.amt;

import java.io.BufferedReader;
import java.io.File;
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


public class SentenceSplit {

  public static void main(String[] args) throws IOException {
    
    final String recipeName = args[0];
    
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/" + recipeName + "/" + recipeName + "-steps/ -type f");
    
    String outDirName = "/home/gt/Documents/" + recipeName + "/" + recipeName + "-ss-steps/";
    
    try {
      File outDir = new File(outDirName);
      outDir.mkdirs();
    } catch (Exception e) {
      System.out.println("Exception while creating output Directory " + e.fillInStackTrace());
    }
    
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String fileName;
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    while( (fileName = reader.readLine()) != null) {
      System.out.println("Processing Recipe " + fileName);
      Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(fileName));
      
      String argsFile = fileName.replace(recipeName + "-steps", recipeName + "-ss-steps");
      
      FileWriter fw = new FileWriter(argsFile);
      
      pipeline.annotate(annotation);
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
            
      
      for (CoreMap sentence : sentences) {
        
        fw.write(sentence.toString());        
        fw.write("\n");
           
      
      }
      
      fw.close();
//      break; //for debugging
    }
    reader.close();
    
  }

}
