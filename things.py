def Aspects(aspect_list = []):
    aspect_dict = {}
    for i, aspect in enumerate(aspect_list):
        name = "High Concept" if i == 0 else "Trouble" if i == 1 else str(i-1)
        aspect_dict[name] = aspect
    return(aspect_dict)

def Stunts(stunt_list = []): 
    stunt_dict = {}
    for i, stunt in enumerate(stunt_list):
        stunt_dict[str(i+1)] = stunt
    return(stunt_dict)

approach_list = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
def Approaches(one = 0, two = 0, thr = 0, fou = 0, fiv = 0, six = 0):
    approach_dict = {
        approach_list[0] : one, approach_list[1] : two, approach_list[2] : thr,
        approach_list[3] : fou, approach_list[4] : fiv, approach_list[5] : six}
    return(approach_dict)

def Damage(damage_list = [], count_list = []):
    damage_dict = {}
    for damage, count in zip(damage_list, count_list):
        damage_dict[str(damage)] = [[] for _ in range(count)]
    return(damage_dict)
        


import pickle 
import tkinter as tk
from tkinter import filedialog

class Thing:
    
    def __init__(
            self, name = "ANONYMOUS", description = "", fate_points = 0, refresh = 0, 
            aspects = Aspects(), stunts = Stunts(), approaches = Approaches(),  
            stress = Damage([1, 2, 3], [1, 1, 1]), consequences = Damage([2, 4, 6], [1, 1, 1]),
            load = False):
        
        self.name = name ; self.description = description 
        self.fate_points = fate_points ; self.refresh = refresh
        self.aspects = aspects ; self.stunts = stunts
        self.approaches = approaches
        self.stress = stress ; self.consequences = consequences
        self.failed = False
        
        if(load):
            root = tk.Tk() ; root.withdraw()
            file_path = filedialog.askopenfilename()
            with open(file_path.format(self.name), 'rb') as handle:
                self = pickle.load(handle)
            
    def save(self):
        root = tk.Tk() ; root.withdraw()
        file_path = filedialog.askdirectory()
        with open('{}/{}.pickle'.format(file_path, self.name), 'wb') as handle: 
            pickle.dump(self, handle)
            
    def __str__(self):
        return(
"""Name: {}. Description: {}.
Fate Points: {}. Refresh: {}.
Aspects: {}. 
Stunts: {}. 
Approaches: {}.
Stress: {}. 
Consequences: {}.""".format(
self.name, self.description, 
self.fate_points, self.refresh, 
self.aspects, self.approaches, self.stunts, self.stress, self.consequences))
    
    

if __name__ == "__main__":
    example = Thing(
        name = "Example Thing", description = "An example thing", 
        fate_points = 0, refresh = 0, 
        aspects = Aspects(["An awesome example", "With a problem", "And other stuff"]), 
        stunts = Stunts(["In this situation, I'm better at this!", "In this other situation, I'm better at this other thing!"]), 
        approaches = Approaches(1,2,3,4,5,6), 
        stress = Damage([1, 2, 3], [1, 2, 1]), 
        consequences = Damage([2, 4, 6], [1, 2, 1]),
        load = False)
    example.stress["2"][0] = "Muscle cramp"
    example.consequences["4"][0] = "Broken arm"
    print(example)
    example.save()