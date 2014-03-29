__author__ = 'gt'

from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode
import nltk
from nltk.corpus import wordnet as wn
#Parses senna output to build PNodes and RNodes

'''
senna was run with the following flags

./senna-linux64 -posvbs  -offsettags -srl < input_file > output_file

-posvbs flag was required to handle for eg: add predicate in imperative sentence

'''

class DCorefGraphBuilder:

  def is_stopword(self, string):
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False

  def __init__(self):
    self.sent_num = -1
    self.pred_num = -1
    self.encoding = 'UTF-8'
    self.PNodes = []
    self.RNodes = []
    self.light_verbs = ('do', 'let', 'give', 'make', 'decide')
    #Also ignore verbs that have arg0
    pass


  def make_nodes(self, srl_text):
    sentences = self.get_sentences(srl_text)
    srl_args_per_sentence = []

    #convert senna output columns to rows for each sentence
    for sentence in sentences:
      if(len(sentence) != 0):
        srl_args_per_sentence.append(self.get_column_args(sentence))

    #standoff_lines for the document
    self.get_standoff_groups(srl_args_per_sentence)

    return

  def get_sentences(self, lines):
    '''
    API to segregate the senna output into chunks per sentence
    '''
    ret = []
    ret.append([])
    i=0
    for line in lines:
      if(len(line.strip()) == 0):
        i += 1
        ret.append([])
        continue
      ret[i].extend([line])

    return ret


  def get_standoff_groups(self, srl_args_per_sentence):
    '''
     srl_args_per_sentence - columns in senna output
     are converted into rows for further processing
     Col1  - Words
     Col2  - Word spans
     Col3  - chosen verb
     .     - argument structure per verb starts from this column
     .
     Coln
    '''
    offset = 0
    for s_idx in xrange(len(srl_args_per_sentence)):
      no_of_tokens = len(srl_args_per_sentence[s_idx][0])
      #per sentence processing:
      pred_num = 0
      self.PNodes.append([])
      self.RNodes.append([])
      for i in xrange(3, len(srl_args_per_sentence[s_idx])):
        self.generate_nodes(srl_args_per_sentence[s_idx], i, offset, s_idx, pred_num)
        pred_num += 1
      # +1 to account for newline char
      offset += int(srl_args_per_sentence[s_idx][1][-1].split()[1]) + 1

    return



  def get_column_args(self, arg_lines):
    '''
    API to transform the senna output column into a row

    arg_lines : chunk of lines for one sentence
    '''
    ret = []
    col_count = len(arg_lines[0].strip().split('\t'))
    for col in xrange(0, col_count):
      ret.append([])
      for arg_line in arg_lines:
        ret[-1].extend([arg_line.split('\t')[col].strip()])

    return ret


  def generate_nodes(self, srl_args, idx, offset, sent_num, pred_num):
    """
    Assuming a grammar here:
    S-V is a predicate
    *-A0 translates to arg0
    *-A1 translates to arg1
    *-A2 translates to arg2
    Parse the IOBES format

    Assuming predicate always occurs before arg2 -> useful assumption
    for handling light verbs
    """
    tokens = len(srl_args[idx])
    self.RNodes[sent_num].append([None,None,None])
    for i in xrange(0, tokens):
      if(srl_args[idx][i].endswith('S-V')):
        self.PNodes[sent_num].append(self.make_pnode('pred', srl_args[0][i], pred_num, sent_num))

      elif(srl_args[idx][i].endswith('-A0')):
        if(srl_args[idx][i] == 'S-A0'):
          self.RNodes[sent_num][pred_num][0] = self.make_rnode('arg0', srl_args[0][i], pred_num, sent_num)
        elif(srl_args[idx][i] == 'E-A0'):
          self.RNodes[sent_num][pred_num][0] = self.make_rnode('arg0', text + ' ' + srl_args[0][i], pred_num, sent_num)
          text = ""
        elif(srl_args[idx][i] == 'B-A0'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-A0'):
          text += ' ' + srl_args[0][i]
      elif(srl_args[idx][i].endswith('-A1')):
        if(srl_args[idx][i] == 'S-A1'):
          self.RNodes[sent_num][pred_num][1] = self.make_rnode('arg1', srl_args[0][i], pred_num, sent_num)
        elif(srl_args[idx][i] == 'E-A1'):
          self.RNodes[sent_num][pred_num][1] = self.make_rnode('arg1', text + ' ' + srl_args[0][i], pred_num, sent_num)
          text = ""
        elif(srl_args[idx][i] == 'B-A1'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-A1'):
          text += ' ' + srl_args[0][i]
      elif(srl_args[idx][i].endswith('-A2')):
        if(srl_args[idx][i] == 'S-A2'):
          self.RNodes[sent_num][pred_num][2] = self.make_rnode('arg2', srl_args[0][i], pred_num, sent_num)
        elif(srl_args[idx][i] == 'E-A2'):
          self.RNodes[sent_num][pred_num][2] = self.make_rnode('arg2', text + ' ' + srl_args[0][i], pred_num, sent_num)
          text = ""
        elif(srl_args[idx][i] == 'B-A2'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-A2'):
          text += ' ' + srl_args[0][i]

  def make_pnode(self, arg_type, arg, pred_num, sent_num):
    if not wn.morphy(arg) is None:
      arg = wn.morphy(arg)

    if arg in self.light_verbs:
      return None
    else:
      return PNode(pred_num, sent_num, arg)
    pass

  def make_rnode(self, arg_type, arg, pred_num, sent_num):
    #based on the assumption made in generate_nodes method
    if arg_type == 'arg2' and self.PNodes[sent_num][pred_num] is None:
      #light verbs
      arg = self.cleanse_arg(arg)
      arg = self.get_derivationally_related(arg)
      return PNode(pred_num, sent_num, arg)
    else:
      arg = self.cleanse_arg(arg)
      return RNode(arg, arg_type, sent_num, pred_num)
    pass

  def cleanse_arg(self, arg):
    ret = []
    for word in arg.split():
      if self.is_stopword(word):
        pass
      else:
        ret.append(word)
    return ' '.join(ret)

  def get_derivationally_related(self, arg):
    for word in arg.split():
      syn_word = wn.synsets(word, wn.NOUN)
      if len(syn_word) == 0:
        continue

      syn_word = syn_word[0]
      dv = syn_word.derivationally_related_forms()

      if(len(dv) == 0):
        continue

      return dv[0].name

    return arg
    pass
