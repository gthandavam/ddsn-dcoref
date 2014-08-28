/*
 * Author: GT
 */
package edu.sbu.recipe.trees;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.List;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

public class PrintParseTrees {
  
    

  public static void main(String[] args) throws IOException {
    // TODO Auto-generated method stub
    
    final String recipeName = args[0];
    
    Process p = Runtime.getRuntime().exec(" find /home/gt/Documents/" + recipeName + "/" + recipeName + "-Isteps/ -type f");
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    
    String outDirName = "/home/gt/Documents/" + recipeName + "/" + recipeName + "-Itrees/";
    
    try {
      File outDir = new File(outDirName);
      outDir.mkdirs();
    } catch (Exception e) {
      System.out.println("Exception while creating output Directory " + e.fillInStackTrace());
    }
    
//    Pattern pattern = Pattern.compile("\\[\\d*\\.\\d*\\]");
    
    String fileName;
    while( (fileName=reader.readLine()) != null ) {
      System.out.println("processing" + fileName);
      Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(fileName));
      pipeline.annotate(annotation);
      List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
      
      String treeFileName = fileName.replace(recipeName + "-Isteps", recipeName + "-Itrees");
      
      FileWriter outF = new FileWriter(treeFileName);
      PrintWriter pw = new PrintWriter(outF);
      
      for(CoreMap sentence : sentences) {
        Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
//        outF.write(tree.pennString());
//        tree.pennPrint(pw, false);
        String pTree = tree.pennString();
        
//        Matcher m = pattern.matcher(pTree);
//        StringBuffer sb = new StringBuffer();
//        
//        while(m.find()) {
//          m.appendReplacement(sb, "");
//        }
//        
//        m.appendTail(sb);
        
        pTree = pTree.replaceAll("\\[\\d*\\.\\d*\\]", "");
        System.out.println(pTree);
        pw.write(pTree);
//        tree.penn
        pw.write("\n");
//        outF.write("\n");
      }
      outF.close();
    }

  }

}
