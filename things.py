approach_list = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
def New_Approaches(one_to_six = [0,0,0,0,0,0]):
    approaches = {approach_list[i] : str(one_to_six[i]) for i in range(6)}
    return(approaches)

def Damage(damage_list = [], count_list = [], text_list = None):
    damage_dict = {}
    if(text_list == None): text_list = [["" for _ in range(count)] for count in count_list]
    for damage, count, texts in zip(damage_list, count_list, text_list):
        damage_dict[str(damage)] = [text for text in texts]
    return(damage_dict)
        


import pickle 
from tkinter import filedialog

class Thing:
    
    def __init__(
            self, name = "", description = "", fate_points = str(3), refresh = str(3), 
            aspects = ["", "", ""], stunts = [""], approaches = New_Approaches(),  
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
                with open(file_path, 'rb') as handle:
                    thing = pickle.load(handle)
            except:
                print("\nCouldn't load {}.".format(file_path))
                self.failed = True
                return
            self.name = thing.name ; self.description = thing.description 
            self.fate_points = thing.fate_points ; self.refresh = thing.refresh
            self.aspects = thing.aspects ; self.stunts = thing.stunts
            self.approaches = thing.approaches
            self.stress = thing.stress ; self.consequences = thing.consequences
                
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
        consequences = Damage([2, 4, 6], [1, 2, 1], [[""], ["Broken leg", ""], [""]]), 
        load = False)
    print(example)
    example.save()
    
    print("\n\n\n")
    example = Thing(load = True)
    print(example)