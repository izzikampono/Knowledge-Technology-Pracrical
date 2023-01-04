from contextlib import nullcontext
import xml.dom.minidom
import xml.etree.ElementTree as ET



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
        changeState(Tree,fact.attrib["name"])
        print()

    newElement = ET.SubElement(factBase,"fact")
    newElement.set("name",name)
    newElement.text=value
    Tree.write("rules.xml")




#checks if a particular fact is in the factBase
def checkFactBase(Tree,name,value):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    for fact in facts:
        if fact.attrib["name"]==name and fact.text==value:
            return True
    return False

#input : fact that is needed to fulfill a specific rule  but is not present in the FB yet
def findQuestion(Tree,fact):
    name=fact.attrib["name"]
    root=Tree.getroot()
    questions=root.findall(".//question")
    for question in questions:
        f=question.find("fact")
        if f.attrib["name"]==name:
            return question

#filters list of nodes
def filter(nodeList,key):
    a=[]
    for i in nodeList:
        if i.attrib["type"]==key:
            a.append(i)
    return a


#checks facts in the factbase and sees if any of the rules can fire,
# if yes, the rule fires and the resulting fact is added to the factbase
def updateFacts(Tree):
    root =Tree.getroot()
    rules = root.findall("rule")
    print(rules)
    counter=0
    check=0
    antecedent_count=0
    for rule in rules:
        print(counter)
        facts = rule.findall(".//fact")
        #doesnt implement or rule yet
        for fact in facts:

            print(f"{fact.attrib}\n")
            print(f"check = {check}")
            if fact.attrib["type"]=="if":
                antecedent_count+=1
                check+=checkFactBase(Tree,fact.attrib["name"],fact.text)
                

            if check and fact.attrib["type"]=="then":
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
    

#will be used for GUI. Currently asks question in terminal and returns fact
def getQuestion(Tree,state):
    root=Tree.getroot()
    questions=root.findall("question")
    desc=[]
    

    for question in questions:
        print(question.attrib)
        if question.attrib["state"]==state:
            desc= [x.text for x in question.findall(".//description")]
            fact=question.find(".//fact")
            break

    for j in desc:
        print(j)
    fact.text=getInput()
    newFact(Tree,fact,fact.attrib["name"],fact.text)
    #updateFacts(Tree)

def askQuestion(Tree,question):
    desc = [x.text for x in question.findall(".//description")]
    fact=question.find(".//fact")
    for j in desc:
        print(j)
    fact.text=getInput()
    newFact(Tree,fact,fact.attrib["name"],fact.text)


#make function to check which fact we need the most
def checkRules(Tree):
    root=Tree.getroot()
    rules=root.findall("rules")
    rule_count=[]
    rule_idx=0
    for rule in rules:
        facts = rule.findall(".//fact")
        fact_count=0
        for fact in facts:
            #if we find an antecedent, we check if it is in the factbase
            if fact.attrib["type"]=="if":
                fact_count+=int(checkFactBase(Tree,fact.attrib["name"],fact.text))
            if fact.attrib["type"]=="then":
                #if resulting fact is alr in the factbase, then we reset count to 0
                if checkFactBase(Tree,fact.attrib["name"],fact.text):
                    fact_count=0
        rule_count[rule_idx]=fact_count
        rule_idx+=1
    
    prioritized_rule = rules[rule_count.index(max(rule_count))]
    return prioritized_rule


        

def askRelatedQuestion(Tree,rule):

    facts = rule.findall(".//fact")
    for fact in facts:
        if fact.attrib["type"]=="if" and checkFactBase(Tree,fact.attrib["name"],fact.text)==False:
            askQuestion(findQuestion(Tree,fact))
    return



    








# ##############################################################################################################################

global state

def changeState(Tree,s):
    getQuestion(Tree,s)


    


def main():
    Tree = ET.parse("rules.xml")
    root =Tree.getroot()

    tag=root.tag


    states=["organic","nature", "num_atoms", "agg_state", "reactivity","conclusion"]
    idx=0
    changeState(Tree,states[idx])

main()









