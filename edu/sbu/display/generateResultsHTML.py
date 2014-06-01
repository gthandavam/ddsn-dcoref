__author__ = 'polina'

import os
import random

def generateDisplayFile():
  img_height = 200
  dirName = "/home/gt/Documents/"
  f = open(dirName+"recipes.html","w")
  dirName += "MacAndCheese/"
  f.write("<html><body><table border=1 cellspacing=5>\n")
  f.write("<tr><td>#</td><td>File</td><td>Recipe text</td><td>Sentence index based weight</td><td>Graph edge statistics based weight</td></tr>\n")
  files = os.listdir(dirName+"MacAndCheese-svg-files")
  i=0
  for fl in files:
    i+=1
    f_txt = open(dirName+"MacAndCheese-steps/"+fl.replace(".svg",".txt"))
    txt = f_txt.read()
    f_txt.close()
    # f.write(("<tr><td>{}</td><td><img height={} src=\"./MacAndCheese/MacAndCheese-svg-files_withSentGapWeight/{}\"></td><td><img height={} src=\"./MacAndCheese/MacAndCheese-svg-files_withStatistics/{}\"></td><td><img height={} src=\"./MacAndCheese/MacAndCheese-svg-files_graphStat/{}\"></td></tr>\n").format(txt,img_height,fl,img_height,fl,img_height,fl))
    # f.write(("<tr><td>{}</td><td><a target='_blank' href=\"./MacAndCheese/MacAndCheese-svg-files_withSentGapWeight/{}\">Img&gt;&gt;</a></td><td><a target='_blank' href=\"./MacAndCheese/MacAndCheese-svg-files_withStatistics/{}\">Img&gt;&gt;</a></td><td><a target='_blank' href=\"./MacAndCheese/MacAndCheese-svg-files_graphStat/{}\">Img&gt;&gt;</a></td></tr>\n").format(txt,fl,fl,fl))
    f.write(("<tr><td>{}</td><td>{}</td><td>{}</td><td><a target='_blank' href=\"./MacAndCheese/MacAndCheese-svg-files_withSentGapWeight/{}\">Img&gt;&gt;</a></td><td><a target='_blank' href=\"./MacAndCheese/MacAndCheese-svg-files/{}\">Img&gt;&gt;</a></td></tr>\n").format(i,fl,txt,fl,fl,fl))
    f.write("<tr><td colspan=4><hr></td></tr>\n")
    pass
  f.write("</table></body></html>")
  f.close()


def generateEvalFile():
  img_height = 800
  dirName1 = "/home/gt/Documents/"
  f = open(dirName1+"user_eval.html","w")
  dirName = dirName1+"UserEvaluation/"
  f.write("<!DOCType HTML><html><head><script src=\"eval.js\"></script></head>\n")
  f.write("<body><table border=1 cellspacing=5>\n")
  f.write("<tr><td>#</td><td></td><td></td></tr>\n")
  files = os.listdir(dirName+"AlgoA_svg")
  i=0
  methods = ["AlgoA_svg", "AlgoB_svg"]
  random.shuffle(files)
  for fl in files:
    txt = None
    try:
      f_txt = open(dirName1+"MacAndCheese/MacAndCheese-steps/"+fl.replace(".svg",".txt"))
      txt = f_txt.read()
      f_txt.close()
    except:
      pass
    if txt==None:
      continue
    i+=1
    if i>20:
      break
    r = random.random()
    m1 = 0
    if r>0.5:
      m1 = 1
    f.write(("<tr><td>{}</td><td><img height={} src=\"UserEvaluation/{}/{}\"></td><td><img height={} src=\"UserEvaluation/{}/{}\"></td></tr>\n").format(txt,img_height,methods[m1],fl,img_height,methods[1-m1],fl))
    f.write(("<tr><td><input type=radio id=graph{} name=graph{} value=2>None</td><td><input type=radio name=graph{} id=graph{} value={}>Graph1</td><td><input type=radio id=graph{} name=graph{} value={}>Graph2</td></tr>\n").format(i,i,i,i,m1,i,i,1-m1))
    f.write("<tr><td colspan=4><hr></td></tr>\n")
    pass
  f.write("<tr><td colspan=4><button onClick=\"calc({});\">Submit</button></td></tr>\n".format(i-1))
  f.write("</table></body></html>")
  f.close()


generateEvalFile()
