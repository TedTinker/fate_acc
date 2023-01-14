import string

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
    else:                return(new(i+1))
            
    
    
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
        
        
        
class Thing_Menu(Menu):
    
    def __init__(self, thing = Thing(), thing_button = None):
        self.thing = thing ; self.thing_button = thing_button
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
        
        conseq_menu = Wide_Tall_Menu(kind = "Consequences", new = lambda i : str(2*i), entries = self.thing.consequences)
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
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        self.update_thing()
        self.render() # Just for example menu below
        if(close): self.close()
        if(self.thing_button != None):
            print("Changing name")
            self.thing_button.name = self.thing.name
        
        
        
class New_Thing_Menu(Thing_Menu):
    
    def __init__(self):
        super().__init__(Thing())
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        self.update_thing()
        thing_button = game.add_object(self.thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), draggable = True)
        thing_menu = Thing_Menu(self.thing, thing_button)
        thing_button.double_click = thing_menu.assemble
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
    thing_button = game.add_object(thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), draggable = True)
    thing_menu = Thing_Menu(thing, thing_button)
    thing_button.double_click = thing_menu.assemble
    thing_button.right_click = get_right_click_this(thing_button)
    
    
    
def get_right_click_this(obj):
    
    def right_click_this():
        positions = [(obj.pos[0] + obj.size[0], obj.pos[1] + obj.size[1] + .11*y) for y in range(3)]
        done = game.add_object("DONE", color = (200,200,200), text_color = (0, 0, 0), pos = positions[0], size = (.5, .1))
        remove = game.add_object("REMOVE {}".format(obj.name), color = (50,50,50), text_color = (0, 0, 0), pos = positions[1], size = (.5, .1))
        
        buttons = [done, remove]
        
        def get_remove_these_and(then = lambda : None):
            def remove_these_and():
                for obj in buttons: game.remove_object(obj.ID)
                then()
            return(remove_these_and)
        
        remove.double_click = get_remove_these_and(lambda : game.remove_object(obj.ID)) # game.remove_object(obj.ID)
        done.double_click = get_remove_these_and()
    return(right_click_this)


    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)

game.run()