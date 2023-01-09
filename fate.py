from game import Object
from menu import Menu, game

from things import Thing, approach_list
        
        
        
class Aspect_Menu(Menu):
    
    def __init__(self, thing = Thing()):
        self.thing = thing
        self.aspect = Object(self.thing.name + " Aspect", "Aspect", color = (255, 255, 255), text_color = (0,0,0), typeable = True)
        add_aspect = Object(self.thing.name + " Add Aspect", "Add Aspect",  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_aspect)
        del_aspect = Object(self.thing.name + " Delete Aspect", "Delete Aspect", color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_aspect)
        super().__init__(self.thing.name + " Aspects", list_of_rows = [[add_aspect], [del_aspect]])
        for text in self.thing.aspects:
            self.add_aspect(text, assemble = False)
        
    def add_aspect(self, text = "NA", assemble = True):
        asp = self.aspect.copy()
        if(len(self.active) == 3):   asp.name = "High Concept"
        elif(len(self.active) == 4): asp.name = "Trouble"
        else:                        asp.name = str(len(self.active)-4)
        asp.text = text
        self.active.insert(-2, [asp]) ; self.current.append([asp])
        if(assemble): self.assemble_menu()
        
    def del_aspect(self):
        if(len(self.active) == 3): return
        self.active.pop(-3)
        self.assemble_menu()
        
    def adjust_thing(self):
        aspects = [row[0].name + " : " + row[0].text for row in self.saved[1:-2]]
        self.thing.aspects = aspects
    
      
        
class Stunt_Menu(Menu):
    
    def __init__(self, thing = Thing()):
        self.thing = thing
        self.aspect = Object(self.thing.name + " Stunt", "Stunt", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "None")
        add_stunt = Object(self.thing.name + " Add Stunt", "Add Stunt",  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_stunt)
        del_stunt = Object(self.thing.name + " Delete Stunt", "Delete Stunt", color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_stunt)
        super().__init__(self.thing.name + " Stunts", list_of_rows = [[add_stunt], [del_stunt]])
        for text in self.thing.stunts:
            self.add_stunt(text, assemble = False)
        
    def add_stunt(self, text = "NA", assemble = True):
        stu = self.aspect.copy()
        stu.name = str(len(self.active)-2)
        stu.text = text
        self.active.insert(-2, [stu]) ; self.current.append([stu])
        if(assemble): self.assemble_menu()
        
    def del_stunt(self, assemble = True):
        if(len(self.active) == 3): return
        self.active.pop(-3)
        if(assemble): self.assemble_menu()
        
    def adjust_thing(self):
        stunts = [row[0].name + " : " + row[0].text for row in self.saved[1:-2]]
        self.thing.stunts = stunts
        
        
        
class Stress_Menu(Menu):
    
    def __init__(self, thing = Thing()):
        add_stress_value = Object("Add Stress Value",  color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.add_stress_value)
        del_stress_value = Object("Delete Stress Value", color = (0, 0, 0), text_color = (255, 255, 255), double_click = self.del_stress_value)
        super().__init__(self.thing.name + " Stress", list_of_rows = [[add_stress_value], [del_stress_value]])
        
    def add_stress_value(self):
        stu = self.aspect.copy()
        stu.name = str(len(self.active)-2)
        self.active.insert(-2, [stu]) ; self.current.append([stu])
        self.assemble_menu()
        
    def del_stress_value(self):
        if(len(self.active) == 3): return
        self.active.pop(-3)
        self.assemble_menu()
        
    def adjust_thing(self):
        pass
        
        
        
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

        self.aspect_menu = Aspect_Menu(thing = self.thing)
        aspects.double_click = self.aspect_menu.assemble_menu
        
        self.stunt_menu = Stunt_Menu(thing = self.thing)
        stunts.double_click = self.stunt_menu.assemble_menu
        
        list_of_rows = [
            [name, fate_points, refresh],
            [description],
            list_of_approaches,
            [aspects, stunts],
            [stress, consequences]]
        super().__init__(self.thing.name + " THING", list_of_rows = list_of_rows, saving = True)
        
    def adjust_thing(self):
        self.thing.name = self.saved[0][0].text
        self.thing.fate_points = self.saved[0][1].text 
        self.thing.refresh = self.saved[0][2].text 
        self.thing.description = self.saved[1][0].text
        self.thing.New_Approaches([self.saved[2][i].text for i in range(6)])
        
        self.thing.aspects = [self.aspect_menu.saved[i][0].text for i in range(1, len(self.aspect_menu.saved)-2)]
        self.thing.stunts = [self.stunt_menu.saved[i][0].text for i in range(1, len(self.stunt_menu.saved)-2)]
        
        self.thing.save()
        
        
        
class New_Thing_Menu(Thing_Menu):
    
    def __init__(self):
        super().__init__(Thing())
        
    def save_and_close(self):
        self.just_save()
        self.just_close()
        game.add_object(self.thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), 
                     double_click = Thing_Menu(self.thing).assemble_menu, draggable = True)
        self.totally_reset()
        self.aspect_menu.totally_reset()
        self.stunt_menu.totally_reset()
                
        
        
def load_this():
    thing = Thing(load = True)
    print("\nafter loading:")
    print(thing)
    if(thing.failed): return
    game.add_object(thing.name, color = (0,0,0), text_color = (255, 255, 255), pos = ("center", "center"), size = (.3, .1), 
                 double_click = Thing_Menu(thing).assemble_menu, draggable = True)


    
new = game.add_object("NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = New_Thing_Menu().assemble_menu)
load = game.add_object("LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (.12, .01), size = (.1, .1), 
             double_click = load_this)
# For remove, consider opening a new menu
remove = game.add_object("REMOVE", color = (0,0,0), text_color = (255, 255, 255), pos = (.23, .01), size = (.1, .1),
             double_click = lambda : None)

game.run()