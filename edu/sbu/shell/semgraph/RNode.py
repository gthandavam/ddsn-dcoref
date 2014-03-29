__author__ = 'gt'



class RNode:

  def __init__(self):
    self.arg_type = ''
    self.text = ''
    self.sent_num = -1 #sentence number
    self.pred_num = -1 #predicate number in the document : because it is needed to generate graph
    self.ShellCoref = []#tracks stepwise reference predicate num
    self.to_delete = False
    pass

  def __init__(self, text, arg_type, snum, pnum):
    self.text = text
    self.arg_type = arg_type
    self.sent_num = snum
    self.pred_num = pnum
    self.shell_coref = []
    self.to_delete = False
    pass

  def add_shell_coref(self, stepnum, pnum):
    #not tracking the step num - assuming one assignment in one step
    self.shell_coref.append(pnum)

