__author__ = 'gt'

from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode
import nltk
from nltk.corpus import wordnet as wn
import logging
#Parses senna output to build PNodes and RNodes

'''
senna was run with the following flags

./senna-linux64 -posvbs  -offsettags -srl < input_file > output_file

-posvbs flag was required to handle for eg: add predicate in imperative sentence

'''

class DCorefGraphBuilder:

  def __init__(self):
    self.sent_num = -1
    self.pred_num = -1
    self.encoding = 'UTF-8'
    self.PNodes = []
    self.RNodes = []
    self.light_verbs = ('do', 'let', 'give', 'make', 'decide', 'set', 'be')

    #From TAABLE
    self.cook_verbs = ('add', 'bake', 'beat', 'blend', 'boil', 'bone', 'braise', 'break', 'broil', 'brown', 'brush', 'chill', 'chop', 'coat', 'combine', 'cook', 'cover', 'curdle', 'cut', 'decorate', 'deep-fry', 'defrost', 'dice', 'dilute', 'dissolve', 'drain', 'dry', 'eat', 'empty', 'farm', 'feed', 'fill', 'flip', 'fold', 'freeze', 'fry', 'glaze', 'grate', 'grease', 'grill', 'grind', 'grow', 'halve', 'heat', 'knead', 'liquidize', 'mash', 'measure', 'melt', 'mince', 'mix', 'parboil', 'peel', 'pinch', 'pour', 'prepare', 'press', 'put', 'refrigerate', 'remove', 'rinse', 'roast', 'roll', 'saute', 'scald', 'scoop', 'seal', 'season', 'serve', 'shake', 'sharpen', 'sieve', 'sift', 'simmer', 'skin', 'slice', 'smoke', 'soak', 'spill', 'spread', 'sprinkle', 'squeeze', 'steam', 'stew', 'stir', 'stir-fry', 'strain', 'stuff', 'thicken', 'toast', 'toss', 'trim', 'turn', 'waste', 'whip', 'whisk')
    #Also ignore verbs that have arg0
    self.logger = logging.getLogger('root')

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
        #TODO: dont fix argument slots : append nodes and capture arg_type in RNode
        if inc:
          pred_num += 1

      # +1 to account for newline char
      offset += int(srl_args_per_sentence[s_idx][1][-1].split()[1]) + 1

    return

  def make_nodes(self, sem_group, sent_num, pred_num):
    """
    Decides whether to make nodes for this predicate and its arguments(sem_group)
    """
    nodes = {'pred' : None, 'arg1' : None, 'arg2' : None}
    if sem_group['pred'] is None:
      return False
    nodes['pred'] = self.make_pnode('pred', sem_group, pred_num, sent_num)

    if nodes['pred'] is None:
      return False

    if not sem_group['arg1'] is None:
      nodes['arg1'] = self.make_rnode('arg1', sem_group['arg1'], pred_num, sent_num, sem_group['arg1POS'])

    #Assumption - LVC have pred, arg1, arg2 compulsarily - effectively we are replacing light verb with
    #verb in arg2, if exists; if no meaningful verb in arg2, ignore the semgroup
    if nodes['pred'].light:
      #always not a light verb in tregex formulation
      if not sem_group['arg2'] is None:
        sem_group['arg2'] = self.get_verbal_form(sem_group['arg2'])

        nodes['pred'] = self.make_pnode('pred', sem_group['arg2'], pred_num, sent_num)
        if nodes['pred'] is None:
          return False
      else:
        return False #not considering a light verb without arg2 having a valid verb form

    else:
      if not sem_group['arg2'] is None:
        nodes['arg2'] = self.make_rnode('arg2', sem_group['arg2'], pred_num, sent_num, sem_group['arg2POS'])

    #TODO: Not handling light verbs for now in this syntactic feature formulation

    #TODO: Allowing null instantiations for now - will come back here later
    # if(nodes['arg1'] is None and nodes['arg2'] is None):
    #   return False

    #if only one of the args is None then treat it as null instantiation - see the TODO above
    if nodes['arg1'] is None:
      # print nodes['pred'].predicate + ' # ' + nodes['arg2'].raw_text + ' # ' + nodes['arg2'].text
      nodes['arg1'] = self.make_rnode('arg1', None, pred_num, sent_num,'', True)

    if nodes['arg2'] is None:
      # print nodes['pred'].predicate + ' # ' + nodes['arg1'].raw_text + ' # ' + nodes['arg1'].text
      nodes['arg2'] = self.make_rnode('arg2', None, pred_num, sent_num,'', True)

    self.PNodes[sent_num].append(nodes['pred'])
    self.RNodes[sent_num].append([None, nodes['arg1'], nodes['arg2']])

    # self.capture_ingredients(nodes['pred'], nodes['arg1'], nodes['arg2'])
    # print 'Yes'
    return True


    pass

  def capture_ingredients(self, pNode, arg1Node, arg2Node):
    """
    Method to capture the discourse entities(ingredients in cooking) for
    a predicate
    """
    #hardcoding ingredients file for now
    ing_file = '/home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-uniqueIng'
    f = open(ing_file)
    ings = [line.strip().rstrip('\n') for line in f.readlines()]
    f.close()


    arg1Words = [] if arg1Node.text is None else arg1Node.text.split()
    arg2Words = [] if arg2Node.text is None else arg2Node.text.split()

    #TODO: Use zip and optimize
    arg1Node.argIngs = set([ing for ing in ings if ing in arg1Words])
    arg2Node.argIngs = set([ing for ing in ings if ing in arg2Words])

    pNode.pIngs = set.union(arg1Node.argIngs, arg2Node.argIngs)

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

    #pred are not cleansed (to capture verb phrases)
    #arg1 and arg2 cleansed in RNode constructor
    # ret['pred'] = self.cleanse_arg(ret['pred'])
    # ret['arg1'] = self.cleanse_arg(ret['arg1'])
    # ret['arg2'] = self.cleanse_arg(ret['arg2'])
    if len(self.RNodes[sent_num]) != len(self.PNodes[sent_num]):
      self.logger.warn(' RP not equal here')

    return ret

  def make_pnode(self, arg_type, sem_group, pred_num, sent_num):
    from nltk.stem.wordnet import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    arg = sem_group['pred'].lower()


    #lemmaitzer is good - when it cannot find lemma,
    #it gracefully returns the arg passed
    arg = lemmatizer.lemmatize(arg, 'v')


    if arg in self.light_verbs:
      return None

    coref_text = ' '
    coref_text_pos = ' '
    if(not sem_group['arg1'] is None):
      coref_text += sem_group['arg1']
      coref_text_pos += sem_group['arg1POS']

    if(not sem_group['arg2'] is None):
      coref_text += ' ' + sem_group['arg2']
      coref_text_pos += ' ' + sem_group['arg2POS']

    #not doing morphy for verbal phrases
    # if not wn.morphy(arg, wn.VERB) is None:
    #   arg = wn.morphy(arg, wn.VERB)

    light = False
    # if arg in self.light_verbs:
    #   light = True
    #
    # #ignoring single word non-cook non-light verbs
    # if not light and arg not in self.cook_verbs and len(arg.split()) == 1:
    #   return None


    return PNode(arg, pred_num, sent_num, light, coref_text, coref_text_pos)
    # return PNode(pred_num, sent_num, arg)
    pass

  def make_rnode(self, arg_type, arg, pred_num, sent_num,argPOS, is_null = False):
    # if arg_type == 'arg2' and self.PNodes[sent_num][pred_num].predicate in  self.light_verbs:
    #   #light verbs
    #   arg = self.cleanse_arg(arg)
    #   arg = self.get_derivationally_related(arg)
    #   return PNode(pred_num, sent_num, arg)
    # else:
    #   arg = self.cleanse_arg(arg)
    #   return RNode(arg, arg_type, sent_num, pred_num)
    return RNode(arg, pred_num, sent_num, arg_type, argPOS, is_null)
    pass


  def get_verbal_form(self, noun_phrase):

    for word in noun_phrase.split():
      verb, converted = self.verbify(word)
      if converted:
        return verb

    return noun_phrase

    pass

  def verbify(self, noun_word):
    """ Transform a noun to the closest verb: mixture -> mix; boiling -> boil """
    noun_synsets = wn.synsets(noun_word, pos="n")

    # Word not found
    if not noun_synsets:
      return noun_word, False

    # Get all noun lemmas of the word
    noun_lemmas = [l for s in noun_synsets \
                   for l in s.lemmas if s.name.split('.')[1] == 'n']

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    noun_lemmas]

    # filter only the verbs
    related_verb_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset.name.split('.')[1] == 'v']

    # Extract the words from the lemmas
    words = [l.name for l in related_verb_lemmas]
    len_words = len(words)

    if len_words == 0:
      return noun_word, False

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])

    # return the verb with max probability
    return result[0][0], True