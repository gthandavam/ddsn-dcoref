package edu.sbu.recipe.preprocess;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Properties;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class PrefixI {

  public static void main(String[] args) throws IOException {
    // TODO Auto-generated method stub
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/MacAndCheese-steps/ -type f");
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    
    String fileName;
    while( (fileName=reader.readLine()) != null ) {
      System.out.println("processing" + fileName);
      Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(fileName));
      
      pipeline.annotate(annotation);
      
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
      
      String treeFileName = fileName.replace("MacAndCheese-steps", "MacAndCheese-Isteps");
      
      FileWriter outF = new FileWriter(treeFileName);
      
      for(CoreMap sentence : sentences) {
        String sent = sentence.toString();
        
        sent = sent.replaceAll(";", "; I ");
        
        outF.write("I " + sent);
        outF.write("\n");
      }
      outF.close();
    }



  }

}
