from contextlib import nullcontext
import xml.dom.minidom
import xml.etree.ElementTree as ET
import sys

from compound import *


global state,states,global_idx, molar_mass, compound_weight, precipitate_weight
global current_question
states=['organic',"nature","num_atoms","agg_state","reactivity",'conclusion']
current_question = None
global_idx=0
state=states[global_idx]
molar_mass=0
compound_weight=0
precipitate_weight=0


def reset(Tree):
    root=Tree.getroot()
    fb=root.find("factBase")
    # iterator=fb.getiterator("fact")

    for fact in fb.findall("fact") :
       fb.remove(fact)

    return




#adds new fact to the factBase
def newFact(Tree,fact):
    name = fact.attrib["name"]
    value = fact.text 
    global state
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    if name=="conclusion":
        print("conclusion reached")
        if value == "cannot classify":
            print("system cannot classify the compound")
            sys.exit("done")
        next()
        changeState(Tree,state)
        #state= "conclusion"
        #sys.exit("done")
        #changeState(Tree,fact.attrib["name"])
        #print()
        return
    
    if name == "reactivity":
        next()


    newElement = ET.SubElement(factBase,"fact")
    newElement.set("name",name)
    newElement.text=value
    print(f'ADDED NEW FACT == {newElement.attrib["name"]}')
    Tree.write("rules.xml")
    updateFactbase(Tree)


def checkFactBaseType(Tree,name):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    for fact in facts:
        if fact.attrib["name"]==name:
            return True
    return False

#checks if a specifc fact is in the factBase
def checkFactBase(Tree,name,value):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    for fact in facts:
        if fact.attrib["name"]==name and fact.text==value:
            return True
    return False


# finds question that is related to a fact 
#input : fact that is needed to fulfill a specific rule  but is not present in the FB yet
def findQuestion(Tree,fact):
    name=fact.attrib["name"]
    root=Tree.getroot()
    questions=root.findall(".//question")
    for question in questions:
        facts=question.findall(".//fact")
        for f in facts:
            if f.attrib["name"]==name:
                return question

#filters list of nodes
def filter(nodeList,key):
    a=[]
    for i in nodeList:
        if i.attrib["type"]==key:
            a.append(i)
    return a

#make function to check which fact we need the most
def checkRules(Tree):
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
                elif checkFactBase(Tree,fact.attrib["name"],fact.text):
                    fact_count+=1
                else:
                    not_in_fb+=1
            if fact.attrib["type"]=="then":
                #if the consequent is alr in the factbase, then we reset count to 0 so that the related question wont be called again
                if checkFactBaseType(Tree,fact.attrib["name"]):
                    fact_count=0
        rule_count.append(fact_count)
        rule_idx+=1
    # print(rule_count)
    prioritized_rule = rules[rule_count.index(max(rule_count))]
    return prioritized_rule

def getCurrentQuestion():
    global current_question
    return current_question

def checkRules2(Tree):
    root=Tree.getroot()
    rules=root.findall("rule")
    factBase=root.find("factBase")
    recent_fact=factBase.findall("fact")[-1]
    rule_count=[]
    rule_idx=0
    for rule in rules:
        facts = rule.findall("fact")
        fact_count=0
        not_in_fb=0
        for fact in facts:
            #if we find an antecedent, we check if it is in the factbase
            if fact.attrib["type"]=="if" :

                if fact.attrib["name"]==recent_fact.attrib["name"]:
                    fact_count+=10
                if checkFactBase(Tree,fact.attrib["name"],fact.text):
                    fact_count+=1
            if fact.attrib["type"]=="then":
                #if the consequent is alr in the factbase, then we reset count to 0 so that the related question wont be called again
                if checkFactBaseType(Tree,fact.attrib["name"]):
                    fact_count=0
        rule_count.append(fact_count)
        rule_idx+=1
    # print(rule_count)
    prioritized_rule = rules[rule_count.index(max(rule_count))]
    return prioritized_rule


#checks facts in the factbase and sees if any of the rules can fire,
# if yes, the rule fires and the resulting fact is added to the factbase
def updateFactbase(Tree):
    root =Tree.getroot()
    rules = root.findall("rule")
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
                newFact(Tree,fact)
            
        counter+=1

def getInput():
    print("press y for yes and n for no")
    answer = input()
    if answer=="y":
        return "true"
    if answer=="n":
        return "false"
    return

def getInput2():
    print("press number 1-4")
    answer = input()
    if answer=="1":
        return 1
    if answer=="2":
        return 2
    if answer=="3": 
        return 3
    if answer=="4":
        return 4
    return 0

def calculateNumAtoms(Tree):
    Mx={"flourinated":19,"brominated":80,"iodinated":127,"chlorinated":35.5}
    global molar_mass, compound_weight, precipitate_weight

    root = Tree.getroot()
    fb = root.find("factBase")
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

#function to print out the question
#also contains if statements for a number of unique questions 
def askQuestion(Tree,question):
    desc = [x.text for x in question.findall(".//description")]
    fact=question.find(".//fact")
    for j in desc:
        print(j)
    if len(desc)==3 and desc[1]!="Double bond":
        fact.text=getInput()
        newFact(Tree,fact)

    elif desc[1]=="Double bond":
        index=int(input())-1
        fact = question.findall(".//fact")[index]
        newFact(Tree,fact)
    else:
        index=int(getInput2())
        fact.text=desc[index]
        newFact(Tree,fact)

        
   
    #checks if latest fact requires user to input mass/weight
    root=Tree.getroot()
    fb=root.find("factBase")

    

    global precipitate_weight, molar_mass, compound_weight

    try:
        recent_fact = fb.findall("fact")[-1]
        recent_fact=recent_fact.attrib["name"].split("-")

        if recent_fact[0]=="input":
            print("input measurement :")
            m = float(input())

            if recent_fact[1]=="mass":
                molar_mass=m
            elif recent_fact[1]=="compound":
                compound_weight=m
            elif recent_fact[1]=="precipitate":
                precipitate_weight = m
            
            if precipitate_weight!=0:
                mm = calculateNumAtoms(Tree)
                fact = ET.Element("fact")
                fact.set("name","num_atoms")
                fact.text=mm
                newFact(Tree,fact)
    except:
        print("error for first fact in FB")
    
    



    updateFactbase(Tree)


    try:
        print("try to change state")
        # print(question.attrib)
        if 'state' in question.attrib:
            # print("IN")
            nextState(Tree,question)
    except:
         print("CANNOT CHANGE STATE")
    

#will be used for GUI. Currently asks question in terminal and returns fact
#asks question with a specific state
def getQuestion(Tree,state):
    global current_question
    root=Tree.getroot()
    questions=root.findall("question")
    

    for question in questions:
        if "state" in question.attrib:
            if question.attrib["state"]==state:
                current_question=question
                return question
                break






        
# asks a question related to a fact in a rule that is not present in the FB
def askRelatedQuestion(Tree,rule):
    global current_question

    print("ask related question")
    facts = rule.findall("fact")
    for fact in facts:
        if fact.attrib["type"]=="if":
            if checkFactBaseType(Tree,fact.attrib["name"])==False:
                # print(f'ask question abt {fact.attrib["name"]}')
                current_question=findQuestion(Tree,fact)
                askQuestion(Tree,current_question)
                break
    return



    
def next():
    global state,states,global_idx
    global_idx+=1
    state=states[global_idx]
    return 
    







# ##############################################################################################################################

def nextState(Tree,question ):
    global state, states, global_idx
    s = question.attrib["state"].split(".")
    # print(s)
    if question.attrib["state"]=="nature":
        global_idx+=1
        state=states[global_idx]
        # print("changed state")
    if question.attrib["state"]=="agg_state":
        global_idx+=1
        state=states[global_idx]
        # print("changed state")
        return

    if len(s)==2:
        
        # state = s[0]
        global_idx+=1
        state=states[global_idx]
        print("changed state")
        return
    if question.attrib["state"]=="nature.next":
        global_idx+=1
        state=states[global_idx]
    
    return


#recursive function to run the program
def changeState(Tree,s):
    global state,current_question
    current_question = getQuestion(Tree,s)
    askQuestion(Tree,current_question)
    print(f"state = {state}")

    if s=="conclusion":

        print("===== END =====")
        return
    
    #change this later
    while state==s and state!="conclusion":
        updateFactbase(Tree)
        askRelatedQuestion(Tree,checkRules(Tree))
    print(state)
    changeState(Tree,state)
    
  
    return


    


def start():
    Tree = ET.parse("rules.xml")
    root =Tree.getroot()
    reset(Tree)

    tag=root.tag


    states=["organic","nature", "num_atoms", "agg_state", "reactivity","conclusion"]
    idx=0
    state=states[0]
    changeState(Tree,"organic")
    return


def system_output():
    Tree = ET.parse("rules.xml")
    compound = Compound()
    dict = loadFactBase(Tree)
    compound.import_dict(dict)

    pprint(vars(compound))
    compound.eliminate()

#######################################################################











