__author__ = 'polina'

import csv,math

recipeName = 'MacAndCheese'

class Eval:

  trust_users = {}

  def __init__(self):
    pass

  def readData(self):
    self.answers = {}
    file_name = "/home/gt/Documents/UserEvaluation-files/" + recipeName + "/download_data.csv"
    f = open(file_name)
    f_csv = csv.reader(f)
    cnt=0
    headers = None
    self.recipe_users = {}
    self.users = {}
    for row in f_csv:
      cnt+=1
      if cnt==1:
        headers = {}
        for i in range(len(row)):
          headers[row[i].strip()] = i
        continue
      user_name = row[headers["user_name"]]
      if "polina" in user_name or user_name=="gt" or user_name=="ggt" or user_name=="gt-1":
        continue
      if "None" in row[headers["task"]] or row[headers["task"]].strip()=="":
        continue
      recipe_name = row[headers["recipe_name"]]
      answ = row[headers["method"]]
      if user_name not in self.users:
        self.users[user_name] = {}
      if recipe_name not in self.users[user_name]:
        self.users[user_name][recipe_name] = answ
      if answ not in self.answers:
        self.answers[answ] = {}
      if recipe_name not in self.answers[answ]:
        self.answers[answ][recipe_name] = {}
      if recipe_name not in self.recipe_users:
        self.recipe_users[recipe_name] = {}
      if user_name not in self.answers[answ][recipe_name]:
        self.answers[answ][recipe_name][user_name] = 1
      else:
        print "Error: {} already answered {}".format(user_name,recipe_name)
      if user_name not in self.recipe_users[recipe_name]:
        self.recipe_users[recipe_name][user_name] = answ
      else:
        print "Error: {} already answered {}".format(user_name,recipe_name)

    f.close()

  def getKappa(self,usr1,usr2):
        yy_cnt=0
        nn_cnt=0
        yn_cnt=0
        ny_cnt=0
        for recipe in self.users[usr1]:
            if recipe not in self.users[usr2]:
              continue
            if int(self.users[usr1][recipe])==2:
                continue
            if int(self.users[usr2][recipe])==2:
                continue
            if int(self.users[usr1][recipe]) == 1:
                if int(self.users[usr2][recipe]) == 1 or int(self.users[usr2][recipe])==3:
                    nn_cnt+=1
                else:
                    ny_cnt+=1
            else:
                if int(self.users[usr2][recipe]) == 1 or int(self.users[usr2][recipe])==3:
                    yn_cnt+=1
                else:
                    yy_cnt+=1
        all_cnt = yy_cnt+nn_cnt+yn_cnt+ny_cnt
        if all_cnt==0:
          return None
        a = float(yy_cnt+nn_cnt)/all_cnt
        e = (float(yy_cnt+yn_cnt)/all_cnt)*(float(yy_cnt+ny_cnt)/all_cnt) + (float(ny_cnt+nn_cnt)/all_cnt)*(float(yn_cnt+nn_cnt)/all_cnt)
        if e==1:
            return None
#         print usr1+", "+usr2+": yy_cnt="+str(yy_cnt)+", nn_cnt="+str(nn_cnt)+", yn_cnt="+str(yn_cnt)+", ny_cnt="+str(ny_cnt)+", k="+str(float(a-e)/(1-e))
        return float(a-e)/(1-e)

  def getUserAgreement(self):
    print "Users: {}".format(len(self.users))
    t_kappa = 0
    cnt=0
    users = self.users.keys()
    for i in range(len(self.users)-1):
      usr = users[i]
      # print usr
    # print "Recipes: {}".format(len(recipe_users))
      for j in range(len(users)-i-1):
        usr2 = users[i+j+1]
        kappa = self.getKappa(usr,usr2)
        if kappa != None:
          t_kappa += kappa
          cnt+=1
          if kappa>0.3:
            self.trust_users[usr] = 1
            self.trust_users[usr2] = 1
          # print "{} and {}: kappa={}".format(usr,usr2,kappa)
    if cnt>0:
      print "Average user agreement: {}".format(float(t_kappa)/cnt)
    else:
      print "Average user agreement: None"

  def printStat(self):
    r_cnt=0
    users_min = 2
    recipe_val = {}
    answers_cnt = {}
    for recipe in self.recipe_users:
        if len(self.recipe_users[recipe])<users_min:
          continue
        if len(self.recipe_users[recipe])>3:
          # print "Error: recipe {} is evaluated by {} users".format(recipe,len(recipe_users[recipe]))
          pass
        r_cnt+=1
        max_cnt=0
        max_val=None
        for a in self.answers:
          a_cnt = 0
          if recipe not in self.answers[a]:
            continue
          for usr in self.answers[a][recipe]:
            # if usr in self.trust_users:
              a_cnt+=1
          if a_cnt>max_cnt:# and a!='2':
            max_cnt = a_cnt
            max_val = a
          elif a_cnt==max_cnt:
            max_val = '2'
        recipe_val[recipe] = max_val
        if max_val not in answers_cnt:
          answers_cnt[max_val] = 1
        else:
          answers_cnt[max_val] += 1
    print "Recipes: {}".format(r_cnt)
    print "Answers stat:"
    for a in answers_cnt:
      print "{} : {}".format(a,answers_cnt[a])
    # for a in answers:
    #   cnt = 0
    #   for recipe in answers[a]:
    #     if len(recipe_users[recipe])<users_min:
    #       continue
    #     if len(recipe_users[recipe])>3:
    #       # print "Error: recipe {} is evaluated by {} users".format(recipe,len(recipe_users[recipe]))
    #       pass
    #     limit = math.ceil(float(len(recipe_users[recipe]))/2)
    #     # print limit
    #     if len(answers[a][recipe])>=limit:
    #       cnt+=1
    #   print "{} : {}".format(a,cnt)


obj = Eval()
obj.readData()
obj.getUserAgreement()
obj.printStat()
