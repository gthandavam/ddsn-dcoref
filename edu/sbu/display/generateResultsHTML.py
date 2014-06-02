__author__ = 'polina'

import os
import random, math
import shutil

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
  recipes_per_page = 10
  pages_per_task = 1
  task_num=1
  dirName1 = "/home/gt/Documents/"
  dirName = "/home/localdirs/NLPLab/Tools/google_appengine/projects/recipe-graphs/UserEvaluation-files/"
  try:
    os.makedirs(dirName+str(task_num))
    os.makedirs(dirName+str(task_num)+"/AlgoA_svg")
    os.makedirs(dirName+str(task_num)+"/AlgoB_svg")
  except:
    pass
  page=1
  files = os.listdir(dirName+"AlgoA_svg")
  # page_cnt=int(math.ceil(float(len(files))/recipes_per_page))
  page_cnt = pages_per_task
  f = open(dirName+"1/1.html","w")
  header = "<html><head><script src=\"./eval.js\"></script></head>\n"
  header += "<style>\n"
  header += "div.floating-menu {background:#fff4c8;border:1px solid #ffcc00;width:250px;z-index:200;}\n"
  header += "div.floating-menu a, div.floating-menu h3 {display:block;margin:0 0.5em;}\n"
  header += ".hidden {\n"
  header += "position: absolute;\n"
  header += "left: -10000px;\n"
  header += "}\n"
  header += "</style>\n"
  header += "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js\"> </script>\n"
  header2 = "<form action=\"/save\" method=\"post\"><table border=0 cellspacing=5>\n"
  header2 += "<tr><td style=\"border-bottom:thin solid;\">#</td><td style=\"border-bottom:thin solid;\">Recipe Text</td><td style=\"border-bottom:thin solid;\">Graph1</td><td style=\"border-bottom:thin solid;\">Graph2</td></tr>\n"
  f.write(header)
  f.write("<body> <h2>Page {} out of {}</h2>\n".format(page,page_cnt))
  f.write(header2)
  i=0
  k=0
  methods = ["AlgoA_svg", "AlgoB_svg"]
  random.shuffle(files)
  html_footer = "</form></table>"
  # html_footer +="<div><***VAR_APP_CODE***></div>"
  html_footer += "<div><input type=\"hidden\" name=\"save_answ\" value=\"1\"></div>\n"
  html_footer += "<div><input type=\"submit\" value=\"Submit\"></div>\n"
  html_footer += "<div><input type=\"hidden\" name=\"page_num\" value=\"{}\"></div>\n"
  # html_footer += "</body></html>"
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
    k+=1
    if k>recipes_per_page:
      # f.write(footer.replace("---page_num---",page))
      f.write("<div><input type=\"hidden\" name=\"task_num\" value=\"{}\"></div>\n".format(task_num))
      f.write(html_footer.format(page))
      page+=1
      k=1
      f.close()
      if page>pages_per_task:
        task_num+=1
        page=1
        try:
          os.makedirs(dirName+str(task_num))
          os.makedirs(dirName+str(task_num)+"/AlgoA_svg")
          os.makedirs(dirName+str(task_num)+"/AlgoB_svg")
        except:
          pass
      f = open(dirName+str(task_num)+"/"+str(page)+".html","w")
      f.write(header)
      f.write("<body> <h2>Page {} out of {}</h2>\n".format(page,page_cnt))
      f.write(header2)
    r = random.random()
    m1 = 0
    if r>0.5:
      m1 = 1
    r_name = fl.replace(".svg","")
    try:
      shutil.copy(dirName+"AlgoA_svg/"+fl, dirName+str(task_num)+"/AlgoA_svg")
      shutil.copy(dirName+"AlgoB_svg/"+fl, dirName+str(task_num)+"/AlgoB_svg")
    except:
      pass
    f.write(("<tr><td style=\"border-left:thin solid; border-right:thin solid;\">{}</td><td style=\"border-left:thin solid; border-right:thin solid;\"><div id='group-1'><div class=\"floating-menu\">{}</div></td><td style=\"border-left:thin solid; border-right:thin solid;\"><img height={} src=\"http://recipe-graphs.appspot.com/graph?folder={}&task_num={}&file_name={}\"></td><td><img height={} src=\"http://recipe-graphs.appspot.com/graph?folder={}&task_num={}&file_name={}\"></td></tr>\n").format(k,txt,img_height,methods[m1],task_num,fl,img_height,methods[1-m1],task_num,fl))
    f.write(("<tr><td colspan=2 style=\"border-left:thin solid; border-right:thin solid;\"><input type=radio id=\"graph{}\" name=\"graph{}\" value=2 checked=true>None&nbsp;&nbsp;&nbsp;&nbsp;<input type=radio id=\"graph{}\" name=\"graph{}\" value=3>Both</td><td style=\"border-left:thin solid; border-right:thin solid;\"><input type=radio name=\"graph{}\" id=\"graph{}\" value={}>Graph1</td><td style=\"border-left:thin solid; border-right:thin solid;\"><input type=radio id=\"graph{}\" name=\"graph{}\" value={}>Graph2</td></tr>\n").format(i,i,i,i,i,i,m1,i,i,1-m1))
    f.write("<tr height=10><td style=\"border-bottom:thin solid;\" colspan=10><hr><input type='hidden' name='recipe_name{}' value='{}'></td></tr>\n".format(i,r_name))
    pass
  # f.write("<tr><td colspan=4><button onClick=\"calc({});\">Submit</button></td></tr>\n".format(i-1))
  # f.write(html_footer.replace("---page_num---",page))
  f.write("<div><input type=\"hidden\" name=\"task_num\" value=\"{}\"></div>\n".format(task_num))
  f.write(html_footer.format(page))
  f.close()


generateEvalFile()
