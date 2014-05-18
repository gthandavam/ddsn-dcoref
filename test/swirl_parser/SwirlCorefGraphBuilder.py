__author__ = 'gt'

from edu.sbu.shell.semgraph.PNode import PNode
from edu.sbu.shell.semgraph.RNode import RNode
import nltk
from nltk.corpus import wordnet as wn
import logging
#Parses swirl output to build PNodes and RNodes

'''
swirl was run with the following flags

[available in the path]
swirl_parse_classify  model_swirl/ model_charniak/ input_file > output_file

'''

class SwirlCorefGraphBuilder:

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


  def build_graph(self, srl_matrix):

    for sent_num in xrange(len(srl_matrix)):
      self.get_semrole_groups(srl_matrix[sent_num], sent_num)

    '''
    Change of behavior in swirl from senna in the way we deal with the output;
    If we dont identify any predicates in a sentence, we totally ignore such sentences
    in swirl; we were not ignoring in senna(it contributes to sent-count and affects
    arbor weights order_close_together)
    '''

    return

  def get_semrole_groups(self, srl_per_sent, sent_num):
    '''

    '''
    #per sentence processing
    pred_num = 0
    self.PNodes.append([])
    self.RNodes.append([])

    #any sentence without a predicate identified will be skipped
    for col in xrange(2, len(srl_per_sent[0]), 2):
      skip = False
      for row in xrange(len(srl_per_sent)):
        #skip a predicate with arg0
        if srl_per_sent[row][col].endswith('-A0'):
          skip = True

      if not skip:
        sem_group = self.get_sem_role_group(srl_per_sent, col, sent_num, pred_num)


        inc = self.make_nodes(sem_group, sent_num, pred_num)
        #TODO: dont fix argument slots : append nodes and capture arg_type in RNode
        if inc:
          # self.logger.error('nodes created')
          self.logger.error(sem_group)
          pred_num += 1

    return

  def make_nodes(self, sem_group, sent_num, pred_num):
    """
    Decides whether to make nodes for this predicate and its arguments(sem_group)
    """
    nodes = {'pred' : None, 'arg1' : None, 'arg2' : None}
    if sem_group['pred'] is None:
      return False
    nodes['pred'] = self.make_pnode('pred', sem_group['pred'], pred_num, sent_num)

    if nodes['pred'] is None:
      return False

    if not sem_group['arg1'] is None:
      nodes['arg1'] = self.make_rnode('arg1', sem_group['arg1'], pred_num, sent_num, False, sem_group['arg1Prob'])

    #Assumption - LVC have pred, arg1, arg2 compulsarily - effectively we are replacing light verb with
    #verb in arg2, if exists; if no meaningful verb in arg2, ignore the semgroup
    if nodes['pred'].light:
      if not sem_group['arg2'] is None:
        sem_group['arg2'] = self.get_verbal_form(sem_group['arg2'])

        nodes['pred'] = self.make_pnode('pred', sem_group['arg2'], pred_num, sent_num)
        if nodes['pred'] is None:
          return False
      else:
        return False #not considering a light verb without arg2 having a valid verb form

    else:
      if not sem_group['arg2'] is None:
        nodes['arg2'] = self.make_rnode('arg2', sem_group['arg2'], pred_num, sent_num, False, sem_group['arg2Prob'])

    #TODO: Allowing null instantiations for now - will come back here later
    if(nodes['arg1'] is None and nodes['arg2'] is None):
      return False

    #if only one of the args is None then treat it as null instantiation - see the TODO above
    if nodes['arg1'] is None:
      # print nodes['pred'].predicate + ' # ' + nodes['arg2'].raw_text + ' # ' + nodes['arg2'].text
      nodes['arg1'] = self.make_rnode('arg1', None, pred_num, sent_num, True)

    if nodes['arg2'] is None:
      # print nodes['pred'].predicate + ' # ' + nodes['arg1'].raw_text + ' # ' + nodes['arg1'].text
      nodes['arg2'] = self.make_rnode('arg2', None, pred_num, sent_num, True)

    self.PNodes[sent_num].append(nodes['pred'])
    self.RNodes[sent_num].append([None, nodes['arg1'], nodes['arg2']])

    self.capture_ingredients(nodes['pred'], nodes['arg1'], nodes['arg2'])
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

  def get_sem_role_group(self, srl_args, col, sent_num, pred_num):
    """
    Assuming a grammar here:
    *-V is a predicate senna srl identifying VPs such as swipe out as verb
    so need to handle BIE/S of V
    *-A0 translates to arg0
    *-A1 translates to arg1
    *-A2 translates to arg2
    Parse the IOB format

    Assuming predicate always occurs before arg2 -> useful assumption
    for handling light verbs

    Special case:
    reduce identified as verb; but also forms A1 for another verb
    /home/gt/PycharmProjects/AllRecipes/gt/crawl/edu/sbu/html2text/MacAndCheese-swirl-files/avocado-mac-and-cheese.txt

    """
    # print srl_args
    ret = {'pred':None, 'arg1':None, 'arg2': None, 'arg1Prob': -1.0, 'arg2Prob' : -1.0}

    for i in xrange(len(srl_args)):
      if(srl_args[i][0].startswith('V#') and ret['pred'] is None):
        ret['pred'] = srl_args[i][0][2:]
      elif(srl_args[i][col].startswith('*')):
        #do nothing - token to be avoided
        pass
      elif(srl_args[i][col].endswith('-A1')):
        if(srl_args[i][col] == 'B-A1'):
          ret['arg1'] = srl_args[i][0]
          ret['arg1Prob'] = srl_args[i][col+1]
        elif(srl_args[i][col] == 'I-A1'):
          ret['arg1'] += ' ' + srl_args[i][0]
      elif(srl_args[i][col].endswith('-A2')):
        if(srl_args[i][col] == 'B-A2'):
          ret['arg2'] = srl_args[i][0]
          ret['arg2Prob'] = srl_args[i][col+1]
        elif(srl_args[i][col] == 'I-A2'):
          ret['arg2'] += ' ' + srl_args[i][0]

    #pred are not cleansed (to capture verb phrases)
    #arg1 and arg2 cleansed in RNode constructor
    # ret['pred'] = self.cleanse_arg(ret['pred'])
    # ret['arg1'] = self.cleanse_arg(ret['arg1'])
    # ret['arg2'] = self.cleanse_arg(ret['arg2'])

    return ret

  def make_pnode(self, arg_type, arg, pred_num, sent_num):
    arg = arg.lower()

    #not doing morphy for verbal phrases
    if not wn.morphy(arg, wn.VERB) is None:
      arg = wn.morphy(arg, wn.VERB)

    light = False
    if arg in self.light_verbs:
      light = True

    #ignoring single word non-cook non-light verbs
    if not light and arg not in self.cook_verbs and len(arg.split()) == 1:
      return None

    return PNode(arg, pred_num, sent_num, light)
    # return PNode(pred_num, sent_num, arg)
    pass

  def make_rnode(self, arg_type, arg, pred_num, sent_num, is_null = False, arg_prob=-1.0):
    # if arg_type == 'arg2' and self.PNodes[sent_num][pred_num].predicate in  self.light_verbs:
    #   #light verbs
    #   arg = self.cleanse_arg(arg)
    #   arg = self.get_derivationally_related(arg)
    #   return PNode(pred_num, sent_num, arg)
    # else:
    #   arg = self.cleanse_arg(arg)
    #   return RNode(arg, arg_type, sent_num, pred_num)
    return RNode(arg, pred_num, sent_num, arg_type, is_null, arg_prob)
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


def get_text(recipe_file):
  """
  Run the swirl labeler and get the srl output file
  """
  swirl_output = '/home/gt/Downloads/swirl-1.1.0/tuna-mac-output'

  ret = []
  #ret has 3 dimensions - sent, row, column
  with open(swirl_output) as f:
    sent_matrix = []
    for line in f.readlines():
      line = line.strip()
      line_matrix = line.split('\t')
      if len(line_matrix) == 1:
        if(len(sent_matrix) != 0):#for handling the case of consecutive empty lines in output
          ret.append(sent_matrix)
        sent_matrix = []
        continue #read next line
        pass

      sent_matrix.append(line_matrix)
      pass

  return ret
  pass

if __name__ == '__main__':
  srl_file = '/home/gt/Downloads/swirl-1.1.0/tuna-mac-output'
  recipe_srl = get_text(srl_file)
  for sent_num in xrange(len(recipe_srl)):
    for row in xrange(len(recipe_srl[sent_num])):
      for column in xrange(len(recipe_srl[sent_num][row])):
        print '\t' + recipe_srl[sent_num][row][column]


