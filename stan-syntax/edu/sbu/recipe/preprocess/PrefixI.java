package edu.sbu.recipe.preprocess;

import java.io.BufferedReader;
import java.io.File;
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
    

    final String recipeName = args[0];
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/" + recipeName + "/" + recipeName + "-steps/ -type f");
    
    String outDirName = "/home/gt/Documents/" + recipeName + "/" + recipeName + "-Isteps/";
    
    try {
      File outDir = new File(outDirName);
      outDir.mkdirs();
    } catch (Exception e) {
      System.out.println("Exception while creating output Directory " + e.fillInStackTrace());
    }
    
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
      
      String treeFileName = fileName.replace(recipeName + "-steps", recipeName + "-Isteps");
      
      FileWriter outF = new FileWriter(treeFileName);
      
      for(CoreMap sentence : sentences) {
        String sent = sentence.toString();
        
        StringBuilder processedSent = new StringBuilder();
        String parts[] = sent.split(";");
        for(int i=0 ; i < parts.length; i++) {
          parts[i] = Character.toLowerCase(
              parts[i].charAt(0)) + (parts[i].length() > 1 ? parts[i].substring(1) : ""); 
          
        }
        
        for(int i=0 ; i < parts.length; i++) {
          if(parts[i].toLowerCase().startsWith("in ")) {
            parts[i] = Character.toUpperCase(
                parts[i].charAt(0)) + (parts[i].length() > 1 ? parts[i].substring(1) : "");
            processedSent.append(parts[i]);
          }
          else if(i != parts.length - 1)
            processedSent.append(" I would " + parts[i] + ";");
          else
            processedSent.append(" I would " + parts[i]);
          
        }
        
        outF.write(processedSent.toString());
        outF.write("\n");
      }
      outF.close();
    }

  }

}
