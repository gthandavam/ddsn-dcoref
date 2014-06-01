__author__ = 'polina'

import os

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