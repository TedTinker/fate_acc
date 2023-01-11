from game import Object
from menu import Menu, game

from things import Thing, approach_list



class Tall_Menu(Menu):
    
    def __init__(self, kind, labels = [], thing = Thing()):
        self.thing = thing ; self.labels = labels
        self.item = Object(self.thing.name + " " + kind, "Aspect", color = (255, 255, 255), text_color = (0,0,0), typeable = True)
        add_item = Object(self.thing.name + " Add " + kind, "Add " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_item)
        del_item = Object(self.thing.name + " Delete " + kind, "Delete " + kind,  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_item)
        super().__init__(self.thing.name + " " + kind, list_of_rows = [[add_item], [del_item]], resetting = True)
        self.update_based_on_thing()
        
    def add_item(self, text = "NA", assemble = True):
        item = self.item.copy()
        if(len(self.active)-3 < len(self.labels)):
            item.name = self.labels[len(self.active)-3]
        else:
            item.name = str(len(self.active)-2-len(self.labels))
        item.text = text
        self.active.insert(-2, [item]) ; self.to_remove.append(item)
        if(assemble): self.assemble()
        
    def del_item(self):
        if(len(self.active) == 3): return
        self.active.pop(-3)
        self.assemble()
        
    def update_thing(self):
        items = [row[0].name + " : " + row[0].text for row in self.saved[1:-2]]
        return(items)
    
    def update_based_on_thing(self):
        for text in self.thing.aspects: self.add_item(text, assemble = False)
        self.save()
        self.reset()
        
        
        
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

        aspect_menu = Tall_Menu(kind = "Aspect", labels = ["High Concept", "Trouble"], thing = self.thing)
        aspects.double_click = aspect_menu.assemble
        
        stunt_menu = Tall_Menu(kind = "Stunt", thing = self.thing)
        stunts.double_click = stunt_menu.assemble
        
        list_of_rows = [
            [name, fate_points, refresh],
            [description],
            list_of_approaches,
            [aspects, stunts],
            [stress, consequences]]
        super().__init__(self.thing.name + " THING", list_of_rows = list_of_rows, saving = True, resetting = True, save_and_close = True, close_and_reset = True)
        self.submenus = [aspect_menu, stunt_menu]
        for submenu in self.submenus:
            submenu.thing = self.thing
            submenu.reset()
        
    def update_thing(self):
        self.thing.name = self.saved[0][0].text
        self.thing.fate_points = self.saved[0][1].text 
        self.thing.refresh = self.saved[0][2].text 
        self.thing.description = self.saved[1][0].text
        self.thing.New_Approaches([self.saved[2][i].text for i in range(6)])
        
        for i, submenu in enumerate(self.submenus):
            self.thing.aspects = [submenu.saved[i][0].text for i in range(1, len(submenu.saved)-2)]
                    
        self.thing.save()
        
    def update_based_on_thing(self):
        self.saved[0][0].text = self.thing.name 
        self.saved[0][1].text = self.thing.fate_points 
        self.saved[0][2].text = self.thing.refresh 
        self.saved[1][0].text = self.thing.description 
        for i, obj in enumerate(self.saved[2]):
            self.saved[2][i].text = self.thing.approaches[self.saved[2][i].name]
        self.reset()
        
        
        
class New_Thing_Menu(Thing_Menu):
    
    def __init__(self):
        super().__init__(Thing(), )
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        self.update_thing()
        game.add_object(self.thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), 
                     double_click = Thing_Menu(self.thing).assemble, draggable = True)
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