from game import Object
from menu import Menu, game

from things import Thing, approach_list



class Tall_Menu(Menu):
    
    def __init__(self, kind, labels = [], entries = []):
        self.kind = kind ; self.labels = labels ; self.entries = entries 
        add_item = Object(kind + " Add " + kind, "Add " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_item)
        del_item = Object(kind + " Delete " + kind, "Delete " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_item)
        
        self.item = Object(kind, "", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "")
        
        super().__init__(kind, list_of_rows = [[add_item], [del_item]], resetting = True)
        self.update_based_on_thing()
        
    def add_item(self, text = "", assemble = True):
        item = self.item.copy()
        if(len(self.active)-3 < len(self.labels)):
            item.name = self.labels[len(self.active)-3]
        item.text = text
        self.active.insert(-2, [item]) ; self.to_remove.append(item)
        if(assemble): self.assemble()
        
    def del_item(self):
        if(len(self.active) == 3): return
        self.active.pop(-3)
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
    else:                return(new(i))
            
    
    
class Wide_Tall_Menu(Menu):
    
    def __init__(self, kind, new = lambda i : str(i), entries = {}):
        self.kind = kind ; self.new = new ; self.entries = entries
        add_line = Object(kind + " Add " + kind, "Add " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_item)
        del_line = Object(kind + " Delete " + kind, "Delete " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_item)
        
        item = Object(kind, "", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "")
        self.line = [item, item.copy()]
        
        super().__init__(kind, list_of_rows = [[add_line], [del_line]], resetting = True)
        self.update_based_on_thing()
        
    def add_item(self, texts = [], assemble = True):
        line = [obj.copy() for obj in self.line]
        line[0].text = from_dict_or_new(len(self.active)-3, self.entries, self.new)
        text = ", ".join(texts) # If you want to add more, do it here.
        line[1].text = text
        self.active.insert(-2, line) ; self.to_remove += line
        if(assemble): self.assemble()
        
    def del_item(self):
        if(len(self.active) == 3): return
        self.active.pop(-3)
        self.assemble()
        
    def update_thing(self):
        self.entries = {row[0].text : [row[1].text] for row in self.saved[1:-2]}
        return(self.entries)
    
    def update_based_on_thing(self):
        self.active = [[obj.copy() for obj in row] for row in self.active]
        self.active = [self.active[0], self.active[-2], self.active[-1]]
        self.labels = list(self.entries.keys())
        for damage, texts in self.entries.items(): 
            self.add_item(texts, assemble = False)
        self.save() ; self.reset()
        
        
        
class Thing_Menu(Menu):
    
    def __init__(self, thing = Thing()):
        self.thing = thing
        name = Object("Name", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = thing.name)
        description = Object("Description", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = thing.description)
        fate_points = Object("Fate Points", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = thing.fate_points)
        refresh = Object("Refresh", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = thing.refresh)
        
        list_of_approaches = [Object(approach, color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = self.thing.approaches[approach]) for approach in approach_list]
        aspects = Object("Aspects", color = (0, 0, 0), text_color = (255, 255, 255))
        stunts = Object("Stunts", color = (0, 0, 0), text_color = (255, 255, 255))
        stress = Object("Stress", color = (0, 0, 0), text_color = (255, 255, 255))
        consequences = Object("Consequences", color = (0, 0, 0), text_color = (255, 255, 255))

        aspect_menu = Tall_Menu(kind = "Aspect", labels = ["High Concept", "Trouble"], entries = self.thing.aspects)
        aspects.double_click = aspect_menu.assemble
        
        stunt_menu = Tall_Menu(kind = "Stunt", entries = self.thing.stunts)
        stunts.double_click = stunt_menu.assemble
        
        stress_menu = Wide_Tall_Menu(kind = "Stress", new = lambda i : str(i), entries = self.thing.stress)
        stress.double_click = stress_menu.assemble
        
        conseq_menu = Wide_Tall_Menu(kind = "Consequences", new = lambda i : 2*str(i), entries = self.thing.consequences)
        consequences.double_click = conseq_menu.assemble
        
        list_of_rows = [
            [name, fate_points, refresh],
            [description],
            list_of_approaches,
            [aspects, stunts],
            [stress, consequences]]
        super().__init__(self.thing.name + " THING", list_of_rows = list_of_rows, saving = True, resetting = True, save_and_close = True, close_and_reset = True)
        self.submenus = [aspect_menu, stunt_menu, stress_menu, conseq_menu]
        for submenu in self.submenus:
            submenu.reset()
        
    def update_thing(self):
        self.thing.name = self.saved[0][0].text
        self.thing.fate_points = self.saved[0][1].text 
        self.thing.refresh = self.saved[0][2].text 
        self.thing.description = self.saved[1][0].text
        self.thing.New_Approaches([self.saved[2][i].text for i in range(6)])
        
        self.thing.aspects      = self.submenus[0].update_thing()
        self.thing.stunts       = self.submenus[1].update_thing() 
        self.thing.stress       = self.submenus[2].update_thing() 
        self.thing.consequences = self.submenus[3].update_thing()    
          
        self.thing.save()
        
    def update_based_on_thing(self):
        self.saved[0][0].text = self.thing.name 
        self.saved[0][1].text = self.thing.fate_points 
        self.saved[0][2].text = self.thing.refresh 
        self.saved[1][0].text = self.thing.description 
        for i, obj in enumerate(self.saved[2]):
            self.saved[2][i].text = self.thing.approaches[self.saved[2][i].name]
        
        self.submenus[0].entries = self.thing.aspects      ; self.submenus[0].update_based_on_thing()
        self.submenus[1].entries = self.thing.stunts       ; self.submenus[1].update_based_on_thing()
        self.submenus[2].entries = self.thing.stress       ; self.submenus[2].update_based_on_thing()
        self.submenus[3].entries = self.thing.consequences ; self.submenus[3].update_based_on_thing()
        
        self.reset()
        
        
        
class New_Thing_Menu(Thing_Menu):
    
    def __init__(self):
        super().__init__(Thing())
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        self.update_thing()
        game.add_object(self.thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), 
                     double_click = Thing_Menu(self.thing).assemble, draggable = True)
        self.thing = Thing()
        self.update_based_on_thing()
        self.saved = self.deep_copy(self.active)
        self.reset()
        if(close): self.close()
        

                
def load_this():
    thing = Thing(load = True)
    if(thing.failed): return
    print("\nLoaded:")
    print(thing)
    game.add_object(thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), 
                 double_click = Thing_Menu(thing).assemble, draggable = True)


    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)
# For remove, consider opening a new menu
remove = game.add_object("REMOVE", color = (0,0,0), text_color = (255, 255, 255), pos = (.23, .01), size = (.1, .1),
             double_click = lambda : None)

game.run()