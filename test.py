import xml.dom.minidom
import xml.etree.ElementTree as ET

domTree = xml.dom.minidom.parse("rules.xml")
Tree = ET.parse("rules.xml")
root =Tree.getroot()

tag=root.tag
print(tag)

group = domTree.documentElement

facts = group.getElementsByTagName('fact')
questions = group.getElementsByTagName('question')
# facts_in_question=questions.getElementByTagName('fact')

for c in root.findall('question'):
    att = c.attrib
    print(att)
    desc = c.findall("description")
    for i in desc:
        print(i.tag,i.attrib,i.text)


def getQuestion(nodelist):
    desc=nodelist.findall("description")

    question = desc[0]
    print(question.text)
    options = desc[1:]
    for j in options:
        print(j.text)
    return(desc)


for i in root.findall('question'):
    getQuestion(i)



# for i in facts:
#     print(f"{i.getAttribute('name')} --> {i.childNodes[0].nodeValue}" )

# for i in questions:
#     print(f"{i.find('description').text}")

#print(facts_in_question.childNodes[0].nodeValue)





