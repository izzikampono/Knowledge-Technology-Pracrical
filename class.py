import numpy as np
import json


def loadKB(file):
    f = open(file)
  
    # returns JSON object as a dictionary
    data = json.load(f)
  
    # Iterating through the json list
    for i in data:
        print(i)
  
    # Closing file
    f.close()
    return data

class Compound():
    nature=""
    num_atoms=0
    position=""
    nature_hydro= ""
    Reactivity=""
    State =""
    Polarity=""
    fact_base=loadKB("kb.json")


    def init(self,nature,num_atoms,position,nature_hydro,reactivity,state,polarity):
        self.nature=nature
        self.num_atoms=num_atoms
        self.position=position
        self.nature_hydro=nature_hydro
        self.reactivity=reactivity
        self.state=state
        self.polarity=polarity
        return

    def export(self):
        dictionary={"nature" : self.nature,
            "num_atoms" : self.num_atoms,
            "position" : self.position,
            "nature_hydro" : self.nature_hydro,
            "Reactivity" : self.Reactivity,
            "State" : self.State,
            "Polarity" : self.polarity,
            "num_atoms" : self.num_atoms }
        return dictionary

def Match(Compound,kb_name):
    KB=loadKB(kb_name)
    counter = 0
    for i,j in zip(Compound,KB):
        if i==j:
            counter+=1
    
    return counter


    


    

