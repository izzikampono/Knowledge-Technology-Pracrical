from contextlib import nullcontext
import xml.dom.minidom
import xml.etree.ElementTree as ET
import sys
from utils import *
# import guiTry
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, \
    QLineEdit, QInputDialog, QFormLayout, QBoxLayout, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QDoubleValidator
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from compound import *

class Model():
    Tree = ET.parse("rules.xml")
    root = Tree.getroot()
    states = ['organic',"nature","num_atoms","agg_state","reactivity",'conclusion']
    global_idx = -1
    state=states[global_idx]
    molar_mass = 0
    compound_weight = 0
    precipitate_weight = 0

    try:
        factBase = root.find("factBase")
    except:
        print("cant find factbase")


    #empties out factBase when program starts
    def reset(self):

        
        
        fb = self.root.find("factBase")

        for fact in fb.findall("fact") :
            fb.remove(fact)
        print("in")

        return

    # #adds new fact to the factBase
    def newFact(self,fact):

        Tree = self.Tree
        root = Tree.getroot()
        factBase = root.find("factBase")


        name = fact.attrib["name"]
        value = fact.text 
        
        root =Tree.getroot()
        factBase=root.find('factBase')
        # facts = factBase.findall('fact')

        # if name=="conclusion":
        #     print("conclusion reached")
        #     if value == "cannot classify":
        #         print("system cannot classify the compound")
        #         sys.exit("done")
        #     next()
        #     changeState(Tree,state)
        #     return
        
        # if name == "reactivity":
        #     next()


        try:
            newElement = ET.SubElement(factBase,"fact")
        except:
            print("ERROR : root global variable not found")
            sys.exit()
        newElement.set("name",name)
        newElement.text=value
        print(f'ADDED NEW FACT == {newElement.attrib["name"]}')
        Tree.write("rules.xml")
        self.updateFactbase()

    #checks if a specific factType is in the factBase
    def checkFactBaseType(self,name):
        
        root =self.Tree.getroot()
        factBase=root.find('factBase')
        facts = factBase.findall('fact')

        for fact in facts:
            if fact.attrib["name"]==name:
                return True
        return False

    #checks if a specifc fact is in the factBase
    def checkFactBase(self,name,value):
        root = self.Tree.getroot()
        factBase=root.find('factBase')
        facts = factBase.findall('fact')

        for fact in facts:
            if fact.attrib["name"]==name and fact.text==value:
                return True
        return False


# finds question that is related to a fact 
#the input should be a  fact that is needed to fulfill a specific rule  but is not present in the FB yet
    def findQuestion(self,fact):
        name=fact.attrib["name"]
        root=self.Tree.getroot()
        questions=root.findall(".//question")
        for question in questions:
            facts=question.findall(".//fact")
            for f in facts:
                if f.attrib["name"]==name:
                    return question



#make function to check which fact we need the most
    def checkRules(self):
        Tree=self.Tree
        root=Tree.getroot()
        rules=root.findall("rule")
        rule_count=[]
        factBase=root.find("factBase")
        rule_idx=0
        recent_fact=factBase.findall("fact")[-1]

        for rule in rules:
            facts = rule.findall(".//fact")
            fact_count=0
            not_in_fb=0
            for fact in facts:
                #if we find an antecedent, we check if it is in the factbase
                if fact.attrib["type"]=="if":
                    if fact.attrib["name"]==recent_fact.attrib["name"] and fact.text==recent_fact.text:
                        fact_count+=10
                    elif self.checkFactBase(Tree,fact.attrib["name"],fact.text):
                        fact_count+=1
                    else:
                        not_in_fb+=1
                if fact.attrib["type"]=="then":
                    #if the consequent is alr in the factbase, then we reset count to 0 so that the related question wont be called again
                    if self.checkFactBaseType(Tree,fact.attrib["name"]):
                        fact_count=0
            rule_count.append(fact_count)
            rule_idx+=1
        # print(rule_count)
        prioritized_rule = rules[rule_count.index(max(rule_count))]
        return prioritized_rule


        #checks facts in the factbase and sees if any of the rules can fire,
        # if yes, the rule fires and the resulting fact is added to the factbase
    def updateFactbase(self):
        rules = self.root.findall("rule")
        counter=0
        
        for rule in rules:
            antecedent_count=0
            # print(f"rule number = {counter}")
            facts = rule.findall(".//fact")
            check=0
            #doesnt implement or rule yet
            for fact in facts:
                if fact.attrib["type"]=="if":
                    antecedent_count+=1
                    check+=checkFactBase(Tree,fact.attrib["name"],fact.text)
                    

                if check==antecedent_count and fact.attrib["type"]=="then" and checkFactBase(Tree,fact.attrib["name"],fact.text)==False:
                    # print("IN")
                    newFact(fact)
                
            counter+=1

    def calculateNumAtoms(self):
        Mx={"flourinated":19,"brominated":80,"iodinated":127,"chlorinated":35.5}
        global molar_mass, compound_weight, precipitate_weight

        fb = self.root.find("factBase")
        facts = fb.findall("fact")

        for i in facts:
            if i.attrib["name"]=="nature":
                nature=i.text
        num_atoms = molar_mass*precipitate_weight/compound_weight*( 108 + Mx[nature])#type: ignore 

        if num_atoms ==1:
            return "monohalogenated"
        if num_atoms>1:
            return "polyhalogenated"
        return num_atoms 

    # def getAnswer(answer):
    #     dicty = makeDictionaryBool(current_question)
    #     return dicty[answer]



    #function to print out the question
    #also contains if statements for a number of unique questions 
    def askQuestion(self,question):
        desc = [x.text for x in question.findall(".//description")]
        fact=question.find(".//fact")
        for j in desc:
            print(j)
        if len(desc)==3 and desc[1]!="Double bond":

            #self.newFact(fact)
        elif desc[1]=="Double bond":
            index=int(input())-1
            fact = question.findall(".//fact")[index]
            self.newFact(fact)
        else:
            fact.text=desc[index]
            self.newFact(fact)

            
   
    #checks if latest fact requires user to input mass/weight
    root=Tree.getroot()
    fb=root.find("factBase")

    


    try:
        recent_fact = fb.findall("fact")[-1]
        recent_fact=recent_fact.attrib["name"].split("-")

        if recent_fact[0]=="input":
            print("input measurement :")
            m = float(input())

            if recent_fact[1]=="mass":
                self.molar_mass=m
            elif recent_fact[1]=="compound":
                compound_weight=m
            elif recent_fact[1]=="precipitate":
                precipitate_weight = m
            
            if precipitate_weight!=0:
                mm = calculateNumAtoms(self.Tree)
                fact = ET.Element("fact")
                fact.set("name","num_atoms")
                fact.text=mm
                self.newFact(fact)
    except:
        print("error for first fact in FB")
    


    try:
        print("try to change state")
        # print(question.attrib)
        if 'state' in question.attrib:
            # print("IN")
            self.nextState(question)
    except:
         print("CANNOT CHANGE STATE")
    

#will be used for GUI. Currently asks question in terminal and returns fact
#asks question with a specific state

def getQuestion(self):
    Tree = self.Tree
    root=Tree.getroot()
    questions=root.findall("question")
    

    for question in questions:
        if "state" in question.attrib:
            if question.attrib["state"]==self.ßstate:
                self.current_question=question
                return question
                break






        
# asks a question related to a fact in a rule that is not present in the FB
    def askRelatedQuestion(self,rule):
        Tree = self.Tree
        print("ask related question")
        facts = rule.findall("fact")
        for fact in facts:
            if fact.attrib["type"]=="if":
                if self.checkFactBaseType(Tree,fact.attrib["name"])==False:
                    # print(f'ask question abt {fact.attrib["name"]}')
                    self.current_question=self.findQuestion(fact)
                    break
        return



    
    def next(self):
        self.global_idx+=1
        self.state=self.states[self.global_idx]
        return 
    







# ##############################################################################################################################

def nextState(self,question ):
    s = question.attrib["state"].split(".")
    # print(s)
    if question.attrib["state"]=="nature":
        self.global_idx+=1
        self.state=self.states[self.global_idx]
        # print("changed state")
        return
    if question.attrib["state"]=="agg_state":
        self.global_idx+=1
        self.state=self.states[self.global_idx]
        # print("changed state")
        return

    if len(s)==2:
        
        # state = s[0]
        self.global_idx+=1
        self.state=self.states[self.global_idx]
        print("changed state")
        return
    if question.attrib["state"]=="nature.next":
        self.global_idx+=1
        self.state=self.states[self.global_idx]
    
    return


#recursive function to run the program
def changeState(self,s):

    if s=="conclusion":

        print("===== END =====")
        return
    
    global state,current_question
    current_question = self.getQuestion()
    self.askQuestion(self.Tree,current_question)
    print(f"state = {self.state}")

    state=""
    #change this later
    while state==s and state!="conclusion":
        self.updateFactbase(self.Tree)
        self.askRelatedQuestion(self.Tree,self.checkRules(self.Tree))
    print(state)
    self.changeState(self.Tree,state)

    def changeState2(self):
        global state,current_question
        s = state
        if state=="conclusion":
            print("===== END =====")
            return
        self.updateFactbase(self.Tree)
        if state=="":
            rules = self.checkRules(self.Tree)
            self.askRelatedQuestion(self.Tree,rules)
        else:
            print("in get question")
            q = self.getQuestion()
            self.askQuestion(self.Tree,q)
        return


    





def system_output():
    Tree = ET.parse("rules.xml")
    compound = Compound()
    dict = loadFactBase(Tree)
    compound.import_dict(dict)

    pprint(vars(compound))
    compound.eliminate()

# ###################################################################################



# changeState2(Tree)
fact = ET.Element("fact")
fact.set("name","organic")
fact.text="true"


model = Model()
model.reset()
model.newFact(fact)










