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
    states = ['organic',"nature","num_atoms","agg_state","bond_type","reactivity",'conclusion']
    global_idx = 0
    state=states[global_idx]
    molar_mass = 0
    compound_weight = 0
    current_question = root.find("question")
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

        
        # if name == "reactivity":
        #     self.state = "conclusion"
    

        try:
            newElement = ET.SubElement(factBase,"fact")
        except:
            print("ERROR : root global variable not found")
            sys.exit()
        newElement.set("name",name)
        newElement.text=value
        print(f'ADDED NEW FACT == {newElement.attrib["name"]}')
        Tree.write("rules.xml")

        if name=="conclusion":
            self.state = "conclusion"
            print("conclusion reached")
            if value == "cannot classify":
                print("system cannot classify the compound")
                # sys.exit("done")
            # self.changeState2()
            print("DONE")
            print(f"current state : {self.state}")
            
        return
        # self.updateFactbase()

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
    def updateXML(self):
        self.Tree = ET.parse("rules.xml")
        self.root = self.Tree.getroot()
        return
    def checkConclusion(self):
        self.updateXML()
        self.updateFactbase()
        fb = self.root.find("factBase")
        recent_fact = fb.findall("fact")[-1]
        if recent_fact.attrib["name"]=="conclusion":
            goal = self.root.find("goal")
            conclusions=goal.findall("answer")
            for i in conclusions:
                if i.attrib['value'] == recent_fact.text:
                    return i

            return recent_fact.text
        else :
            print("check conclusion : not conclusion fact in factBase")
        return False


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
                    elif self.checkFactBase(fact.attrib["name"],fact.text):
                        fact_count+=1
                    else:
                        not_in_fb+=1
                if fact.attrib["type"]=="then":
                    #if the consequent is alr in the factbase, then we reset count to 0 so that the related question wont be called again
                    if self.checkFactBaseType(fact.attrib["name"]):
                        fact_count=0
            rule_count.append(fact_count)
            rule_idx+=1
        # print(rule_count)
        prioritized_rule = rules[rule_count.index(max(rule_count))]
        return prioritized_rule


        #checks facts in the factbase and sees if any of the rules can fire,
        # if yes, the rule fires and the resulting fact is added to the factbase
    def updateFactbase(self):
        self.updateXML()
        rules = self.root.findall("rule")
        counter=0
        
        if self.state=="conclusion":
            return

        for rule in rules:
            antecedent_count=0
            # print(f"rule number = {counter}")
            facts = rule.findall(".//fact")
            check=0
            #doesnt implement or rule yet
            for fact in facts:
                if fact.attrib["type"]=="if":
                    antecedent_count+=1
                    check+=self.checkFactBase(fact.attrib["name"],fact.text)

                if check==antecedent_count and fact.attrib["type"]=="then" and self.checkFactBase(fact.attrib["name"],fact.text)==False:
                    # print("IN")
                    self.newFact(fact)
                
            counter+=1

    def calculateNumAtoms(self,molar_mass, compound_weight,precipitate_weight):
        Mx={"flourinated":19,"brominated":80,"iodinated":127,"chlorinated":35.5}

        fb = self.root.find("factBase")
        facts = fb.findall("fact")
        text = ""

        if molar_mass==None or compound_weight==None or precipitate_weight==None:
            print("unable to calculate num atoms")
            return 

        for i in facts:
            if i.attrib["name"]=="nature":
                nature=i.text
        num_atoms = molar_mass*precipitate_weight/compound_weight*( 108 + Mx[nature])#type: ignore 

        if num_atoms == 1:
            text = "monohalogenated"
        if num_atoms>1:
            text =  "polyhalogenated"

        fact = ET.Element("fact")
        fact.set("name","num_atoms")
        fact.text = text
        self.newFact(fact)
        self.next()
        return 

    

    def checkState(self):
        print("IN checkState ")
        if self.state == "conclusion":
            return
        try:
            print("try to change state")
            print(self.state)

            self.updateFactbase()
            if 'state' in self.current_question.attrib:
                # print("IN")
                self.nextState()
            # else:
                # print("state changed to =''")
                # self.state=""
        except:
            self.state=""
            print("CANNOT CHANGE STATE")
        return
    

#will be used for GUI. Currently asks question in terminal and returns fact
#asks question with a specific state

    def getQuestion(self):
        Tree = self.Tree
        root=Tree.getroot()
        questions=root.findall("question")
        

        for question in questions:
            if "state" in question.attrib:
                if question.attrib["state"]==self.state:
                    self.current_question=question
                    return question
                    






        
# asks a question related to a fact in a rule that is not present in the FB
    def askRelatedQuestion(self,rule):
        Tree = self.Tree
        print("ask related question")
        facts = rule.findall("fact")
        for fact in facts:
            if fact.attrib["type"]=="if":
                if self.checkFactBaseType(fact.attrib["name"])==False:
                    self.current_question = self.findQuestion(fact)
                    return self.current_question
        return



    
    def next(self):
        try:
            idx = self.states.index(self.state)
            self.state= self.states[idx+1]
        except:
            self.global_idx+=1
            self.state=self.states[self.global_idx]
        return 
    






        question = self.current_question

# ##############################################################################################################################

    def nextState(self):
        question = self.current_question
        Tree = ET.parse("rules.xml")
        root = Tree.getroot()
        fb = root.find("factBase")
        recent_fact = fb.findall("fact")[-1]
        recent_fact_name = recent_fact.attrib["name"]
        print(f"recent fact : {recent_fact_name}")
        s = question.attrib["state"].split(".")
        if self.state == "conclusion":
            return
        if recent_fact_name == "precipitate-color" or recent_fact_name=="nature":
            self.state = "num_atoms"
            print(f"state changed to {self.state}")
            return
        if recent_fact_name == "num_atoms":
            self.state = "agg_state"
            print(f"state changed to {self.state}")

            return
        if recent_fact_name== "aggregation-state":

            self.state = "bond_type"
            print(f"state changed to {self.state}")

            return
        if recent_fact_name=="normal-bond" or recent_fact_name=="double-bond":
            self.state = "reactivity"
            print(f"state changed to {self.state}")

            return
        if recent_fact_name == "reactivity":
            self.state = "conclusion"
            print(f"state changed to {self.state}")

            return
        
        
        self.state =""
        return

    def mostRecent(self):
        fb = self.root.find("factBase")
        try:
            recent_fact = fb.findall("fact")[-1]
        except:
            print("empty")
            return False
        if "name" in recent_fact.attrib:
            s=recent_fact.attrib["name"].split("-")
            if s[0]=="input":
                return True
        return False

    def changeState2(self):
        print(f"current state : {self.state} \n")
        if self.state=="conclusion":
            print("===== END =====")
            return
        self.updateFactbase()
        self.checkState()
        if self.state=="":
            rules = self.checkRules()
            self.askRelatedQuestion(rules)
        else:
            print("in get question")
            self.getQuestion()
        return

    def system_output(self):
        self.Tree = ET.parse("rules.xml")
        compound = Compound()
        dict = loadFactBase(self.Tree)
        compound.import_dict(dict)

        pprint(vars(compound))
        return compound.eliminate()
        

# ###################################################################################



# changeState2(Tree)
fact = ET.Element("fact")
fact.set("name","organic")
fact.text="true"


model = Model()
model.reset()










