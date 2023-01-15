from itertools import groupby

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)



from game import Game, Object, w, h

game = Game()



class Menu:
    
    def __init__(
            self, ID, list_of_rows = [], widths = [], bg_color = (50, 50, 50), space_between = .05, 
            saving = False, resetting = False, save_and_close = False, close_and_reset = False):
        
        self.ID = ID
        
        close_it = Object("CLOSE", color = (255, 0, 0), text_color = (0,0,0), double_click = lambda : self.close(reset = close_and_reset))
        list_of_rows.append([close_it])
            
        if(saving):
            save_it = Object("SAVE", color = (0, 255, 0), text_color = (0,0,0), double_click = lambda : self.save(close = save_and_close))
            list_of_rows[-1].append(save_it)
            
        if(resetting):
            reset_it = Object("RESET", color = (0, 0, 255), text_color = (0,0,0), double_click = lambda : self.reset(assemble = True))
            list_of_rows[-1].append(reset_it)
        
        for row in list_of_rows:
            for obj in row:  obj.ID = self.ID + " " + obj.ID
                    
        while(len(widths) < len(list_of_rows)):
            widths.append([])
        for i, row in enumerate(widths):
            while len(widths[i]) != len(list_of_rows[i]):
                widths[i].append(1)
        self.widths = widths
            
        self.active    = self.deep_copy(list_of_rows)
        self.saved     = self.deep_copy(list_of_rows)
        self.to_remove = []
        
        self.bg = Object(self.ID + " bg", color = bg_color)
        self.space_between = space_between
        self.x_start = space_between ; self.x_end = w/h - space_between
        self.y_start = space_between ; self.y_end = 1 - space_between
        self.bg.pos, self.bg.size = self.pos_size()
        
        self.submenus = []
        
    def deep_copy(self, list_of_rows):
        return([[obj.copy() for obj in row] for row in list_of_rows])
        
    def pos_size(self, x = None, y = None, width = "bg", last_x_pos = (0, 0)):
        if(width == "bg"):
            pos = (self.x_start, self.y_start)
            size = (self.x_end - self.x_start, self.y_end - self.y_start)
            return(pos, size)
        y_size = (self.y_end - self.y_start - self.space_between) / len(self.active)
        x_size = (self.x_end - self.x_start - self.space_between) * width
        pos = (self.x_start + last_x_pos, self.y_start + y * y_size + self.space_between)
        size = (x_size - self.space_between, y_size - self.space_between)
        return(pos, size)
        
    def assemble(self):  
        self.close()
        game.objects.append(self.bg)
        for y, row in enumerate(self.active):
            widths = [width / sum(self.widths[y]) for width in self.widths[y]]
            last_x_pos = self.space_between
            for x, obj in enumerate(row):
                obj.pos, obj.size = self.pos_size(x, y, widths[x], last_x_pos)
                last_x_pos = obj.pos[0] + obj.size[0]
                game.objects.append(obj); self.to_remove.append(obj)
                
    def close(self, reset = False):
        game.remove_object(self.bg.ID)
        for obj in self.to_remove: game.remove_object(obj.ID)
        self.to_remove = []
        if(reset): self.reset()
        
    def save(self, close = False):
        for submenu in self.submenus: submenu.save()
        self.saved = self.deep_copy(self.active)
        self.update_thing()
        self.render() # Just for example menu below
        if(close): self.close()
        
    def reset(self, assemble = False):
        self.active = self.deep_copy(self.saved)
        self.render()
        if(assemble == True): self.assemble()
        for submenu in self.submenus: submenu.reset()
        
    def update_thing(self):
        pass # For Superclasses
        
    def update_based_on_thing(self):
        pass # For Superclasses
        
    def render(self):
        pass # For Superclasses
        
    def __str__(self):
        s = "\n\n", self.ID
        for row in self.saved:
            for obj in row:
                s += obj.__str__() + ", "
            s += "\n"
        return(s)
    
    
    
if __name__ == "__main__":
    
    box  = Object("",  color = (255,255,255), text_color = (0, 0, 0))
    
    def add_box():
        b = box.copy()
        b.ID += str(len(menu.active[0])-1)
        b.text = b.ID
        menu.active[0].insert(-1, b) ; menu.to_remove.append(b) ; menu.widths[0].insert(-1, 1)
        menu.assemble()
        render()
        
    def del_box():
        if(len(menu.active[0]) == 2): return
        menu.active[0].pop(-2) ; menu.widths[0].pop(-2)
        menu.assemble()
        render()
    
    more = Object("+", color = (0,0,0), text_color = (255, 255, 255), double_click = add_box)
    less = Object("-", color = (0,0,0), text_color = (255, 255, 255), double_click = del_box)
    
    active  = Object("ACTIVE",  color = (255,0,0), text_color = (255, 255, 255))
    saved   = Object("SAVED",   color = (0,0,255), text_color = (255, 255, 255))
    
    def render():
        menu.active[1][0].text = ", ".join([menu.active[0][i].text for i in range(1,len(menu.active[0])-1)])
        menu.active[1][1].text = ", ".join([menu.saved[0][i].text for i in range(1,len(menu.saved[0])-1)])
        menu.assemble
    
    menu = Menu("TEST MENU", list_of_rows = [[more, less], [active, saved]], 
                widths = [[1,2]],
                saving = True, resetting = True)
    
    menu.render = render
    
    show = game.add_object("SHOW", color = (0,0,0), text_color = (255, 255, 255), size = (.1, .1), pos = ("center", "center"),
                 typeable = False, draggable = True, double_click = menu.assemble)
    
    game.run()