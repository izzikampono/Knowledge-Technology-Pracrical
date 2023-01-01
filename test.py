import xml.dom.minidom
import xml.etree.ElementTree as ET

Tree = ET.parse("rules.xml")
root =Tree.getroot()

tag=root.tag

for child in root:
    print(child.tag, child.attrib)
print("===================")


goals=["organic","nature",""]
cur_goal=0

def updateGoal(current_goal,goals):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    for fact in facts:
        if fact.attrib["name"]==current_goal:
            return goals[goals.index(current_goal)+1]
    return current_goal

#adds new fact to the factBase
def newFact(Tree,name,value):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

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
                newFact(Tree,fact.attrib["name"],fact.text)
            
        counter+=1



#will be used for GUI
def getQuestion(nodelist):
    #finds all child/grandchild nodes with tag == 'description'
    desc=nodelist.findall(".//description")

    question = desc
    options = desc[:]
    for j in desc:
        print(j.text)
    return(desc)

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
            if fact.attrib["type"]=="if":
                fact_count+=int(checkFactBase(Tree,fact.attrib["name"],fact.text))
        rule_count[rule_idx]=fact_count
        rule_idx+=1
    
    prioritized_rule = rules[rule_count.index(max(rule_count))]
    return prioritized_rule

def askRelatedQuestion(prioritized_rule):
    
    return





# ##############################################################################################################################
for i in root.findall('question'):
    getQuestion(i)


#newFact(Tree,"Saturated","True")
updateFacts(Tree)
# checkFactBase(Tree)







