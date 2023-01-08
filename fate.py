from game import Game, Object, w, h
from things import Thing, approach_list

game = Game()



def get_load_this(load_button):
    def load_this():
        thing = Thing(name = load_button.text, load = load_button.text)
        if(thing.failed): return
        thing_object(thing)
    return(load_this)

def thing_object(thing):
    thing_obj = game.add_object(
        name = thing.name, color = (0,0,0), text_color = (255, 255, 255), 
        pos = ("center", "center"), size = (.3, .1), draggable = True)
    thing_menu = make_thing_menu(group = thing.name)
    thing_obj.double_click = thing_menu.assemble_menu
    # Change stuff in the menus to reflect the thing!



class Menu:
    
    def __init__(self, group, name, bg, list_of_rows, space_between = .05,
                 x_start = .01, x_end = w/h - .01, y_start = .01, y_end = .99):
    
        self.group = group ; self.name = name
        self.bg = bg  ; bg.name = self.name + " " + bg.name ; self.list_of_rows = list_of_rows
        self.space_between = space_between
        self.x_start = x_start ; self.x_end = x_end 
        self.y_start = y_start ; self.y_end = y_end 
        
        self.cancel = Object(group = self.group, name = "CANCEL", color = (255, 0, 0), text_color = (0,0,0))
        self.save = Object(group = self.group, name = "SAVE", color = (0, 255, 0), text_color = (0,0,0))
        self.cancel.double_click = self.cancel_menu
        self.save.double_click = self.save_and_close
        self.list_of_rows.append([self.cancel, self.save])
        
        self.original = [[obj.copy() for obj in row] for row in self.list_of_rows]
        self.saved = [[obj.copy() for obj in row] for row in self.list_of_rows]
        self.in_action = []
        
    def assemble_menu(self):  
        print("\n\n")
        self.delete() ; self.in_action = []
        bg = self.bg.copy() ; bg.group = self.group
        bg.pos = (self.x_start, self.y_start) ; bg.size = (self.x_end - self.x_start, self.y_end - self.y_start)
        game.objects.append(bg)
        
        self.in_action = [[obj.copy() for obj in row] for row in self.list_of_rows]
    
        y_dif = (self.y_end - self.y_start - self.space_between) / len(self.in_action)
        for y, row in enumerate(self.in_action):
            x_dif = (self.x_end - self.x_start - self.space_between) / len(row)
            for x, obj in enumerate(row):
                obj.pos = (self.x_start + x * x_dif + self.space_between, self.y_start + y * y_dif + self.space_between)
                obj.size = (x_dif - self.space_between, y_dif - self.space_between)
                obj.group = self.group + " " + self.name
                game.objects.append(obj)
                print("Adding {}".format(obj.group + ", " + obj.name))
        
    def delete(self):
        print("\n\n")
        game.remove_object(self.group, self.bg.name)
        for row in self.in_action:
            for obj in row:
                print("REMOVING {}".format(obj.group + ", " + obj.name))
                game.remove_object(obj.group, obj.name)
        
    def cancel_menu(self):
        self.delete()
        self.list_of_rows = self.saved
        if(self.group == "NEW_THING" and self.name == "THING"):
            self.reset()
                
    def save_and_close(self):
        self.delete()
        if(self.group == "NEW_THING" and self.name == "THING"):
            print("SAVE THINGY!")
            thing = Thing() ; thing.save()
            thing_object(thing)
            self.reset()
            return
        print("SAVING")
        self.saved = [[obj.copy() for obj in row] for row in self.in_action]
        self.list_of_rows = self.saved
        
    def reset(self):
        aspects = self.list_of_rows[3][0].copy()
        aspect_menu = make_aspect_menu(group = self.group)
        aspects.double_click = aspect_menu.assemble_menu
        self.list_of_rows[3][0] = aspects
        
        stunt_menu = make_stunt_menu(group = self.group)
        self.list_of_rows[3][1].double_click = stunt_menu.assemble_menu

                
        
        

def make_thing_menu(group = ""):
    bg =  Object(name = "bg", color = (50, 50, 50))
    name = Object(name = "Name", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "None")
    description = Object(name = "Description", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "None")
    fate_points = Object(name = "Fate Points", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "3")
    refresh = Object(name = "Refresh", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "3")
    list_of_approaches = [Object(name = approach, color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "0") for approach in approach_list]
    aspects = Object(name = "Aspects", color = (0, 0, 0), text_color = (255, 255, 255))
    stunts = Object(name = "Stunts", color = (0, 0, 0), text_color = (255, 255, 255))
    stress = Object(name = "Stress", color = (0, 0, 0), text_color = (255, 255, 255))
    consequences = Object(name = "Consequences", color = (0, 0, 0), text_color = (255, 255, 255))
    thing_menu = Menu(group, "THING", bg, [
        [name, fate_points, refresh],
        [description],
        list_of_approaches,
        [aspects, stunts],
        [stress, consequences]])
    aspect_menu = make_aspect_menu(group = group)
    aspects.double_click = aspect_menu.assemble_menu
    stunt_menu = make_stunt_menu(group = group)
    stunts.double_click = stunt_menu.assemble_menu
    return(thing_menu)

def make_aspect_menu(group = ""):
    bg =  Object(name = "bg", color = (50, 50, 50))
    aspect = Object(name = "Aspect", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "None")
    add_aspect = Object(name = "Add Aspect", color = (0, 0, 0), text_color = (255, 255, 255))
    delete_aspect = Object(name = "Delete Aspect", color = (0, 0, 0), text_color = (255, 255, 255))
    aspect_menu = Menu(group, "ASPECTS", bg, [[add_aspect], [delete_aspect]])
    
    def add_aspect():
        print("Adding aspect")
        asp = aspect.copy()
        if(len(aspect_menu.list_of_rows) == 3):   asp.name = "High Concept"
        elif(len(aspect_menu.list_of_rows) == 4): asp.name = "Trouble"
        else:                                     asp.name = str(len(aspect_menu.list_of_rows)-4)
        aspect_menu.list_of_rows.insert(-2, [asp])
        aspect_menu.assemble_menu()
    aspect_menu.list_of_rows[0][0].double_click = add_aspect 
    
    def del_aspect():
        print("Deleting aspect")
        if(len(aspect_menu.list_of_rows) == 3): return
        aspect_menu.delete()
        aspect_menu.list_of_rows.pop(-3)
        aspect_menu.assemble_menu()
    aspect_menu.list_of_rows[-2][0].double_click = del_aspect 
        
    return(aspect_menu)

def make_stunt_menu(group = ""):
    bg =  Object(name = "bg", color = (50, 50, 50))
    stunt = Object(name = "Stunt", color = (255, 255, 255), text_color = (0,0,0), typeable = True, text = "None")
    add_stunt = Object(name = "Add Stunt", color = (0, 0, 0), text_color = (255, 255, 255))
    delete_stunt = Object(name = "Delete Stunt", color = (0, 0, 0), text_color = (255, 255, 255))
    stunt_menu = Menu(group, "STUNTS", bg, [[add_stunt], [delete_stunt]])
    
    def add_stunt():
        print("Adding stunt")
        stu = stunt.copy()
        stu.name = str(len(stunt_menu.list_of_rows)-2)
        stunt_menu.list_of_rows.insert(-2, [stu])
        stunt_menu.assemble_menu()
    stunt_menu.list_of_rows[0][0].double_click = add_stunt
    
    def del_stunt():
        print("Deleting stunt")
        if(len(stunt_menu.list_of_rows) == 3): return
        stunt_menu.delete()
        stunt_menu.list_of_rows.pop(-3)
        stunt_menu.assemble_menu()
    stunt_menu.list_of_rows[-2][0].double_click = del_stunt
        
    return(stunt_menu)


    


new = game.add_object(name = "NEW", color = (0,0,0), text_color = (255, 255, 255), pos = (.01, .01), size = (.1, .1), 
             double_click = make_thing_menu(group = "NEW_THING").assemble_menu)
load = game.add_object(name = "LOAD", color = (0,0,0), text_color = (255, 255, 255), pos = (w/h - .31, .01), size = (.3, .1), 
             typeable = True, text = "None")
load.double_click = get_load_this(load)

game.run()