import numpy as np
import json
import xml.etree.ElementTree as ET
import sys
import inspect
from pprint import pprint



def loadKB(file):
    f = open(file)
  
    # returns JSON object as a dictionary
    data = json.load(f)
  
    # Iterating through the json list
    # for i in data:
    #     print(i)
  
    # Closing file
    f.close()
    return data


def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

class Compound():
    name=""
    nature=""
    num_atoms=""
    position=""
    saturation= ""
    reactivity=""
    state =""
    polarity=""
    fact_base=loadKB("kb2.json")
    possible_list=[]

    def setter(self,s):
        if s[0] =="name":
            self.name=s[1]
            return
        if s[0] =="num_atoms":
            self.num_atoms=s[1]
            return
        if s[0] =="nature":
            self.nature=s[1]
            return
        if s[0] =="position":
            self.position=s[1]
            return
        if s[0] =="saturation":
            self.saturation=s[1]
            return
        if s[0] =="reactivity":
            self.reactivity=s[1]
            return
        if s[0] =="state":
            self.state=s[1]
            return
        if s[0] =="polarity":
            self.polarity=s[1]
            return
        
    @classmethod
    def initialize_possibilities(cls):
        for i in cls.fact_base:
            cls.possible_list.append(str(i["name"]))
    
    def eliminate(self):
        """" this function checks the existing attributes of the compound 
        and eliminates all other compounds that do not have the same attributes"""

        self.initialize_possibilities()
        this_compound = self.__dict__
        for compound in self.fact_base:
            for i,j in this_compound.items():
                #print(i,j)
                if i=="name":
                    pass
                    print("YAY")
                if this_compound[i]!=compound[i] and j!="":
                    try: 
                        self.possible_list.remove(compound["name"])
                        print("removed {}".format(compound["name"]))
                        break
                    except:
                        print("{} not in list".format(compound["name"]))
            
        print(f"list of possible compounds : {self.possible_list}")
        return






    # def __init__(self,nature,num_atoms,position,nature_hydro,reactivity,state,polarity):
    #     self.nature=nature
    #     self.num_atoms=num_atoms
    #     self.position=position
    #     self.nature_hydro=nature_hydro
    #     self.reactivity=reactivity
    #     self.state=state
    #     self.polarity=polarity
    #     return
    
    def import_dict(self,fact_dict):
        for i in fact_dict.items():
            self.setter(i)
        return


    def to_dict(self):
        dictionary={
            "name" : self.name,
            "nature" : self.nature,
            "num_atoms" : self.num_atoms,
            "position" : self.position,
            "nature_hydro" : self.saturation,
            "reactivity" : self.reactivity,
            "state" : self.state,
            "polarity" : self.polarity,
            "num_atoms" : self.num_atoms }
        return dictionary

def Match(Compound,kb_name):
    "IN MATCH"
    KB=loadKB(kb_name)
    Compound=Compound.__dict__
    counter = {}
    for Halogen in KB:
        counter[Halogen["name"]]=0
        for i,j in zip(Halogen,Compound):
            if j=="name":
                pass
            if Halogen[i]==Compound[j]:
                print("The compound has {} of {} which is the same as  {} that has {} ".format(i,Halogen[i],Compound["name"],Compound[j]))
                counter[Halogen["name"]]+=1
        print("\n NEW")
    print(max(counter))
    
    
    return counter

def loadFactBase(Tree):
    root =Tree.getroot()
    factBase=root.find('factBase')
    facts = factBase.findall('fact')
    facts_dictionary={}


    for fact in facts:
        if fact.attrib["name"] in props(Compound)[1:7]:
            facts_dictionary[fact.attrib["name"]]=fact.text
    return facts_dictionary

def getAttrib(Compound):
    inspect.getmembers(Compound)


############################## MAIN ##################################


# test = Compound()
# setattr(test,'nature',"Chlorinated")
# setattr(test,"num_atoms","Monohalogenated")
#setattr(test,"position","Saturated")
#print(test.nature)

# print(inspect.getmembers(Compound)
# )
# Tree = ET.parse("rules.xml")

# dict = loadFactBase(Tree)
# test.import_dict(dict)

# pprint(vars(test))
# test.eliminate()


#Match(test,"kb2.json")


    


    

