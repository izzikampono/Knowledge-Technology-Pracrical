from contextlib import nullcontext
import xml.dom.minidom
import xml.etree.ElementTree as ET
import sys
from compound import *

#extracts the question out of a question tag
def getQuestion(question):
    return question.find("description").text


#exports question tag into a dictionary with all options and facts.
# only works for yes or no questions
def makeDictionaryBool(question):
    dictionary={}
    descriptions = question.findall(".//description")
    dictionary[descriptions[0].text]=[]
    facts = question.findall(".//fact")

    for i,j in zip(descriptions[1:],facts):
        dictionary[i.text]=j
    print(dictionary)
    return dictionary


#extracts answer options from a question tag
def getOptions(question):
    options=[]
    descriptions=question.findall(".//description")
    
    for i in descriptions[1:]:
        options.append(i)
    return options



#gets the corresponding facts to each option in a question,
#returns a dictionary of quesition options linked to facts 
def getCorrespondingFact(question,userAnswer):
    answer = -5
    if userAnswer=="yes":
        answer = 0 
    elif userAnswer=="no":
        answer = 1
    facts = question.findall(".//fact")

    return facts[answer]

# def clickButton(userInput,Tree):
#     root = Tree.getroot()
#     questions = root.findall(".//question")
#     for i in questions:
#         name

#gets a question element given a state
def getQuestionState(Tree,state):
    root=Tree.getroot()
    questions=root.findall("question")
    

    for question in questions:
        if "state" in question.attrib:
            if question.attrib["state"]==state:
                return question







# def getCorrespondingFact(question):
#     options_facts = {}
#     facts = question.findall(".//fact")
#     options = question.findall(".//description")[1:]

#     for i,j in zip(options,facts):
#         options_facts[i]=j
        
#################################################################
Tree = ET.parse("rules.xml")
root =Tree.getroot()
root.find("question")

makeDictionaryBool(root.findall("question")[4])

