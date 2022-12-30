import xml.dom.minidom
import xml.etree.ElementTree as ET

Tree = ET.parse("rules.xml")
root =Tree.getroot()

tag=root.tag
print(tag)

for child in root:
    print(child.tag, child.attrib)
print("===================")



def newFact(Tree,name,value):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    newElement = ET.SubElement(factBase,"fact")
    newElement.set("name",name)
    newElement.text=value
    Tree.write("rules2.xml")

    # for fact in facts:
    #     print(fact.tag,fact.attrib,fact.text)

def checkFactBase(Tree,name,value):
    #checks if a particular fact is in the factBase
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')

    for fact in facts:
        if fact.attrib==name and fact.text==value:
            return True


def updateFacts(Tree):
    root =Tree.getroot()
    rules = root.findall("rule")
    print(rules)
    counter=0
    for rule in rules:
        print(counter)
        ifs = rule.find(".//fact")
        print(ifs.tag,ifs.attrib,ifs.text)
        counter+=1




def getQuestion(nodelist):
    #finds all child/grandchild nodes with tag == 'description'
    desc=nodelist.findall(".//description")

    question = desc
    options = desc[:]
    for j in desc:
        print(j.text)
    return(desc)





# ##############################################################################################################################
for i in root.findall('question'):
    getQuestion(i)


#newFact(Tree,"Saturated","True")
updateFacts(Tree)
checkFactBase(Tree)







