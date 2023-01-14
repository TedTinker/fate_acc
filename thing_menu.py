from game import Object
from menu import Menu, game
from things import Thing, approach_list
from wide_tall_menu import Tall_Menu, Wide_Tall_Menu
        
        
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
        thing_before = self.thing.copy()
        self.thing.name = self.saved[0][0].text
        self.thing.fate_points = self.saved[0][1].text 
        self.thing.refresh = self.saved[0][2].text 
        self.thing.description = self.saved[1][0].text
        self.thing.New_Approaches([self.saved[2][i].text for i in range(6)])
        
        self.thing.aspects      = self.submenus[0].update_thing()
        self.thing.stunts       = self.submenus[1].update_thing() 
        self.thing.stress       = self.submenus[2].update_thing() 
        self.thing.consequences = self.submenus[3].update_thing()    
        
        success = self.thing.save()
        if(not success): 
            self.thing = thing_before
            self.update_based_on_thing()
        return(success)
            
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
        if(close): self.close()
        if(self.thing_button != None):
            self.thing_button.name = self.thing.name
        
        
        
class New_Thing_Menu(Thing_Menu):
    
    def __init__(self):
        super().__init__(Thing())
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        success = self.update_thing()
        if(success):
            thing_button = game.add_object(self.thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), draggable = True)
            thing_menu = Thing_Menu(self.thing, thing_button)
            thing_button.double_click = thing_menu.assemble
        self.thing = Thing()
        self.update_based_on_thing()
        self.saved = self.deep_copy(self.active)
        self.reset()
        if(close): self.close()