__author__ = 'gt'



class RNode:

  def __init__(self):
    self.argType = ''
    self.text = ''
    self.sentNum = -1 #sentence number
    self.predNum = -1 #predicate number in the document : because it is needed to generate graph
    self.reference = []#tracks stepwise reference predicate num
    pass

  def __init__(self, text, argType, snum, pnum):
    self.text = text
    self.argType = argType
    self.sentNum = snum
    self.predNum = pnum
    self.reference = []
    pass

  def add_reference(self, stepnum, pnum):
    #not tracking the step num - assuming one assignment in one step
    self.reference.append(pnum)

