import numpy as np
import json


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

class Compound():
    name=""
    nature=""
    num_atoms=""
    position=""
    nature_hydro= ""
    reactivity=""
    state =""
    polarity=""
    fact_base=loadKB("kb2.json")
    possible_list=[]

    @classmethod
    def initialize_possibilities(cls):
        for i in cls.fact_base:
            cls.possible_list.append(str(i["name"]))
        #print(f"INITIALIZED : {cls.possible_list}\n")
    
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
                if this_compound[i]!=compound[i]:
                    try: 
                        self.possible_list.remove(compound["name"])
                        print("removed {}".format(compound["name"]))
                        break
                    except:
                        print("{} not in list".format(compound["name"]))
            
        print(f"list of possible compounds : {self.possible_list}")
        return








    def init(self,nature,num_atoms,position,nature_hydro,reactivity,state,polarity):
        self.nature=nature
        self.num_atoms=num_atoms
        self.position=position
        self.nature_hydro=nature_hydro
        self.reactivity=reactivity
        self.state=state
        self.polarity=polarity
        return

    @classmethod
    def to_dict(self):
        dictionary={
            "name" : self.name,
            "nature" : self.nature,
            "num_atoms" : self.num_atoms,
            "position" : self.position,
            "nature_hydro" : self.nature_hydro,
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



test = Compound()
setattr(test,'nature',"Chlorinated")
setattr(test,"num_atoms","Monohalogenated")
#setattr(test,"position","Saturated")
print(test.nature)
test.eliminate()


#Match(test,"kb2.json")


    


    

