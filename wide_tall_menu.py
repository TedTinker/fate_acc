import string

from game import Object
from menu import Menu

class Tall_Menu(Menu):
    
    def __init__(self, kind, labels = [], entries = []):
        self.kind = kind ; self.labels = labels ; self.entries = entries 
        add_item = Object(kind + " Add " + kind, "Add " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_item)
        del_item = Object(kind + " Delete " + kind, "Delete " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_item)
        
        self.item = Object(kind, "", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "")
        
        super().__init__(kind, list_of_rows = [[add_item], [del_item]], widths = [], resetting = True)
        self.update_based_on_thing()
        
    def add_item(self, text = "", assemble = True):
        item = self.item.copy()
        if(len(self.active)-3 < len(self.labels)):
            item.name = self.labels[len(self.active)-3]
        item.text = text
        self.active.insert(-2, [item]) ; self.to_remove.append(item) ; self.widths.insert(-2, [1])
        if(assemble): self.assemble()
        
    def del_item(self):
        if(len(self.active) == 3): return
        self.active.pop(-3) ; self.widths.pop(-3)
        self.assemble()
        
    def update_thing(self):
        self.entries = [row[0].text for row in self.saved[1:-2]]
        return(self.entries)
    
    def update_based_on_thing(self):
        self.active = [[obj.copy() for obj in row] for row in self.active]
        self.active = [self.active[0], self.active[-2], self.active[-1]]
        for text in self.entries: self.add_item(text, assemble = False)
        self.save(); self.reset() 
        
        
        
def from_dict_or_new(i, d, new = lambda i : str(i)):
    values = list(d.keys())
    if(i < len(values)): return(values[i])
    else:                return(new(i+1))
            
    
    
class Wide_Tall_Menu(Menu):
    
    def __init__(self, kind, new = lambda i : str(i), entries = {}):
        self.kind = kind ; self.new = new ; self.entries = entries
        add_line = Object(kind + " Add " + kind, "Add " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_item)
        del_line = Object(kind + " Delete " + kind, "Delete " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_item)
        
        item = Object(kind, "", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "")
        self.line = [item, item.copy()]
        
        super().__init__(kind, list_of_rows = [[add_line], [del_line]], widths = [], resetting = True)
        self.update_based_on_thing()
        
    def add_item(self, texts = [], assemble = True):
        line = [obj.copy() for obj in self.line]
        line[0].text = from_dict_or_new(len(self.active)-3, self.entries, self.new)
        text = ", ".join(texts) # If you want to add more, do it here.
        line[1].text = text
        self.active.insert(-2, line) ; self.to_remove += line ; self.widths.insert(-2, [1, 10])
        if(assemble): self.assemble()
        
    def del_item(self):
        if(len(self.active) == 3): return
        self.active.pop(-3) ; self.widths.pop(-3)
        self.assemble()
        
    def update_thing(self):
        labels = [row[0].text for row in self.saved[1:-2]]
        for i, label in enumerate(labels):
            if(labels.count(label) > 1):
                alphabet = list(string.ascii_lowercase)
                labels = [l if l != label else l + alphabet.pop(0) for l in labels]
        self.entries = {label : [row[1].text] for label, row in zip(labels, self.saved[1:-2])}
        return(self.entries)
    
    def update_based_on_thing(self):
        self.active = [self.active[0], self.active[-2], self.active[-1]]
        self.labels = list(self.entries.keys())
        for damage, texts in self.entries.items(): 
            self.add_item(texts, assemble = False)
        self.save() ; self.reset()