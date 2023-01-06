from contextlib import nullcontext
import xml.dom.minidom
import xml.etree.ElementTree as ET

global state,states,global_idx
states=['organic',"nature",'conclusion']
global_idx=0
state=states[global_idx]


# def updateGoal(current_goal,goals):
#     root =Tree.getroot()
#     factBase=root.find('factBase')
#     facts = factBase.findall('fact')

#     for fact in facts:
#         if fact.attrib["name"]==current_goal:
#             return goals[goals.index(current_goal)+1]
#     return current_goal



#adds new fact to the factBase
def newFact(Tree,fact,name,value):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    if name=="conclusion":
        print("conclusion reached")
        state= "conclusion"
        #changeState(Tree,fact.attrib["name"])
        #print()
        return

    newElement = ET.SubElement(factBase,"fact")
    newElement.set("name",name)
    newElement.text=value
    print(f'ADDED NEW FACT == {newElement.attrib["name"]}')
    Tree.write("rules.xml")


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
        f=question.find(".//fact")
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
    rule_idx=0
    for rule in rules:
        facts = rule.findall(".//fact")
        fact_count=0
        not_in_fb=0
        for fact in facts:
            #if we find an antecedent, we check if it is in the factbase
            if fact.attrib["type"]=="if":
                if checkFactBase(Tree,fact.attrib["name"],fact.text):
                    fact_count+=1
                else:
                    not_in_fb+=1
            if fact.attrib["type"]=="then":
                #if the consequent is alr in the factbase, then we reset count to 0
                if checkFactBase(Tree,fact.attrib["name"],fact.text):
                    fact_count=0
        rule_count.append(fact_count)
        rule_idx+=1
    
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
        print(f"rule number = {counter}")
        facts = rule.findall(".//fact")
        check=0
        #doesnt implement or rule yet
        for fact in facts:
            if fact.attrib["type"]=="if":
                antecedent_count+=1
                check+=checkFactBase(Tree,fact.attrib["name"],fact.text)
                

            if check==antecedent_count and fact.attrib["type"]=="then" and checkFactBaseType(Tree,fact.attrib["name"])==False:
                print("IN")
                newFact(Tree,fact,fact.attrib["name"],fact.text)
            
        counter+=1

def getInput():
    print("press y for yes and n for no")
    answer = input()
    if answer=="y":
        return "true"
    if answer=="n":
        return "false"
    return

def askQuestion(Tree,question):
    desc = [x.text for x in question.findall(".//description")]
    try:
        if question.attrib["state"]!=nullcontext:
            nextState(Tree,question)
    except:
        print("CANNOT CHANGE STATE")
    fact=question.find(".//fact")
    for j in desc:
        print(j)
    fact.text=getInput()
    newFact(Tree,fact,fact.attrib["name"],fact.text)
    

#will be used for GUI. Currently asks question in terminal and returns fact
#asks question with a specific state
def getQuestion(Tree,state):
    root=Tree.getroot()
    questions=root.findall("question")
    desc=[]
    

    for question in questions:
        print(question.attrib)
        if question.attrib["state"]==state:
            desc= [x.text for x in question.findall(".//description")]
            fact=question.find(".//fact")
            askQuestion(Tree,question)
            break

    # for j in desc:
    #     print(j)
    # fact.text=getInput()
    # newFact(Tree,fact,fact.attrib["name"],fact.text)





        
# asks a question related to a fact in a rule that is not present in the FB
def askRelatedQuestion(Tree,rule):

    facts = rule.findall(".//fact")
    for fact in facts:
        if fact.attrib["type"]=="if" and checkFactBase(Tree,fact.attrib["name"],fact.text)==False:
            askQuestion(Tree,findQuestion(Tree,fact))
    return



    








# ##############################################################################################################################

def nextState(Tree,question ):
    global state, states, global_idx
    if question.attrib["state"]==state:
        global_idx+=1
        state=states[global_idx]



def changeState(Tree,s):
    getQuestion(Tree,s)
    global state
    

    while state==s:
        updateFactbase(Tree)
        askRelatedQuestion(Tree,checkRules(Tree))

    
    
    print(state)
    return


    


def main():
    Tree = ET.parse("rules.xml")
    root =Tree.getroot()

    tag=root.tag


    states=["organic","nature", "num_atoms", "agg_state", "reactivity","conclusion"]
    idx=0
    state=states[0]
    changeState(Tree,"organic")

main()









