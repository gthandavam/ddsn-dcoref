__author__ = 'gt'

from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode
import nltk
from nltk.corpus import wordnet as wn
from string import punctuation as punct
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
    self.light_verbs = ('do', 'let', 'give', 'make', 'decide', 'set')
    #Also ignore verbs that have arg0
    pass


  def build_graph(self, srl_text):
    sentences = self.get_sentences(srl_text)
    srl_args_per_sentence = []

    #convert senna output columns to rows for each sentence
    for sentence in sentences:
      if(len(sentence) != 0):
        srl_args_per_sentence.append(self.get_column_args(sentence))

    #standoff_lines for the document
    self.get_semrole_groups(srl_args_per_sentence)

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


  def get_semrole_groups(self, srl_args_per_sentence):
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
        skip = False
        for sem_role in srl_args_per_sentence[s_idx][i]:
          #skipping a combination having -A0
          if sem_role.endswith('-A0'):
            skip = True
            break

        if skip:
          continue

        skip = True

        for sem_role in srl_args_per_sentence[s_idx][i]:
          #skipping a combination having no -V
          if sem_role.endswith('-V'):
            skip = False
            break

        if skip:
          continue

        sem_group = self.get_sem_role_group(srl_args_per_sentence[s_idx], i, offset, s_idx, pred_num)
        inc = self.make_nodes(sem_group, s_idx, pred_num)
        #TODO: dont fix argument slots : append nodes and capture arg_type in RNode -> this will be useful to
        if inc:
          pred_num += 1

      # +1 to account for newline char
      offset += int(srl_args_per_sentence[s_idx][1][-1].split()[1]) + 1

    return

  def make_nodes(self, sem_group, sent_num, pred_num):
    nodes = {'pred' : None, 'arg1' : None, 'arg2' : None}
    if sem_group['pred'] is None:
      return False
    nodes['pred'] = self.make_pnode('pred', sem_group['pred'], pred_num, sent_num)

    if not sem_group['arg1'] is None:
      nodes['arg1'] = self.make_rnode('arg1', sem_group['arg1'], pred_num, sent_num)

    if nodes['pred'].light:
      if not sem_group['arg2'] is None:
        sem_group['arg2'] = self.get_derivationally_related(sem_group['arg2'])

        nodes['pred'] = self.make_pnode('pred', sem_group['arg2'], pred_num, sent_num)
    else:
      if not sem_group['arg2'] is None:
        nodes['arg2'] = self.make_rnode('arg2', sem_group['arg2'], pred_num, sent_num)

    if(nodes['arg1'] is None and nodes['arg2'] is None):
      return False

    self.PNodes[sent_num].append(nodes['pred'])
    self.RNodes[sent_num].append([None, nodes['arg1'], nodes['arg2']])

    return True


    pass

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


  def get_sem_role_group(self, srl_args, idx, offset, sent_num, pred_num):
    """
    Assuming a grammar here:
    *-V is a predicate senna srl identifying VPs such as swipe out as verb
    so need to handle BIE/S of V
    *-A0 translates to arg0
    *-A1 translates to arg1
    *-A2 translates to arg2
    Parse the IOBES format

    Baked-Char-Siu-Bao----Buns-With-Minced-BBQ-Pork -> Gives a case when args can be present without a predicate. Eg: 1 egg beaten B-A1, E-A1, O
    => Need to skip arg groups when no predicate is present

    '/home/gt/NewSchematicSummary/recipe-split/hearty-chicken-noodle-soup.txt'
    -> arg group having S-V and BIE-V separately in a column causing confusion

    Assuming predicate always occurs before arg2 -> useful assumption
    for handling light verbs

    """
    tokens = len(srl_args[idx])

    ret = {'pred':None, 'arg1':None, 'arg2': None}


    for i in xrange(0, tokens):
      if(srl_args[idx][i].endswith('-V')):
        if(srl_args[idx][i] == 'S-V'):
          ret['pred'] = srl_args[0][i]
        elif(srl_args[idx][i] == 'E-V'):
          ret['pred'] = text + ' ' + srl_args[0][i]
          text = ""
        elif(srl_args[idx][i] == 'B-V'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-V'):
          text += ' ' + srl_args[0][i]
      # elif(srl_args[idx][i].endswith('-A0')):
      #   if(srl_args[idx][i] == 'S-A0'):
      #     ret['arg0'] = srl_args[0][i]
      #   elif(srl_args[idx][i] == 'E-A0'):
      #     ret['arg0'] = text + ' ' + srl_args[0][i]
      #     text = ""
      #   elif(srl_args[idx][i] == 'B-A0'):
      #     text = srl_args[0][i]
      #   elif(srl_args[idx][i] == 'I-A0'):
      #     text += ' ' + srl_args[0][i]
      elif(srl_args[idx][i].endswith('-A1')):
        if(srl_args[idx][i] == 'S-A1'):
          ret['arg1'] = srl_args[0][i]
        elif(srl_args[idx][i] == 'E-A1'):
          ret['arg1'] = text + ' ' + srl_args[0][i]
          text = ""
        elif(srl_args[idx][i] == 'B-A1'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-A1'):
          text += ' ' + srl_args[0][i]
      elif(srl_args[idx][i].endswith('-A2')):
        if(srl_args[idx][i] == 'S-A2'):
          ret['arg2'] = srl_args[0][i]

        elif(srl_args[idx][i] == 'E-A2'):
          ret['arg2'] = text + ' ' + srl_args[0][i]
          text = ""
        elif(srl_args[idx][i] == 'B-A2'):
          text = srl_args[0][i]
        elif(srl_args[idx][i] == 'I-A2'):
          text += ' ' + srl_args[0][i]

    ret['pred'] = self.cleanse_arg(ret['pred'])
    ret['arg1'] = self.cleanse_arg(ret['arg1'])
    ret['arg2'] = self.cleanse_arg(ret['arg2'])
    if len(self.RNodes[sent_num]) != len(self.PNodes[sent_num]):
      print ' RP not equal here'

    return ret

  def make_pnode(self, arg_type, arg, pred_num, sent_num):
    arg = arg.lower()
    if not wn.morphy(arg) is None:
      arg = wn.morphy(arg)

    light = False
    if arg in self.light_verbs:
      light = True

    return PNode(arg, pred_num, sent_num, light)
    # return PNode(pred_num, sent_num, arg)
    pass

  def make_rnode(self, arg_type, arg, pred_num, sent_num):
    #based on the assumption made in generate_nodes method
    arg = arg.lower()
    # if arg_type == 'arg2' and self.PNodes[sent_num][pred_num].predicate in  self.light_verbs:
    #   #light verbs
    #   arg = self.cleanse_arg(arg)
    #   arg = self.get_derivationally_related(arg)
    #   return PNode(pred_num, sent_num, arg)
    # else:
    #   arg = self.cleanse_arg(arg)
    #   return RNode(arg, arg_type, sent_num, pred_num)
    return RNode(arg, pred_num, sent_num, arg_type)
    pass

  def cleanse_arg(self, arg):
    if arg is None:
      return None

    arg = unicode(arg)
    punct_translate_map = dict( (ord(char), None) for char in punct )
    arg = arg.translate(punct_translate_map)

    ret = []
    for word in arg.split():
      if self.is_stopword(word):
        continue
      else:
        ret.append(word)
    return ' '.join(ret)

  def get_derivationally_related(self, arg):
    for word in arg.split():
      if not wn.morphy(word) is None:
        word = wn.morphy(word)
      syn_word = wn.synsets(word, wn.NOUN)
      if len(syn_word) == 0:
        continue

      syn_word = syn_word[0]
      if len(syn_word.lemmas) == 0:
        continue
      lemma = syn_word.lemmas[0]
      dv = lemma.derivationally_related_forms()

      if(len(dv) == 0):
        continue

      return dv[0].name

    return arg
    pass
