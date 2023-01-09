approach_list = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
def New_Approaches(one_to_six = [0,0,0,0,0,0]):
    approaches = {approach_list[i] : str(one_to_six[i]) for i in range(6)}
    return(approaches)

def Damage(damage_list = [], count_list = []):
    damage_dict = {}
    for damage, count in zip(damage_list, count_list):
        damage_dict[str(damage)] = [[] for _ in range(count)]
    return(damage_dict)
        


import pickle 
from tkinter import filedialog

class Thing:
    
    def __init__(
            self, name = "NA", description = "NA", fate_points = str(0), refresh = str(0), 
            aspects = [], stunts = [], approaches = New_Approaches(),  
            stress = Damage([1, 2, 3], [1, 1, 1]), consequences = Damage([2, 4, 6], [1, 1, 1]),
            load = False):
        
        self.name = name ; self.description = description 
        self.fate_points = fate_points ; self.refresh = refresh
        self.aspects = aspects ; self.stunts = stunts
        self.approaches = approaches
        self.stress = stress ; self.consequences = consequences
        self.failed = False
        
        if(load):
            file_path = filedialog.askopenfilename()
            try:
                with open(file_path.format(self.name), 'rb') as handle:
                    self = pickle.load(handle)
            except:
                print("\nCouldn't load {}.".format(file_path))
                self.failed = True
                
    def New_Approaches(self, one_to_six):
        self.approaches = {approach_list[i] : str(one_to_six[i]) for i in range(6)}
            
    def save(self):
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
        aspects = ["An awesome example", "With a problem", "And other stuff"], 
        stunts = ["In this situation, I'm better at this!", "In this other situation, I'm better at this other thing!"], 
        approaches = New_Approaches([1,2,3,4,5,6]), 
        stress = Damage([1, 2, 3], [1, 2, 1]), 
        consequences = Damage([2, 4, 6], [1, 2, 1]),
        load = False)
    example.stress["2"][0] = "Muscle cramp"
    example.consequences["4"][0] = "Broken arm"
    print(example)
    example.save()